import time
import datetime
import os
from dotenv import dotenv_values

from account_handler import Account


def getDaysMidVacation(today):
    """
    Find out if the mid year vacations have already passed, and return the days until it starts.

    :param today: Today's date
    :type today: datetime object
    """

    # Date that the mid year vacation starts.
    midStart = datetime.datetime.fromisoformat(custom_dotenv["MIDYEAR_START"])
    midEnd = datetime.datetime.fromisoformat(custom_dotenv["MIDYEAR_END"])

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

    # Date that the end of the year vacation starts.
    endDay = datetime.datetime.fromisoformat(custom_dotenv["ENDYEAR_START"])

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

# Startup message
print("Starting the bot program...")

# Load the custom environment variables from the dotenv file.
custom_dotenv = dotenv_values(".env")

# Assert that the environment variables are properly set. Otherwise, the program will
# not function properly.

environment_variables = ["CONSUMER_KEY",
                         "CONSUMER_SECRET",
                         "BEARER",
                         "ACCESS_TOKEN",
                         "ACCESS_TOKEN_SECRET",
                         "MIDYEAR_START",
                         "MIDYEAR_END",
                         "ENDYEAR_START",
                         "DEBUG_MODE",
                         "TIME_START_TWEET",
                         "TIME_DELTA_TWEET"]

for variable in environment_variables:
    assert custom_dotenv[variable]

print("Environment variables are OK.")

# Store the user specified account environment variables
consumer_key = (custom_dotenv["CONSUMER_KEY"], custom_dotenv["CONSUMER_SECRET"])
bearer = custom_dotenv["BEARER"]
access_token = (custom_dotenv["ACCESS_TOKEN"], custom_dotenv["ACCESS_TOKEN_SECRET"])

# Create the account object using said variables
bot_account = Account(consumer_key, bearer, access_token)

print("Account object created.")
print("Starting tweet loop...\n")

# Start the bot script
while True:
    # Update the environment variables
    custom_dotenv = dotenv_values(".env")
    
    dateToday = datetime.datetime.today()
    lastText = bot_account.get_last_tweet_text()
    print("\nLast tweet: ", lastText)

    hour_sp = (datetime.datetime.utcnow() - datetime.timedelta(hours=3)).hour
    last_delta = post_delta(bot_account)

    print("Hours since last post:", last_delta)
    print("Current time in SP:", hour_sp)

    # If it has been more than the specified amount of hours since the last post, and it is over the specified
    # tweet start time in Sao Paulo, execute the tweet routine.
    # Suggested values are 13 hours for TIME_DELTA_TWEET, and 8 a.m. for TIME_START_TWEET.
    if last_delta >= int(custom_dotenv["TIME_DELTA_TWEET"]) and hour_sp >= int(custom_dotenv["TIME_START_TWEET"]):
        passedMidYear, currentDelta = getDaysMidVacation(dateToday)

        if passedMidYear:
            currentDelta = getDaysEndVacation(dateToday)
            tweet = compose_tweet(currentDelta, "fim de ano")
        else:
            tweet = compose_tweet(currentDelta, "meio de ano")

        if custom_dotenv["DEBUG_MODE"].lower() == "true":
            print("Composed tweet: ", tweet)
            time.sleep(5)
            continue

        if lastText != tweet:
            bot_account.tweet(tweet)
            print("Tweeted: ", tweet)

    time.sleep(3600 / 2)
