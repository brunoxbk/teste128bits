from django.db import models
from django.utils.translation import ugettext_lazy as _


class People(models.Model):
    name = models.CharField(
        _('Name'), max_length=80, blank=False, null=False)
    photo = models.URLField(
        _('Photo'), max_length=80, blank=False, null=False)
    age = models.IntegerField(_("Age"), blank=False, null=False)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    changed = models.DateTimeField(_('Changed'), auto_now=True)

    class Meta:
        ordering = ['-created']
        get_latest_by = "-created"

    def __str__(self):
        return "%s" % (self.name)
