from django.contrib import admin

from .models import Biding, Comments, Listing, User, Watch

# Register your models here.
admin.site.register(Listing)
admin.site.register(Biding)
admin.site.register(Comments)
admin.site.register(Watch)
admin.site.register(User)
