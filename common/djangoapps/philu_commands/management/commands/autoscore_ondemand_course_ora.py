from logging import getLogger

from lms.djangoapps.grades.new.course_grade import CourseGradeFactory, CourseGrade
from pytz import utc
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from lms.djangoapps.courseware.courses import get_course_with_access

from student.models import CourseEnrollment

log = getLogger(__name__)

DAYS_TO_SEND_EMAIL = 7


class Command(BaseCommand):
    help = """
    Send Notifications prompts to users who have not entered into course after Course Open Date.
    Orientation module will not be considered because that module will be accessible to user 
    before course actually starts. We are managing this by introducing our own date "Course Open Date"
    in custom setting.
    Note: As we know in some cases enrollment process may continues after Course Open Date so if any student
    enroll to some course after 7 days of course open date, those users will not be notified.
    """

    def handle(self, *args, **options):

        from django.contrib.auth.models import User
        from openedx.core.djangoapps.content.course_overviews.models import CourseOverview

        courses = CourseOverview.objects.filter(self_paced=True)

        for course in courses:
            enrollments = CourseEnrollment.objects.filter(course_id=course.id, is_active=True)

            for enrollment in enrollments:

                today = datetime.now(utc).date()
                delta_days = today - enrollment.created.date()
                current_module = delta_days.days / 7 + 1
                user = enrollment.user

                log.info('Enrolled Course: %s and User: %s', course.id, user)
                log.info('Days passed by enrollment: %s User at Module: %s', delta_days.days, current_module)

                if current_module < 3:
                    log.info('Current module is less than 3')
                    continue

                else:
                    i = 1
                    # student = User.objects.prefetch_related("groups").get(id=user.id)
                    # course_access = get_course_with_access(user, 'load', course.id, depth=None, check_if_enrolled=True)
                    #
                    # course_grade = CourseGradeFactory().create(student, course_access)
                    from lms.djangoapps.course_blocks.api import get_course_blocks
                    course_blocks = get_course_blocks(user, course.location)
                    course_grade = CourseGrade(user, course, course_blocks)
                    courseware_summary = course_grade.chapter_grades

                    for index_chapter, chapter in enumerate(courseware_summary):
                        if i < current_module:
                            for section in chapter['sections']:
                                if len(section._get_visible_blocks) > 0:
                                    for visible_blocks in section._get_visible_blocks:
                                        block_id = visible_blocks[0]
                                        # visible_blocks[0] return Block Usage Locator
                                        if block_id.block_type == 'openassessment':

                                            # check if this chapter is 2 weeks older or not.
                                            module_access_days = delta_days.days - (index_chapter * 7)
                                            log.info('Module accessed: %s', module_access_days)

                                            from submissions.models import Submission
                                            # user = User.objects.get(id=student['id'])

                                            from student.models import AnonymousUserId
                                            anonymous_user = AnonymousUserId.objects.get(user=user, course_id=course.id)

                                            # anonymous_user = user.anonymoususerid_set.get(course_id=course.id)
                                            log.info('Anonymous User ID: %s', anonymous_user.anonymous_user_id)
                                            try:
                                                response_submissions = Submission.objects.get(student_item__student_id=anonymous_user.anonymous_user_id,
                                                                                              student_item__item_id=block_id)
                                                log.info('Response Created at: %s', response_submissions.created_at.date())

                                                response_submission_delta = today - response_submissions.created_at.date()

                                                if module_access_days >= 14 and response_submission_delta.days >= 14:
                                                    log.info('Block Type: %s', visible_blocks[0].block_type)
                                                    try:
                                                        from openassessment.workflow.models import AssessmentWorkflow
                                                        AssessmentWorkflow.objects.get(status=AssessmentWorkflow.STATUSES[0], course_id=course.id, item_id=block_id, submission_uuid=response_submissions.uuid)
                                                        autoscore_ora(user, course.id, unicode(visible_blocks[0]), anonymous_user)
                                                    except AssessmentWorkflow.DoesNotExist:
                                                        continue


                                            except Submission.DoesNotExist:
                                                continue

                        i = i + 1


