# TODO:
# set up github actions?
# run a new build on heroku everytime settings.json is changed

import discord
from discord.ext import tasks
import os
import requests
import json
from numbers import Number
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
AV_API_KEY = os.getenv('AV_API_KEY')
CHANNEL_ID = os.getenv('CHANNEL_ID')

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    check_rates.start()

# Pulls current exchange rate from Alpha Vantage API every 5 minutes
# Updates status to include the crypto code and current rate
# Sends a message to the channnel if current rate is below min or above max rates
@tasks.loop(minutes=5)
async def check_rates():
    channel = client.get_channel(CHANNEL_ID)

    # get current rate
    curr_rate = get_curr_rate()

    # update bot's status to display current rate
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name=crypto_code + ' @ ' + str(curr_rate)
        )
    )

    # if min_rate and max_rate not yet configured, don't do anything
    if min_rate == -1.0 and max_rate == -1.0:
        pass

    # send message to channel if current rate is below min_rate or above max_rate
    elif curr_rate <= min_rate and curr_rate > 0.0:
        await channel.send(
            f'📉 **DIP!** Current exchange rate for {crypto_code} is **{curr_rate}**!'
        )
    elif curr_rate >= max_rate and curr_rate > 0.0:
        await channel.send(
            f'📈 **SPIKE!** Current exchange rate for {crypto_code} is **{curr_rate}**!'
        )

# Listens for and handles commands: !rate, !info, !setcode, !setrange, !help
@client.event
async def on_message(message):
    global crypto_code, min_rate, max_rate

    if message.author == client.user:
        return

    msg = message.content

    # Displays the current exchange rate
    if msg.startswith('!rate'):
        rate = get_curr_rate()
        await message.channel.send(
            f"💸 Current exchange rate for {crypto_code} is **{rate}**!"
        )

    # Displays the current crypto code and range (min and max rates)
    if msg.startswith('!info'):
        await message.channel.send(
            f"> Cryptocurrency: **{crypto_code}**\n> Range: From **{min_rate}** to **{max_rate}**\nYou can change either of these with `!setcode` or `!setrange`, respectively."
        )
    
    # Sets the code for the cryptocurrency the user wants to follow
    if msg.startswith('!setcode'):
        code = msg.split('!setcode', 1)[1].strip()
        currency_name = get_currency_name(code)
        if currency_name:
            set_crypto_code(code)
            await message.channel.send(
                f"👍 Okay, boss! I'll send you notifications about **{currency_name}**, aka **{crypto_code}**!"
            )
        else:
            await message.channel.send(
                f"❌ Hmmm... Sorry, I don't know this code. Try entering a different one. Make sure you're entering the symbol, which is only 3 or 4 letters."
            )

    # Sets the min and max rates at which the user wants to be notified
    if msg.startswith('!setrange'):
        range = msg.split('!setrange', 1)[1].strip().split()
        if len(range) != 2 or any(c.isalpha() for c in range[0]) or any(c.isalpha() for c in range[1]):
            await message.channel.send(
                f"❌ Slow down, you need to enter **2 numbers** (minimum and maximum) to set a range!"
            )
        else:
            min = float(range[0])
            max = float(range[1])
            if min <= 0 or max <= 0:
                await message.channel.send(
                    f"❌ Whoa there, make sure you're entering 2 numbers that are **greater than 0**!"
                )
            elif min >= max:
                await message.channel.send(
                    f"❌ Hold up, make sure that the 1st number is **less than** the 2nd!"
                )
            else:
                set_rates(min, max)
                await message.channel.send(
                    f"👍 Got it! I'll do my best to notify you when the exchange rate drops below **{min_rate}** or rises above **{max_rate}**!"
                )
    
    if msg.startswith('!help'):
        await message.channel.send(
            "❗️ Need help? Here's what I can do for you.\n" +
            "```" +
            " !help - Show all commands\n" +
            " !info - Show your crypto and your range\n" +
            " !rate - Show current exchange rate for your crypto\n" +
            " !setcode <code> - Set the crypto code you want to follow\n" +
            " !setrange <min> <max> - Set the range of rates at which you want to be notified```"
        )

# Returns the current exchange rate for our cryptocurrency
def get_curr_rate():
    url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=" + crypto_code + "&to_currency=USD&apikey=" + AV_API_KEY
    response = requests.request("GET", url)
    data = response.json()
    try:
        curr_rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    except KeyError:
        curr_rate = -1.0
        print('KeyError Occurred')

    return curr_rate

# Given a code, returns the full currency name if it is valid; None otherwise
def get_currency_name(code):
    url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=" + code + "&to_currency=USD&apikey=" + AV_API_KEY
    response = requests.request("GET", url)
    data = response.json()
    if 'Error Message' not in data:
        currency_name = data["Realtime Currency Exchange Rate"]["2. From_Currency Name"]
        return currency_name
    else:
        return None

# Gets crypto_code, min_rate, and max_rate from settings.json
def get_settings():
    with open('bot/settings.json', 'r') as openfile:
        # Reading from json file
        data = json.load(openfile)
    return data['crypto_code'], data['min_rate'], data['max_rate']

# Sets new crypto code
def set_crypto_code(new_code):
    global crypto_code, min_rate, max_rate

    crypto_code = new_code.upper()

    # Data to be written
    data = {
        "crypto_code": new_code,
        "min_rate": min_rate,
        "max_rate": max_rate
    }
    # Serializing json 
    json_object = json.dumps(data, indent = 4)
    # Writing to file
    with open("bot/settings.json", "w") as outfile:
        outfile.write(json_object)

# Sets new min and max rates
def set_rates(new_min, new_max):
    global crypto_code, min_rate, max_rate

    min_rate = new_min
    max_rate = new_max

    # Data to be written
    data = {
        "crypto_code": crypto_code,
        "min_rate": new_min,
        "max_rate": new_max
    }
    # Serializing json 
    json_object = json.dumps(data, indent = 4)
    # Writing to file
    with open("bot/settings.json", "w") as outfile:
        outfile.write(json_object)

# load settings
crypto_code, min_rate, max_rate = get_settings()

client.run(TOKEN)