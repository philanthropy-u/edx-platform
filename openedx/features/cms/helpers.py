from dateutil.parser import parse
from django.contrib.auth.models import User

from xmodule.course_module import CourseFields
from courseware.courses import get_course_by_id
from openedx.features.course_card.helpers import initialize_course_settings

from openassessment.xblock.defaults import DEFAULT_START, DEFAULT_DUE
from xmodule.modulestore.django import modulestore


def apply_post_rerun_creation_tasks(source_course_key, destination_course_key, user_id):
    """
    This method is responsible for applying all the tasks after re-run creation has successfully completed

    :param source_course_key: source course key (from which the course was created)
    :param destination_course_key: re run course key (key of the re run created)
    :param user_id: user that created this course
    """
    user = User.objects.get(id=user_id)

    # initialize course custom settings
    initialize_course_settings(source_course_key, destination_course_key)

    re_run = get_course_by_id(destination_course_key)

    # If re run has the default start date, it was created from old flow
    if re_run.start == CourseFields.start.default:
        return

    source_course = get_course_by_id(source_course_key)

    # Set course re-run module start and due dates according to the source course
    set_rerun_course_dates(source_course, re_run, user)


def set_rerun_course_dates(source_course, re_run, user):
    """
    This method is responsible for updating all required dates for the re-run course according to
    source course.
    """
    source_course_start_date = source_course.start
    re_run_start_date = re_run.start

    re_run_sections = re_run.get_children()
    re_run_subsections = [sub_section for s in re_run_sections for sub_section in s.get_children()]

    # If there are no sections ignore setting dates
    if not re_run_sections:
        return

    set_rerun_module_dates(re_run_sections.extend(re_run_subsections),
                           source_course_start_date, re_run_start_date, user)

    set_rerun_ora_dates(re_run_subsections, re_run_start_date, source_course_start_date, user)


def set_rerun_module_dates(re_run_sections, source_course_start_date, re_run_start_date, user):
    """
    This method is responsible for updating all section and subsection start and due dates for the re-run
    according to source course. This is achieved by calculating the delta between a source section/subsection's
    relevant date and start date, and then adding that delta to the start_date of the re-run course.
    """
    from cms.djangoapps.contentstore.views.item import _save_xblock

    for xblock in re_run_sections:
        meta_data = dict()

        meta_data['start'] = calculate_date_by_delta(xblock.start, source_course_start_date, re_run_start_date)

        if xblock.due:
            meta_data['due'] = calculate_date_by_delta(xblock.due, source_course_start_date, re_run_start_date)

        _save_xblock(user, xblock, metadata=meta_data)


def set_rerun_ora_dates(re_run_subsections, re_run_start_date, source_course_start_date, user):
    """
    This method is responsible for updating all dates in ORA i.e submission, start, due etc, for
    the re-run according to source course. This is achieved by calculating new dates for ORA based
    on delta value.
    :param re_run_subsections: list of subsection in a (re-run) course
    :param re_run_start_date: course start date of source course
    :param source_course_start_date: course start date of source course
    :param user: user that created this course
    """
    def update_date_by_delta(date_to_update, default_date):
        """
        Method to calculate new dates for ORA, on re-run, according to previous values. The delta
        is calculated from course start date of source course and re-run course. Delta is then
        added to previous dates in ORA. If date to update is default date then same date is
        returned with negative flag, indicating no need to update date.

        :param date_to_update: submission, start or due date from ORA
        :param default_date: DEFAULT_START or DEFAULT_DUE dates for ORA
        :return: date string and boolean flag indicating need for updating ORA date
        """
        date_update_required = date_to_update and not date_to_update.startswith(default_date)
        if date_update_required:
            date_delta = source_course_start_date - parse(date_to_update)
            updated_date = (re_run_start_date - date_delta).strftime('%Y-%m-%dT%H:%M:%S%z')
            return updated_date, date_update_required
        else:
            return date_to_update, date_update_required

    # flat sub-sections to the level of components and pick ORA only
    re_run_ora_list = [component for subsection in re_run_subsections for unit in
                  subsection.get_children() for component in unit.get_children() if
                  component.category == 'openassessment']

    for ora in re_run_ora_list:
        ora.submission_start, to_update = update_date_by_delta(ora.submission_start, DEFAULT_START)
        ora.submission_due, to_update = update_date_by_delta(ora.submission_due, DEFAULT_DUE)

        for assessment in ora.rubric_assessments:
            if 'start' in assessment:
                assessment['start'], to_update = update_date_by_delta(assessment['start'], DEFAULT_START)
            if 'due' in assessment:
                assessment['due'], to_update = update_date_by_delta(assessment['due'], DEFAULT_DUE)

        # If all dates in ORA are default then no need to update it during re-run process
        if not to_update:
            continue

        component_update(ora, user)


def component_update(descriptor, user):
    """
    This method is responsible for updating provided component i.e. peer assessment
    :param descriptor: component to update
    :param user: user that is updating component
    """
    from cms.djangoapps.contentstore.views.item import StudioEditModuleRuntime

    descriptor.xmodule_runtime = StudioEditModuleRuntime(user)
    modulestore().update_item(descriptor, user.id)


def calculate_date_by_delta(date, source_date, destination_date):
    """
    This method is used to compute a date with a delta based on the difference of source_date and date
    and adding that delta to the destination date
    :param date: date for which delta is to be calculated
    :param source_date: date from which delta is to be calculated
    :param destination_date: date into which delta is to be added
    """
    date_delta = source_date - date
    return destination_date - date_delta
