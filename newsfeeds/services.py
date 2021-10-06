from friendships.services import FriendshipService
from newsfeeds.models import Newsfeed


class NewsFeedService(object):
    @classmethod
    def fanout_to_followers(cls, tweet):
        # wrong version
        # Do not put database queries in for loop, it will be very slow
        # for follower in FriendshipService.get_followers(tweet.user):
        #     NewsFeed.objects.create(
        #         user=follower,
        #         tweet=tweet,
        #     )


        # correct version , bulk create will put all inserts into one query
        # INSERT
        # INTO
        # `newsfeeds_newsfeed`(`user_id`, `tweet_id`, `created_at`)
        # VALUES(4, 18, '2021-10-05 11:27:39.655146'), (3, 18, '2021-10-05 11:27:39.655199'), (
        # 5, 18, '2021-10-05 11:27:39.655224'), (1, 18, '2021-10-05 11:27:39.655246')
        newsfeeds = [
            Newsfeed(tweet = tweet, user = follower)
            for follower in FriendshipService.get_followers(tweet.user)
        ]
        newsfeeds.append(Newsfeed(tweet = tweet, user = tweet.user))
        Newsfeed.objects.bulk_create(newsfeeds)


