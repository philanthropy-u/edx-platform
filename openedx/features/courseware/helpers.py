from logging import getLogger

from django.conf import settings
from django.core.urlresolvers import reverse

from xmodule.modulestore.django import modulestore

log = getLogger(__name__)

base_url = settings.LMS_ROOT_URL


def get_nth_chapter_link(course, chapter_index=0):
    course_chapters = modulestore().get_items(
        course.id,
        qualifiers={'category': 'course'}
    )
    if not course_chapters:
        log.info("%s Course dont have any chapters", course.display_name)

    chapter = course_chapters[0].children[chapter_index]
    subsection = modulestore().get_item(chapter).children[0]

    course_target = reverse(
        'courseware_section',
        args=[course.id.to_deprecated_string(),
              chapter.block_id,
              subsection.block_id]
    )

    return base_url + course_target


def get_my_account_link(course_id):
    my_account_url = reverse('update_account_settings')
    url_target = '{my_account_url}?course_id={course_id}'.format(my_account_url=my_account_url, course_id=course_id)
    return base_url + url_target
