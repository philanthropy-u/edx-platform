from django.db import models
from openedx.core.djangoapps.xmodule_django.models import CourseKeyField
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview


class CourseCard(models.Model):
    """
    These courses are used for representing course re-runs.
    @course_id: (string) id of the course. can be gotten through to_deprecated_string() method of CourseKey object
    organization: if given, it will make course card private for that organization
    is_enabled: whether to publish the course or not
    """

    class Meta:
        app_label = 'course_card'


    course_id = CourseKeyField(db_index=True, max_length=255, null=False)
    course_name = models.CharField(max_length=255, blank=True, null=True)
    is_enabled = models.BooleanField(default=False, null=False)

    def __unicode__(self):
        return '{}--{}'.format(self.course_name, unicode(self.course_id))

    def save(self, *args, **kwargs):
        course_overview = CourseOverview.objects.get(id=self.course_id)
        self.course_name = course_overview.display_name
        super(CourseCard, self).save(*args, **kwargs)
