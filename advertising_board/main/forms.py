from django.forms import (inlineformset_factory, BaseInlineFormSet,
                          ModelForm)
from sorl.thumbnail import delete

from .models import Ad, Picture


class AdForm(ModelForm):

    class Meta:
        model = Ad
        fields = ('seller', 'title', 'description',
                  'category', 'tags', 'price', 'type_ad')


class BaseImageFormset(BaseInlineFormSet):

    def save(self, commit=True):
        self._delete_image_file()
        return super().save(commit=commit)

    def _delete_image_file(self):
        for form in self.forms:
            data = form.cleaned_data
            if data.get('DELETE'):
                try:
                    img_path = data.get('id').img.path
                    delete(img_path)
                except AttributeError:
                    pass


ImageFormset = inlineformset_factory(parent_model=Ad, model=Picture,
                                     extra=4, fields=('img',),
                                     formset=BaseImageFormset)
