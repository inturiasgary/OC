from django.db import models
from pages.models import Page
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

class Gallery(models.Model):
    date_added = models.DateTimeField(_('date published'))
    title = models.CharField(_('title'), max_length=100, unique=True)
    title_slug = models.SlugField(_('title slug'), unique=True, help_text=_('A "slug" is a unique URL-friendly title for an object.'))
    description = models.TextField(_('description'), blank=True)
    pictures = models.ManyToManyField('Picture', related_name='galleries', verbose_name=_('photos'), null=True, blank=True)

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')

    def __unicode__(self):
        return self.title

    def picture_count(self):
        return self.photos.all().count()

    picture_count.short_description = _('count')


class Picture(models.Model):
    title = models.CharField(_('title'), max_length=100, unique=True)
    title_slug = models.SlugField(_('slug'), unique=True, help_text=_('A slug is a unique URL-friendly title for an object.'))
    caption = models.TextField(_('caption'), blank=True)
    date_added = models.DateTimeField(_('date added'))
    image = models.ImageField(_('File Image'),upload_to ='pictures', help_text=_('Provide an exactly picture sized otherwise will be cropped.'))

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _("picture")
        verbose_name_plural = _("pictures")

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title_slug is None:
            self.title_slug = slugify(self.title)
        super(Picture, self).save(*args, **kwargs)

class GalleryPage(models.Model):
    page = models.ForeignKey(Page)
    gallery = models.ForeignKey(Gallery)
