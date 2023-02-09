from friendships.models import Friendship


class FriendshipService(object):

    @classmethod
    def get_followers(cls, user):
        '''
        wrong version 1
        It will lead N + 1 Queries
        filter out all the friendship is 1 query
        FOR loop to get all the from_user will cost N queries
        NEVER USE FOR LOOP TO DO QUERY!
        '''
        # friendships = Friendship.objects.filter(to_user = user)
        # return [friendship.from_user for friendship in friendships]

        '''
        wrong version 2
        It will create JOIN statement, 
        
        FROM `friendships_friendship` 
        LEFT OUTER JOIN `auth_user` T3 
        ON (`friendships_friendship`.`from_user_id` = T3.`id`) 
        
        JOIN statement is not allowed in large web system because it will become really slow
        '''
        # friendships = Friendship.objects.filter(
        #     to_user = user
        # ).select_related('from_user')
        # return [friendship.from_user for friendship in friendships]

        '''
        correct version 1
        get user_id first
        use IN QUERY
        
        FROM `auth_user` 
        WHERE `auth_user`.`id` IN (4, 3, 5)
 
        '''
        # friendships = Friendship.objects.filter(to_user=user)
        # follower_ids = [friendship.from_user_id for friendship in friendships]
        # followers = User.objects.filter(id__in=follower_ids)
        #return followers

        # queries that are executed is exactly same as correct version 1
        friendships = Friendship.objects.filter(
            to_user = user
        ).prefetch_related('from_user')
        return [friendship.from_user for friendship in friendships]

