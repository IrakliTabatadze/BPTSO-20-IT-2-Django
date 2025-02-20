from django.contrib import admin
from .models import Event, Category

# admin.site.register(Event)


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'max_attendees', 'category', 'create_date')
    search_fields = ('title', 'max_attendees')
    list_filter = ('max_attendees', 'category')
    ordering = ('-create_date',)


admin.site.register(Event, EventAdmin)
admin.site.register(Category)
