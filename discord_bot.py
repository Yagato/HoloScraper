# Yagato
# 1/4/2023

import discord
from scrapper import create_csv_reddit
from yt_data import create_csv_talents
from discord.ext import commands
from datetime import date
import os
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="$")

VALID_FLAIRS = ["EN", "ES", "JP", "RU", "ID"]

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


@bot.command()
async def scrape(ctx, flair):
    if flair in VALID_FLAIRS:
        day = date.today().strftime("%d-%m-%Y")
        filename = flair + "_issues_" + day + ".csv"
        await create_csv_reddit(flair)
        with open(f'csv/reddit_scrapper/{filename}', 'rb') as f:
            csv = discord.File(f)
            await ctx.reply(file=csv)
    else:
        await ctx.reply("Invalid flair")


@bot.command()
async def get_subs(ctx):
    day = date.today().strftime("%Y-%m-%d")
    filename = 'talents_subscribers_' + day + '.csv'
    create_csv_talents(filename, day)
    with open(f'csv/yt_data/{filename}', 'rb') as file:
        csv = discord.File(file)
        await ctx.reply(file=csv)

@bot.command()
async def quit(ctx):
    await ctx.send("Adioooos 👋")
    return await bot.logout()


load_dotenv()
bot.run(os.getenv('DISCORD_TOKEN'))