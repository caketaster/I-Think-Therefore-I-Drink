from django.contrib import admin
from .models import Post
from .models import Submit_form
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    summernote_fields = ('content')
    list_display = ('title', 'slug', 'status', 'created_on')
    search = ('title', 'ingredients')

@admin.register(Submit_form)
class PostAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content')
    list_filter = ('approved', 'created_on')
    search = ('name', 'email', 'ingredients')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

