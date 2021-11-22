from django.contrib import admin
from .models import Genre, Movie
from embed_video.admin import AdminVideoMixin

# Register your models here.



# class MovieAdmin(AdminVideoMixin, admin.ModelAdmin):
#     list_display = ('title', 'video')

# admin.site.register(MovieAdmin)
admin.site.register(Genre)
admin.site.register(Movie)