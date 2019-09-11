from django.db import models
from django.utils.translation import ugettext_noop

from model_utils.models import TimeStampedModel
from .constants import CONVERSATIONALIST, TEAM_PLAYER


class Badge(models.Model):
    BADGE_TYPES = (
        (CONVERSATIONALIST['key'], ugettext_noop(CONVERSATIONALIST['value'])),
        (TEAM_PLAYER['key'], ugettext_noop(TEAM_PLAYER['value']))
    )

    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    threshold = models.IntegerField(blank=False, null=False)
    type = models.CharField(max_length=100, blank=False, null=False, choices=BADGE_TYPES)
    image = models.CharField(max_length=255, blank=False, null=False)
    date_created = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.name)
