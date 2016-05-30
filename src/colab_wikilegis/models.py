from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


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
    number = models.PositiveIntegerField()
    content = models.TextField()


class WikilegisComment(models.Model):

    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    submit_date = models.DateTimeField()
    content_type = models.CharField(max_length=255)
    object_pk = models.IntegerField()
    comment = models.TextField()
