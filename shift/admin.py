from django.contrib import admin
from .models import Schedule , Shop_config,Shop_config_day


# class ScheduleAdmin(admin.ModelAdmin):
#     )
#     list_display = ('shops','date')


admin.site.register(Schedule)
admin.site.register(Shop_config)
admin.site.register(Shop_config_day)
