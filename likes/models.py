from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User

class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )

    # https://docs.djangoproject.com/en/3.1/ref/contrib/contenttypes/#generic-relations
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('content_type', 'object_id', 'created_at'),)
        unique_together = (('user', 'content_type', 'object_id'),)

    def __str__(self):
        return f'user: {self.user} liked type: {self.content_type} id: {self.object_id} at time: {self.created_at}'


