from django.contrib import admin
from events.models import CategoryModel, EventModel
# Register your models here.

admin.site.register(EventModel)
admin.site.register(CategoryModel)
