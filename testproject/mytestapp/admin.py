from django import forms
from django.core.files.storage import FileSystemStorage
from django.contrib import admin
from .models import News, NewsImages, Tags, NewTags, Anonymous, AnonymousFeedback
import time

class NewsImagesForm(forms.ModelForm):
    image = forms.FileField()

    class Meta:
        model = NewsImages
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            image = self.cleaned_data.get('image')
            if image:
                path = '../front/src/images'
                file_storage = FileSystemStorage(location=path)
                unix_time = int(time.time())
                image_name = file_storage.save(f'{unix_time}.jpg', image)
                instance.image = image_name
                instance.save()
        return instance

class NewsImagesInline(admin.TabularInline):
    model = NewsImages
    extra = 1
    form = NewsImagesForm

class NewTagsInline(admin.TabularInline):
    model = NewTags
    extra = 1

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'title', 'text')
    fields = ('date', 'title', 'text')
    readonly_fields = ['date']
    inlines = [NewsImagesInline, NewTagsInline]

    def tags(self, obj):
        return ", ".join([str(newtag.tag) for newtag in NewTags.objects.filter(news=obj)])

    def images(self, obj):
        return ", ".join([str(image.image) for image in NewsImages.objects.filter(news=obj)])
    
class TagsAdmin(admin.ModelAdmin):
    list_display = ('tag',)

class NewTagsAdmin(admin.ModelAdmin):
    list_display = ('tag', 'news')

class AnonymousAdmin(admin.ModelAdmin):
    list_display = ('id', 'token')

class AnonymousFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'anonymous', 'status', 'news', 'rate')

admin.site.register(News, NewsAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(NewTags, NewTagsAdmin)
admin.site.register(Anonymous, AnonymousAdmin)
admin.site.register(AnonymousFeedback, AnonymousFeedbackAdmin)
