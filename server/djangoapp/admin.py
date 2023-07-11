from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 4
# CarModelInline class

class CarModelAdmin(admin.ModelAdmin):
    search_fields = ['name']

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)

# Register models here
