# human-simulator

Twitter bot that uses a Markov chain to train on a person's messages.

The bot is trained on a dataset of a user's messages in a Telegram chat group and creates
a Markov chain to store the way the user talks. The bot produces random output
from the Markov chain and tweets it.

## Installation and Usage
1. Clone the repo to your computer and install the required dependencies.
    ```console
    git clone https://github.com/abhinavk99/human-simulator.git
    cd human-simulator
    pip install -r requirements.txt
    ```
2. Get your Telegram chat logs using [telegram-history-dump](https://github.com/tvdstaaij/telegram-history-dump).
3. Get your Twitter credentials for the account you want to tweet with. [This guide](https://www.digitalocean.com/community/tutorials/how-to-create-a-twitter-app) should help.
4. Make a file called `config.py` in the repo directory.
5. Copy/paste the below into the file.
    ```
    consumer_key = 'key'
    consumer_secret = 'secret'
    access_token = 'token'
    access_secret = 'secret'
    ```
6. Put your Twitter authentication information where it says to in config.py.
7. Run the bot.
    ```console
    python main.py
    ```
8. Enter the first name of the person you want to train the bot on.
9. Check your Twitter bot's profile to see the new tweets.
