from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Eleveur)
admin.site.register(Boeuf)
admin.site.register(DonneeBoeuf)
admin.site.register(Administrateur)
admin.site.register(CodeConnexionAdmin)