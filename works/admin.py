from django.contrib import admin
from .models import Works


@admin.register(Works)
class WorksAdmin(admin.ModelAdmin):
    list_display = ['opera', 'beforeopera', 'afteropera', 'name']
    list_filter = ['opera']
    fields = ('opera', 'beforeopera', 'afteropera', 'name')
    # readonly_fields = ['beforeopera', 'afteropera', 'name']

    class Meta:
        verbose_name = 'Работы'
        verbose_name_plural = 'Работы'
