import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands

import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

low_limit = 0.1
high_limit = 1.0
current_code = "DOGE"

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
@bot.command(name='prices', help='Enter 1 low and 1 high number to be notified when the exchannge rate crosses either limit')
async def set_prices(ctx, low, high):
    low = float(low)
    high = float(high)
    if low <= 0 or high <= 0: # low and/or high are 0 or negative
        await ctx.send(
            f"🛑 Slow down! Make sure you're entering 2 prices that are **greater than 0**!"
        )
    elif low == high: # low and high are the same number
        await ctx.send(
            f"🛑 Whoa there! Make sure you're entering 2 **different** prices!"
        )
    elif low < high:
        low_limit = low
        high_limit = high
        await ctx.send(
            f"✅ Got it! I'll do my best to notify you when the current exchange rate drops below **{low_limit}** or raises above **{high_limit}**!"
        )
    else: # low > high
        await ctx.send(
            f"🛑 Hold up! When setting prices, make sure that the 1st number is **less than** the 2nd!"
        )

# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.errors.MissingRequiredArgument):
#         await ctx.send('Missing argument(s)')
    
@bot.command(name='code', help='Enter the code for the cryptocurrency you want to get notifications for (i.e. BTC, DOGE)')
async def set_code(ctx, code):
    # await ctx.send(
    #     f"🛑 Hey, make sure to enter a code! Remember that I can only keep track of one code at a time."
    # )

    # check if code is valid
    url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=" + code + "&to_currency=USD&apikey=" + os.getenv('API_KEY')
    response = requests.request("GET", url)
    data = response.json()
    if 'Error Message' not in data:
        full_name = data["Realtime Currency Exchange Rate"]["2. From_Currency Name"]
        current_code = code.upper()
        await ctx.send(
            f"✅ Okay, boss! I'll send you notifications about **{full_name}**, aka **{current_code}**!"
        )
    else:
        await ctx.send(
            f"🛑 Hmmm... I'm sorry, but I don't know this code. Try entering a different one."
        )
    
    # url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=" + code + "&to_currency=USD&apikey=" + os.getenv('API_KEY')
    # response = requests.request("GET", url)
    # data = response.json()
    # exchange_rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    # if exchange_rate < low:
    #     await ctx.send(
    #         f'🔻 PRICE DROP! 🔻 The current exchange rate for DOGE is {exchange_rate}! Maybe buy?'
    #     )
    # elif exchange_rate > high:
    #     await ctx.send(
    #         f'🟢 PRICE SPIKE! 🟢 The current exchange rate for DOGE is {exchange_rate}! Maybe sell?'
    #     )

bot.run(TOKEN)

# @bot.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )

# @bot.command(name='roll_dice', help='Simulates rolling dice.')
# async def roll(ctx, number_of_dice: int, number_of_sides: int):
#     dice = [
#         str(random.choice(range(1, number_of_sides + 1)))
#         for _ in range(number_of_dice)
#     ]
#     await ctx.send(', '.join(dice))

# @bot.command(name='create-channel')
# @commands.has_role('admin')
# async def create_channel(ctx, channel_name='real-python'):
#     guild = ctx.guild
#     existing_channel = discord.utils.get(guild.channels, name=channel_name)
#     if not existing_channel:
#         print(f'Creating a new channel: {channel_name}')
#         await guild.create_text_channel(channel_name)