from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Claims)
admin.site.register(Item)
admin.site.register(Keywords)