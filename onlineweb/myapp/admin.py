from django.contrib import admin
from .models import donorregister,requests,bloodcamp

# Register your models here.
admin.site.register(donorregister)
admin.site.register(requests)

admin.site.register(bloodcamp)


