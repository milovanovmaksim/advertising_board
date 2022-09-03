from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from sorl.thumbnail.admin import AdminImageMixin

from .models import Category, Tag, Ad, Picture, AdType


def archive_ad(modeladmin, request, queryset):
    change_type_ad(queryset, type_ad=AdType.archived)


def unarchive_ad(modeladmin, request, queryset):
    change_type_ad(queryset, type_ad=AdType.not_archived)


def change_type_ad(queryset, type_ad):
    for ad in queryset:
        ad.type_ad = type_ad
        ad.save()


archive_ad.short_description = 'Архивировать вабранные объявления'
unarchive_ad.short_description = 'Разархивировать выбранные объявления'


class FlatpageForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = '__all__'


class FlatPageNewAdmin(FlatPageAdmin):
    form = FlatpageForm


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    prepopulated_fields = {'slug': ('title', )}
    list_display_links = ('id', 'title')


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', )
    prepopulated_fields = {'slug': ('title', )}


class ImageAdInline(AdminImageMixin, admin.TabularInline):
    model = Picture


class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'seller',
                    'created_at', 'updated_at', 'type_ad')
    list_display_links = ('id', 'title', )
    search_fields = ('title', 'category__title', 'tags__title')
    list_filter = ['tags', 'category', 'created_at']
    readonly_fields = ('created_at', )
    inlines = [ImageAdInline]
    actions = [archive_ad, unarchive_ad]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ad, AdAdmin)

# flatpages
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageNewAdmin)
