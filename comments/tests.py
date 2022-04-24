from testing.testcases import TestCase
from .models import Comment

class CommentTests(TestCase):
    def setUp(self) -> None:
        self.user1 = self.create_user('liquan', 'liquan@gg.com', '12345678')
        self.tweet = self.create_tweet(self.user1)
        self.comment = self.create_comment(self.user1, self.tweet)
        self.user2 = self.create_user('liquan2', "adfsdf@gg.com","ddddd")

    def test_like_set(self):
        # no like at the beginning
        self.assertEqual(len(self.comment.like_set), 0)

        # successfully like a comment
        self.create_like(self.user1, self.comment)
        self.assertEqual(len(self.comment.like_set), 1)

        # like the same comment, it won't change the anything
        self.create_like(self.user1, self.comment)
        self.assertEqual(len(self.comment.like_set), 1)

        # someone else like the same comment, the count increase
        self.create_like(self.user2, self.comment)
        self.assertEqual(len(self.comment.like_set), 2)





