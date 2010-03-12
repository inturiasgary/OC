from django.forms import ModelForm
from models import GalleryPage

class GalleryPageForm(ModelForm):
    class Meta:
            model = GalleryPage