# ITA Vacation Bot

Bot that tweets the remaining days until the next vacation for the Aeronautics Institute of Technology graduate students.
Made using Tweepy and Dotenv libraries.

## Environment Variables

Data, such as the Twitter API tokens, and the starting and ending dates for vacations, are stored as environment variables. To set these, you must create a `.env` file inside the `src` folder, and set them accordingly. This is done to avoid storing sensitive information in source code, and to allow changes in variables during runtime.

The environment variables, and what they do, is as follows:

- `CONSUMER_KEY` - Consumer API Key set in the Twitter Developers Dashboard.
- `CONSUMER_SECRET` - Consumer API Secret set in the Twitter Developers Dashboard.
- `BEARER` - Bearer Authentication Token set in the Twitter Developers Dashboard.
- `ACCESS_TOKEN` - Access Authentication Token set in the Twitter Developers Dashboard.
- `ACCESS_TOKEN_SECRET` - Access Authentication Secret set in the Twitter Developers Dashboard.
- `MIDYEAR_START` - Date for the start of the midyear vacation. In `YYYY-MM-DD` format.
- `MIDYEAR_END` - Date for the end of the midyear vacation. In `YYYY-MM-DD` format.
- `ENDYEAR_START` - Date for the start of the end of the year vacation. In `YYYY-MM-DD` format.
- `DEBUG_MODE` - Setting this to "True" will enable Debug mode, in which the bot will not tweet the strings it creates. Setting it to "False", however, will allow the bot to tweet in the account.
- `TIME_START_TWEET` - Time of day from which the bot will start tweeting messages.
- `TIME_DELTA_TWEET` - Minimum amount of hours in between two consecutive tweets.

Below is a sample `.env` file:

```env
CONSUMER_KEY="X"
CONSUMER_SECRET="X"
BEARER="X"
ACCESS_TOKEN="X"
ACCESS_TOKEN_SECRET="X"
MIDYEAR_START="2022-07-09"
MIDYEAR_END="2022-07-30"
ENDYEAR_START="2022-12-15"
DEBUG_MODE="False"
TIME_START_TWEET="8"
TIME_DELTA_TWEET="13"
```
