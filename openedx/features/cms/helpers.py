from xmodule.course_module import CourseFields
from courseware.courses import get_course_by_id
from cms.djangoapps.contentstore.views.item import _save_xblock
from openedx.features.course_card.helpers import initialize_course_settings


def apply_post_rerun_creation_tasks(source_course_key, destination_course_key, user):
    # initialize course custom settings
    initialize_course_settings(source_course_key, destination_course_key)

    re_run = get_course_by_id(destination_course_key)

    # if re run has the default start date, it was created from old flow
    if re_run.start == CourseFields.start.default:
        return

    source_course = get_course_by_id(source_course_key)

    set_rerun_course_module_dates(source_course, re_run, user)


def set_rerun_course_module_dates(source_course, re_run, user):
    source_course_start_date = source_course.start
    re_run_start_date = re_run.start

    source_course_sections = source_course.get_children()
    re_run_sections = re_run.get_children()
    source_course_subsections = [sub_section for s in source_course_sections for sub_section in s.get_children()]
    re_run_subsections = [sub_section for s in re_run_sections for sub_section in s.get_children()]

    source_course_sections.extend(source_course_subsections)
    re_run_sections.extend(re_run_subsections)

    # setting release and due dates for sections and subsections
    for source_xblock, re_run_xblock in zip(source_course_sections, re_run_sections):
        meta_data = {}

        start_date_delta = source_course_start_date - source_xblock.start
        meta_data['start'] = re_run_start_date - start_date_delta

        if source_xblock.due:
            due_date_delta = source_course_start_date - source_xblock.due
            meta_data['due'] = re_run_start_date - due_date_delta

        _save_xblock(user, re_run_xblock, metadata=meta_data)
