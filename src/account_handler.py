import tweepy

class Account(object):
    """
    Represents the account that will be used with the Twitter API.
    """    
    def __init__(self, consumerkey, bearer, accesskey):
        """
        Prepares the account for use with the Twitter API via Tweepy.
        :param consumerkey: Tuple containing the Consumer Key and Consumer Key Secret.
        :type consumerkey: tuple
        :param bearer: String containing the bearer for the account.
        :type bearer: str
        :param accesskey: Tuple containing the Access Token and Access Token Secret. 
        :type accesskey: tuple
        """

        self.consumer_key = consumerkey
        self.bearer = bearer
        self.access_key = accesskey
        
        self.auth = tweepy.OAuthHandler(self.consumer_key[0], self.consumer_key[1])
        self.auth.set_access_token(self.access_key[0], self.access_key[1])
        self.api = tweepy.API(self.auth)


    def get_homepage_tweets(self):
        """
        Gets the last 20 tweets presented in the account's main timeline (i.e. homepage).
        :rtype: list of status objects        
        """

        return self.api.home_timeline()

    def get_last_tweet_date(self):
        """
        Gets the last tweet from the account.
        :rtype: datetime object
        """

        return self.api.user_timeline()[0].created_at

    def get_last_tweet_text(self):
        """
        Gets the last tweet from the account.
        :rtype: str
        """

        return self.api.user_timeline()[0].text

    def tweet(self, tweetedText):
        """
        Tweets the specified string.
        :param: tweetedText: String that will be tweeted by the account.
        :type: tweetedText: str
        :rtype: none
        """

        self.api.update_status(tweetedText)