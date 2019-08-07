import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix="t!")


@client.command(aliases=["Tayball", "tayball", "tayBall", "TayBall"])
async def tay_ball(ctx, *, question):
    question = question.tolower()
    # Taylorized 8ball answers, 10 positive, 5 neutral, 5 negative
    answers = ["Taylor thinks it is certain",
               "Taylor has no doubt",
               "Taylor will rely on it",
               "As taylor sees it, yes",
               "Taylor says it's most likely",
               "Taylor's outlook is good",
               "Leaks point to yes",
               "Taylor's positive that is the case",
               "Taylor's sure of it",
               "Taylor thinks it's definite"
               "Taylor's hazy, try again",
               "Ask Taylor later",
               "Taylor will tell you in a different time",
               "Taylor can't predict now",
               "Concentrate and ask again",
               "Taylor won't count on it",
               "Taylor's reply is no",
               "Leaks say no",
               "Taylor's outlook isn't very good",
               "Taylor is very doubtful"]
    selected_message = random.randint(0, len(answers))
    # Providing a positive answer if someone asks if New Romantics/Wildest Dreams are good songs
    if question.find("new romantics") != -1 or question.find("wildest dreams") \
        and question.find("best") != -1 or question.find("good") != -1  \
        or question.find("fantastic") != -1 or question.find("great") != -1:
        selected_message = random.randint(0, 11)
    await ctx.send(answers[selected_message])
