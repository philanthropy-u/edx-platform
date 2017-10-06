import logging

from celery.exceptions import MaxRetriesExceededError
from celery.task import task  # pylint: disable=no-name-in-module, import-error

from common.lib.nodebb_client.client import NodeBBClient
from django.conf import settings

log = logging.getLogger('edx.celery.task')


@task(bind=True, default_retry_delay=settings.NODEBB_TASK_DELAY, max_retries=settings.NODEBB_TASK_MAX_TRIES)
def task_create_category_on_nodebb(self, course_name):
    status_code, response_body = NodeBBClient().categories.create(name=course_name)

    if status_code != 200:
        try:
            self.retry()
        except MaxRetriesExceededError:
            log.error(
                "Error: Can't create nodebb community for the given course %s due to %s" % (course_name, response_body)
            )
    else:
        log.info('Success: Community created for course %s' % course_name)


@task(bind=True, default_retry_delay=settings.NODEBB_TASK_DELAY, max_retries=settings.NODEBB_TASK_MAX_TRIES)
def task_join_group_on_nodebb(self, username, course_name):
    status_code, response_body = NodeBBClient().users.join(group_name=course_name, user_name=username)

    if status_code != 200:
        try:
            self.retry()

        except MaxRetriesExceededError:
            log.error('Error: Can not join the group, user (%s, %s) due to %s' % (course_name, username, response_body))
    else:
        log.info('Success: User have joined the group %s successfully' % course_name)
