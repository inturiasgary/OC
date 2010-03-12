from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

class Category(models.Model):
    title       = models.CharField(_('Title'), max_length=100, help_text=_('The title for the category'), unique=True)
    description = models.TextField(_('Description'), help_text=_('The description for the category'), blank=True)
    slug        = models.SlugField(editable=False)

    class Meta:
        ordering            = ["title"]
        verbose_name        = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('links_by_category', [self.slug])

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(**kwargs)


class Link(models.Model):
    title       = models.CharField(_('Title'), max_length=100, help_text=_('The title for the link'))
    description = models.TextField(_('Description'), help_text=_('The description for the link'), blank=True)
    url         = models.URLField(_('URL'), help_text=_('The URL represented by the link'), unique=True)
    category    = models.ForeignKey(Category, verbose_name=_('Category'), related_name="link_categories", help_text=_('The Categories for the link'))

    class Meta:
        ordering            = ["title"]
        verbose_name        = _('Link')
        verbose_name_plural = _('Links')

    def __unicode__(self):
        return ("%s,  %s" % (self.title, self.url))




