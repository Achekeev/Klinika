from django.contrib import admin
from .models import Works, Blogs, Asks, Feedback


@admin.register(Works)
class WorksAdmin(admin.ModelAdmin):
    list_display = ['opera', 'beforeopera', 'afteropera', 'name']
    list_filter = ['opera']
    fields = ('opera', 'beforeopera', 'afteropera', 'name')

    # readonly_fields = ['beforeopera', 'afteropera', 'name']

    class Meta:
        verbose_name = 'Работы'
        verbose_name_plural = 'Работы'


@admin.register(Blogs)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['name_blog']
    fields = ('name_blog', 'photo', 'blog', 'url_blog')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блог'


@admin.register(Asks)
class AsksAdmin(admin.ModelAdmin):
    list_display = ['fio', 'phone', 'mail', 'date']
    readonly_fields = ('fio', 'phone', 'mail', 'message', 'date')

    class Meta:
        verbose_name = 'Вопросы'
        verbose_name_plural = 'Вопросы'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    readonly_fields = ('name', 'photo', 'feedback')