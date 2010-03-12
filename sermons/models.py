from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

class Pastor(models.Model):
    first_name  = models.CharField(_('First Name'), max_length=100)
    middle_name = models.CharField(_('Middle Name'), max_length=100, blank=True)
    last_name   = models.CharField(_('Last Name'), max_length=100)
    image       = models.ImageField(_('Image'), upload_to="images/", null=True, blank=True)
    slug        = models.SlugField(editable=False)

    def __unicode__(self):
        return (u'%s %s, %s' % (self.last_name, self.middle_name, self.first_name))

    @models.permalink
    def get_absolute_url(self):
        return ('sermons_by_pastor', [self.slug])

    class Meta:
        ordering            = ['last_name']
        verbose_name        = _('Pastor')
        verbose_name_plural = _('Pastors')

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify("%s %s" % (self.first_name, self.last_name))

        super(Pastor, self).save(**kwargs)


class Subject(models.Model):
    title   = models.CharField(_('Title'), max_length=100, unique=True)
    slug    = models.SlugField(editable=False)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('sermons_by_subject', [self.slug])

    class Meta:
        ordering            = ['title']
        verbose_name        = _('Subject')
        verbose_name_plural = _('Subjects')

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Subject, self).save(**kwargs)


class Attachment(models.Model):
    attach = models.FileField(_('File'), upload_to="uploads")

    def __unicode__(self):
        return self.attach.name


class Sermon(models.Model):
    title       = models.CharField(_('Title'), max_length=100)
    subject     = models.ManyToManyField(Subject, related_name="subject_sermons", verbose_name=_('Subjects'))
    excerpt     = models.CharField(_('Excerpt'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    pastor      = models.ForeignKey(Pastor, related_name="pastor_sermons", verbose_name=_('Pastor'))
    date        = models.DateField(_('Date'))
    attachment  = models.ManyToManyField(Attachment, related_name="attachment_sermons", verbose_name=_('Attachments'))
    slug        = models.SlugField(editable=False)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('sermon_by_slug', [self.slug])

    class Meta:
        ordering            = ['title','pastor']
        verbose_name        = _('Sermon')
        verbose_name_plural = _('Sermons')

    #TODO sermon's date can't be greater than current date
    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Sermon, self).save(**kwargs)
