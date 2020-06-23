from django.contrib import admin

# Register your models here.
from .models import imdbPopularMovie
from .models import imdbTopMovie
# Register your models here.
admin.site.register(imdbPopularMovie)
admin.site.register(imdbTopMovie)
