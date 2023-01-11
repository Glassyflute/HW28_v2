from django.contrib import admin

# Register your models here.
from ads.models import Ad, Category, Location, AdUser, Selection

admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(AdUser)
admin.site.register(Selection)


