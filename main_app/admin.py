from django.contrib import admin

# Register your models here.
from .models import imdbPopMovie, imdbTopMovie, imdbTopTv, imdbPopTv
# Register your models here.
admin.site.register(imdbPopMovie)
admin.site.register(imdbTopMovie)
admin.site.register(imdbTopTv)
admin.site.register(imdbPopTv)
