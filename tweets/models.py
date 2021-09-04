from django.db import models
from django.contrib.auth.models import User
from utils.time_helpers import utc_now

class Tweet(models.Model):
    user = models.ForeignKey(User,on_delete= models.SET_NULL,null=True,)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def hours_to_now(self):
        # datetime.now does not have timezone info, we need to add it
        return (utc_now() - self.created_at).seconds // 3600

    def __str__(self):
        return f'user: {self.user}, content: {self.content}, created_at: {self.created_at}'


