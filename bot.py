import discord
from discord.ext import tasks
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
AV_API_KEY = os.getenv('AV_API_KEY')

client = discord.Client()

crypto_code = 'DOGE'
min_rate = -1.0
max_rate = -1.0
count = 0

# Returns the current exchange rate for our cryptocurrency
def get_curr_rate():
    url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=" + crypto_code + "&to_currency=USD&apikey=" + AV_API_KEY
    response = requests.request("GET", url)
    data = response.json()
    curr_rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
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

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    check_rates.start()

@client.event
async def on_message(message):
    global crypto_code

    if message.author == client.user:
        return

    msg = message.content

    # Displays the current exchange rate
    if msg.startswith('!rate'):
        rate = get_curr_rate()
        await message.channel.send(
            f"💸 The current exchange rate for {crypto_code} is **{rate}**!"
        )
    
    # Sets the code for the cryptocurrency the user wants to follow
    if msg.startswith('!setcode'):
        code = msg.split('!setcode', 1)[1].strip()
        # print(code)
        currency_name = get_currency_name(code)
        if currency_name:
            crypto_code = code.upper()
            await message.channel.send(
                f"👍 Okay, boss! I'll send you notifications about **{currency_name}**, aka **{crypto_code}**!"
            )
        else:
            await message.channel.send(
                f"❌ Hmmm... Sorry, I don't know this code. Try entering a different one."
            )

    # Sets the min and max rates at which the user wants to be notified
    if msg.startswith('!setrange'):
        range = msg.split('!setrange', 1)[1].strip().split()
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
            min_rate = min
            max_rate = max
            await message.channel.send(
                f"👍 Got it! I'll do my best to notify you when the exchange rate drops below **{min_rate}** or raises above **{max_rate}**!"
            )

# @tasks.loop(seconds=5)
# async def check_rates():
#     curr_rate = get_curr_rate()
#     count += 1
#     await message.channel.send(
#         f'Count: {count}'
#         # f'The current exchange rate for **{current_code}** is **{current_exchange_rate}**!'
#     )

client.run(TOKEN)


'''
!prices <low> <high>
Sets the low and high threshold points at which the user wants to be notified
'''
# @bot.command(name='prices', help='Enter 1 low and 1 high number to be notified when the exchange rate crosses either limit')
# async def set_prices(ctx, low, high):



# if exchange_rate < low:
#     await ctx.send(
#         f'🔻 PRICE DROP! 🔻 The current exchange rate for DOGE is {exchange_rate}! Maybe buy?'
#     )
# elif exchange_rate > high:
#     await ctx.send(
#         f'🟢 PRICE SPIKE! 🟢 The current exchange rate for DOGE is {exchange_rate}! Maybe sell?'
#     )

# @bot.event
# async def send_alert(ctx):
#     if current_exchange_rate < low_limit:
#         ctx.send(
#             f'⬇️⬇️ **PRICE DROP!** The current exchange rate for **{current_code}** is **{current_exchange_rate}**!'
#         )
#     elif current_exchange_rate > high_limit:
#         ctx.send(
#             f'⬆️⬆️ **PRICE SPIKE!** The current exchange rate for **{current_code}** is **{current_exchange_rate}**!'
#         )


# @tasks.loop(seconds=10)
# async def check_rates(ctx):
#     curr_rate = get_curr_rate()
#     await ctx.send(
#         f'The current exchange rate for **{current_code}** is **{current_exchange_rate}**!'
#     )