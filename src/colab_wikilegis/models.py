# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from colab.accounts.models import User
from colab.plugins import helpers


BILL_STATUS_CHOICES = (
    ('draft', _('Draft')),
    ('published', _('Published')),
    ('closed', _('Closed'))
)

BILL_THEMES_CHOICES = (
    ('documento', _('Others')),
    ('adm-publica', _('Public Administration')),
    ('agropecuaria', _('Farming')),
    ('assistencia-social', _('Social Assistance')),
    ('cidades', _('Cities')),
    ('ciencia', _('Science')),
    ('comunicacao', _('Communication')),
    ('consumidor', _('Consumer')),
    ('cultura', _('Culture')),
    ('direito-e-justica', _('Law and Justice')),
    ('direitos-humanos', _('Human Rights')),
    ('economia', _('Economy')),
    ('educacao', _('Education')),
    ('esportes', _('Sports')),
    ('familia', _('Family')),
    ('industria', _('Industry')),
    ('institucional', _('Institutional')),
    ('meio-ambiente', _('Environment')),
    ('participacao_e_transparencia', _('Participation and Transparency')),
    ('politica', _('Policy')),
    ('previdencia', _('Foresight')),
    ('relacoes-exteriores', _('Foreign Affairs')),
    ('saude', _('Health')),
    ('seguranca', _('Security')),
    ('trabalho', _('Work')),
    ('transporte-e-transito', _('Transportation and Transit')),
    ('turismo', _('Tourism'))
)


class WikilegisBill(models.Model):

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    epigraph = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=255,
                              choices=BILL_STATUS_CHOICES, default='1')
    theme = models.CharField(max_length=255, choices=BILL_THEMES_CHOICES,
                             default='documento')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def get_url(self):
        prefix = helpers.get_plugin_prefix('colab_wikilegis', regex=False)
        return '/{}bill/{}'.format(prefix, self.id)

    def get_status(self):
        return self.get_status_display()

    def get_theme(self):
        return self.get_theme_display()

    def get_total_proposals(self):
        return self.segments.filter(original=False).count()


class WikilegisSegmentType(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)


class WikilegisSegment(models.Model):

    id = models.IntegerField(primary_key=True)
    bill = models.ForeignKey('WikilegisBill', related_name='segments')
    original = models.BooleanField(default=True)
    replaced = models.ForeignKey('self', related_name='substitutes',
                                 null=True, blank=True)
    parent = models.ForeignKey('self', related_name='children',
                               null=True, blank=True)
    type = models.ForeignKey('WikilegisSegmentType')
    number = models.PositiveIntegerField(default=0, null=True, blank=True)
    content = models.TextField()
    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(editable=False, auto_now=True)

    def get_segment_type(self):
        return self.type.name

    def get_bill(self):
        return self.bill.title

    def get_url(self):
        prefix = helpers.get_plugin_prefix('colab_wikilegis', regex=False)
        return '/{}bill/{}/segments/{}'.format(prefix, self.bill_id, self.id)


class WikilegisComment(models.Model):

    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    submit_date = models.DateTimeField()
    content_type = models.CharField(max_length=255)
    object_pk = models.IntegerField()
    comment = models.TextField()

    def get_author(self):
        return User.objects.get(pk=self.user_id).username

    def get_parent_object(self):
        parent_obj = None
        if self.content_type == 'segment':
            parent_obj = WikilegisSegment.objects.get(pk=self.object_pk)

        return parent_obj

    def get_segment(self):
        parent = self.get_parent_object()
        return parent.get_segment_type()

    def get_bill(self):
        parent = self.get_parent_object()
        return parent.bill.title

    def get_url(self):
        parent = self.get_parent_object()
        return '{}#c{}'.format(parent.get_url(), self.id)
