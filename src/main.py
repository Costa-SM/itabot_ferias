import time
import datetime

from account_handler import Account


def getDaysMidVacation(today):
    """
    Find out if the mid year vacations have already passed, and return the days until it starts.

    :param today: Today's date
    :type today: datetime object
    """
    # 2021 Mid-year Vacation: July 9 - July 30

    # Date that the mid year vacation starts.
    midStart = datetime.datetime.fromisoformat("2021-07-09")
    midEnd = datetime.datetime.fromisoformat("2021-07-30")

    if (midStart - today).days + 1 > 0:
        return False, ((midStart - today).days + 1)

    elif (midStart - today).days + 1 <= 0 and (midEnd - today).days + 1 >= 0:
        return False, -1

    else:
        return True, -1


def getDaysEndVacation(today):
    """
    Find out if the end of the year vacations have already passed, and return the days until it starts.

    :param today: Today's date
    :type today: datetime object
    """
    # 2021 End-of-the-year vacation: December 13

    # Date that the end of the year vacation starts.
    endDay = datetime.datetime.fromisoformat("2021-12-13")

    return (endDay - today).days + 1


def compose_tweet(days, vacation):
    """
    Composes the tweet that will be sent to the API.

    :param days: Number of days until the next vacation.
    :type days: int
    :param vacation: String that connects the tweet's sentence. Either "meio de ano" or "fim de ano".
    :type vacation: str
    """

    if days <= 0 or vacation == "holiday":
        return "Boas férias!"
    elif days == 1:
        return "Falta 1 dia até as férias de " + vacation + " do ITA!"
    else:
        return "Faltam " + str(days) + " dias até as férias de " + vacation + " do ITA!"


def post_delta(account):
    """
    Returns the number of hours since the last tweet has been made.
    :param account: Account object for the bot
    :type account: Account object
    :rtype: float
    """
    lastPost = account.get_last_tweet_date()
    currentUTC = datetime.datetime.utcnow()

    time_delta = currentUTC - lastPost

    return (time_delta.seconds / 3600) + 24 * time_delta.days


#############################################################################################################################
# ---------------------------------------------------------------------------------------------------------------------------#
#############################################################################################################################

consumer_key = ("CONSUMER_KEY", "CONSUMER_SECRET")
bearer = "BEARER"
access_token = ("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")

bot_account = Account(consumer_key, bearer, access_token)

# Start the bot script
while True:
    dateToday = datetime.datetime.today()
    lastText = bot_account.get_last_tweet_text()

    hour_sp = (datetime.datetime.utcnow() - datetime.timedelta(hours=3)).hour
    last_delta = post_delta(bot_account)

    print("Hours since last post:", last_delta)
    print("Current time in SP:", hour_sp)

    # If it has been more than 13 hours since the last post, and it is over 8am in Sao Paulo, execute the tweet routine.
    if last_delta >= 13 and hour_sp >= 8:
        passedMidYear, currentDelta = getDaysMidVacation(dateToday)

        if passedMidYear:
            currentDelta = getDaysEndVacation(dateToday)
            tweet = compose_tweet(currentDelta, "fim de ano")
        else:
            tweet = compose_tweet(currentDelta, "meio de ano")

        if lastText != tweet:
            bot_account.tweet(tweet)
            print("Tweeted: ", tweet)

    time.sleep(3600 / 2)
