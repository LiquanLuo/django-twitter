from django.contrib.contenttypes.models import ContentType

from likes.models import Like


class LikeService(object):
    @classmethod
    def has_liked(cls, user, instance):
        if user.is_anonymous:
            return False
        return Like.objects.filter(
            user = user,
            content_type = ContentType.objects.get_for_model(instance.__class__),
            object_id = instance.id
        ).exists()