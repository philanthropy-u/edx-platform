from django.contrib.auth.models import User

from xmodule.course_module import CourseFields
from courseware.courses import get_course_by_id
from openedx.features.course_card.helpers import initialize_course_settings

import dateutil.parser
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
    set_rerun_course_module_dates(source_course, re_run, user)


def set_rerun_course_module_dates(source_course, re_run, user):
    """
    This method is responsible for updating all section and subsection start and due dates for the re-run
    according to source course. This is achieved by calculating the delta between a source section/subsection's
    relevant date and start date, and then adding that delta to the start_date of the re-run course.

    """
    from cms.djangoapps.contentstore.views.item import _save_xblock

    source_course_start_date = source_course.start
    re_run_start_date = re_run.start

    source_course_sections = source_course.get_children()
    re_run_sections = re_run.get_children()
    source_course_subsections = [sub_section for s in source_course_sections for sub_section in s.get_children()]
    re_run_subsections = [sub_section for s in re_run_sections for sub_section in s.get_children()]

    source_course_sections.extend(source_course_subsections)
    re_run_sections.extend(re_run_subsections)

    set_ora_dates(re_run_subsections, source_course_start_date, re_run_start_date, user)

    # setting release and due dates for sections and subsections
    for source_xblock, re_run_xblock in zip(source_course_sections, re_run_sections):
        meta_data = {}

        start_date_delta = source_course_start_date - source_xblock.start
        meta_data['start'] = re_run_start_date - start_date_delta

        if source_xblock.due:
            due_date_delta = source_course_start_date - source_xblock.due
            meta_data['due'] = re_run_start_date - due_date_delta

        _save_xblock(user, re_run_xblock, metadata=meta_data)


def set_ora_dates(re_run_subsections, source_course_start_date, re_run_start_date, user):
    """
    This method is responsible for updating all dates in ORA i.e submission, start, due etc, for
    the re-run according to source course. This is achieved by calculating new dates for ORA based
    on delta value.
    :param re_run_subsections: list of subsection in a (re-run) course
    :param source_course_start_date: course start date of source course
    :param re_run_start_date: course start date of re-run course
    :param user: user that created this course
    """
    def update_date_by_delta(date_to_update):
        """
        Method to calculate new dates for ORA, on re-run, according to previous values. The delta
        is calculated from course start date of source course and re-run course. Delta is then
        added to previous dates in ORA.
        :param date_to_update:
        :return: new date string
        """
        date_to_update = dateutil.parser.parse(date_to_update)
        date_delta = source_course_start_date - date_to_update
        return (re_run_start_date - date_delta).strftime('%Y-%m-%dT%H:%M:%S%z')

    # flat sub-sections to the level of components and pick ORA only
    re_run_ora_list = [component for subsection in re_run_subsections for unit in
                  subsection.get_children() for component in unit.get_children() if
                  component.category == 'openassessment']

    for ora in re_run_ora_list:
        is_dirty = False
        if ora.submission_start and ora.submission_start != DEFAULT_START:
            is_dirty = True
            ora.submission_start = update_date_by_delta(ora.submission_start)
        if ora.submission_due and ora.submission_due != DEFAULT_DUE:
            is_dirty = True
            ora.submission_due = update_date_by_delta(ora.submission_due)
        for assessment in ora.rubric_assessments:
            if 'start' in assessment and assessment['start'] and assessment['start'] != DEFAULT_START:
                is_dirty = True
                assessment['start'] = update_date_by_delta(assessment['start'])
            if 'due' in assessment and assessment['due'] and assessment['due'] != DEFAULT_DUE:
                is_dirty = True
                assessment['due'] = update_date_by_delta(assessment['due'])
        # If all dates in ORA are default then no need to update it during re-run process
        if is_dirty:
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