def autoscore_ora(user, course_id, usage_key, anonymous_user):
    from submissions.models import Submission
    from submissions.api import reset_score, set_score
    from openassessment.assessment.serializers import rubric_from_dict
    from openassessment.assessment.models import Assessment, AssessmentPart
    student = {'id': user.id, 'username': user.username, 'email': user.email,
               'anonymous_user_id': anonymous_user.anonymous_user_id}

    # anonymous_user = user.anonymoususerid_set.get(course_id=course_id)

    # Find the associated rubric for that course_id & item_id
    rubric_dict = _get_rubric_for_course(course_id, usage_key)

    rubric = rubric_from_dict(rubric_dict)
    options_selected, earned, possible = _select_options(rubric_dict)

    # Use usage key and student id to get the submission of the user.
    try:
        submission = Submission.objects.get(
            student_item__course_id=course_id.to_deprecated_string(),
            student_item__student_id=student['anonymous_user_id'],
            student_item__item_id=usage_key,
            student_item__item_type='openassessment'
        )
    except Submission.DoesNotExist:
        log.warn(u"No submission found for user {user_id}".format(
            user_id=student['anonymous_user_id']
        ))
        return

    # Create assessments
    assessment = Assessment.create(
        rubric=rubric,
        scorer_id=_get_philu_bot(),
        submission_uuid=submission.uuid,
        score_type='ST'
    )
    AssessmentPart.create_from_option_names(
        assessment=assessment,
        selected=options_selected
    )

    log.info(
        u"Created assessment for user {user_id}, submission {submission}, "
        u"course {course_id}, item {item_id} with rubric {rubric} by PhilU Bot.".format(
            user_id=student['anonymous_user_id'],
            submission=submission.uuid,
            course_id=course_id.to_deprecated_string(),
            item_id=usage_key,
            rubric=rubric.content_hash
        )
    )

    reset_score(
        student_id=student['anonymous_user_id'],
        course_id=course_id.to_deprecated_string(),
        item_id=usage_key
    )

    set_score(
        submission_uuid=submission.uuid,
        points_earned=earned,
        points_possible=possible
    )

    return 0


def _select_options(rubric_dict):
    criteria = rubric_dict['criteria']
    options_selected = {}
    points_earned = 0
    points_possible = 0

    for crit in criteria:
        options = crit['options']
        points = list(set([o['points'] for o in options]))

        if len(points) > 2:
            # 3 pt rubric
            pt = points[-2]
        else:
            # 2 pt rubric
            pt = points[-1]

        points_earned += pt
        points_possible += max(points)
        # Get a list of all options with the pt value.
        # Some rubrics have multiple options against a single point value.
        # for such cases we are using list here.
        options_selected[crit['name']] = [o['name'] for o in options if o['points'] == pt][0]

    return options_selected, points_earned, points_possible


def _get_rubric_for_course(course_id, usage_key):
    from xmodule.modulestore.django import modulestore
    from openedx.core.lib.url_utils import unquote_slashes
    from opaque_keys.edx.locations import SlashSeparatedCourseKey
    course_id = SlashSeparatedCourseKey.from_deprecated_string(course_id.to_deprecated_string())
    usage_key = course_id.make_usage_key_from_deprecated_string(unquote_slashes(usage_key))

    instance = modulestore().get_item(usage_key)
    return {
        'prompts': instance.prompts,
        'criteria': instance.rubric_criteria
    }


def _get_philu_bot():
    import hashlib
    from django.conf import settings
    from django.contrib.auth.models import User
    # Check if bot user exist
    philu_bot, _ = User.objects.get_or_create(
        username='philubot',
        defaults={
            'first_name': 'PhilU',
            'last_name': 'Bot',
            'email': 'bot@philanthropyu.org',
            'is_active': True
        }
    )

    # Create anonymized id for the bot
    hasher = hashlib.md5()
    hasher.update(settings.SECRET_KEY)
    hasher.update(unicode(philu_bot.id))
    digest = hasher.hexdigest()

    return digest
