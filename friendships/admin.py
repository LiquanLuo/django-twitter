from django.contrib import admin
from .models import Friendship
# Register your models here.

# admin.site.register(Friendship)
@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    """
        If you don’t set list_display, the admin site will display a 
        single column that displays the __str__() representation of each object.
    """
    list_display = (
        'from_user',
        'to_user',
        'created_at',
    )
