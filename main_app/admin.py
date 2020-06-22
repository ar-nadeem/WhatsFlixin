from django.contrib import admin

# Register your models here.
from .models import PopularMovie
from .models import TopMovie
# Register your models here.
admin.site.register(PopularMovie)
admin.site.register(TopMovie)
