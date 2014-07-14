from django.contrib import admin
from forum.models import Category, Forum, Thread

class ForumInline(admin.StackedInline):
    model = Forum

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ForumInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Thread)
