from django.contrib import admin
from .models import Like
# Register your models here.

# admin.site.register(Like)
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    """
        If you don’t set list_display, the admin site will display a 
        single column that displays the __str__() representation of each object.
    """
    list_display = (
        'user',
        'content_type',
        'object_id',
        'content_object',
        'created_at',
    )
    list_filter = ('content_type','user',)
