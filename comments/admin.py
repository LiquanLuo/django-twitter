from django.contrib import admin
from .models import Comment
# Register your models here.

# admin.site.register(Tweet)
@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    """
        If you don’t set list_display, the admin site will display a 
        single column that displays the __str__() representation of each object.
    """
    list_display = (
        'id',
        'created_at',
        'user',
        'content',
        'tweet',
        'updated_at',
    )
