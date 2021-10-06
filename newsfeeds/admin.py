from django.contrib import admin
from .models import Newsfeed
# Register your models here.

@admin.register(Newsfeed)
class NewsfeedAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    """
        If you don’t set list_display, the admin site will display a 
        single column that displays the __str__() representation of each object.
    """
    list_display = (
        'user',
        'tweet',
        'created_at',
    )

