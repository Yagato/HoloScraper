# Yagato
# 17/5/2022

import discord
from scrapper import create_csv
from discord.ext import commands
from datetime import date
import os
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="$")

VALID_FLAIRS = ["EN", "ES", "JP", "RU", "ID"]

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.command(
    help = "<flair> represents the flair of the issues you want to retrieve. Supported flairs: JP, ES, RU, EN and ID",
    brief = "Fetches all the specificed issues from r/HoloNews and returns them as a CSV"
)
async def scrape(ctx, flair):
    if flair in VALID_FLAIRS:
        day = date.today().strftime("%d-%m-%Y")
        filename = flair + "_issues_" + day + ".csv"
        create_csv(flair)
        with open(f'csv/{filename}', 'rb') as f:
            csv = discord.File(f)
            await ctx.reply(file=csv)
    else:
        await ctx.reply("Invalid flair")

load_dotenv()
bot.run(os.getenv('DISCORD_TOKEN'))