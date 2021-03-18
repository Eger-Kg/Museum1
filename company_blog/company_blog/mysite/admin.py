from django.contrib import admin
from .models import Incident, Advertisement, AdvertisementImage, Commentary
# Register your models here.


class AdImageInline(admin.TabularInline):
    model = AdvertisementImage
    fields = ('image', 'description')


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    inlines = [AdImageInline, ]


admin.site.register(Incident)

admin.site.register(Commentary)
