# Crypto Discord Bot (aka Nigel)

## About
Nigel is a Discord bot that will keep you up-to-date on the exchange rates (in USD) for any cryptocurrency. 

Built with Python and the Alpha Vantage API. Hosted on Heroku.

### Features
* Updates its status every 5 minutes to include the current exchange rate
* Notifies you whenever the current exchange rate is above or below user-specified thresholds

Due to API limitations (500 requests/day), the bot can only keep track of one cryptocurrency.

**Fun fact:** I decided to name the bot Nigel, after the [humble stockbroker from Neopets](https://bookofages.jellyneo.net/characters/411/). The site was a big part of my childhood, and it was my first exposure to how the stock market works.

## Commands
| Command       | Parameters        |  Description    |
| ------------- | ----------------- | --------------- |
| **!help**     |                   | Show all commands
| **!info**     |                   | Show your crypto and your range
| **!rate**     |                   | Show current exchange rate for your
| **!setcode**  | `<code>`          | Set the crypto code you want to
| **!setrange** | `<min> <max>`     | Set the range of rates at which you want to be notified

## Self-Hosting
0. Create a Discord bot and invite it to your server. Follow the steps listed [here](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/), up to (but not including) "How to Code a Basic Discord Bot with the discord.py Library". You should have a Discord token.
1. Claim your Alpha Vantage API key from [here](https://www.alphavantage.co/support/#api-key).
3. Clone this repo.
4. Create a `.env` file at the root of the project folder to include the following, replacing everything in the angled brackets:
```
DISCORD_TOKEN=<YOUR DISCORD TOKEN>
AV_API_KEY=<YOUR ALPHA VANTAGE API KEY>
CHANNEL_ID=<CHANNEL ID IN YOUR SERVER WHERE THE BOT WILL POST NOTIFICATIONS>
```
5. Run: `python bot/main.py`
6. To run continuously, follow the steps listed [here](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/), under "How to Set Up the Bot to Run Continuously".

## First Use
After adding the bot to your Discord server:
1. Type `!setcode <code>` to set the cryptocurrency you want to follow. The code should be the 3 or 4 letter symbol (i.e. DOGE, BTC). The default code is set to DOGE.
2. Type `!setrange <min> <max>` to set the minimum and maximum rates for which you want to be notified. If the exchange rate drops below the min or rises above the max, the bot will send a message. The default range is -1 to -1, so the bot will not send any notifcations at first.

## Screenshots
### Setting Up
![Commands](./screenshots/commands.png)

### Bot's Status
![Status](./screenshots/status.png)
