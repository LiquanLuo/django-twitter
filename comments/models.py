from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User

from likes.models import Like
from tweets.models import Tweet


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete= models.SET_NULL,null=True,)
    tweet = models.ForeignKey(Tweet,on_delete=models.SET_NULL,null=True)
    content = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        index_together = [["tweet", "created_at"],]
        ordering = ('tweet', '-created_at')

    @property
    def like_set(self):
        return Like.objects.filter(
            content_type = ContentType.objects.get_for_model(Comment),
            object_id = self.id,
        ).order_by('-created_at')

    def __str__(self):
        return f'id: {self.id} ' \
               f'user: {self.user}, ' \
               f'tweet: {self.tweet}, ' \
               f'content: {self.content}, ' \
               f'created_at: {self.created_at}'


