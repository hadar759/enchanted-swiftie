import discord
from discord.ext import commands
import random
from google_images_search import GoogleImagesSearch


client = commands.Bot(command_prefix="t!")
with open("google shit.txt", "rt") as codes:
    gis = GoogleImagesSearch(codes.readline().rstrip(), codes.readline().strip())

# TODO move this to chat:
@client.command(aliases=["Tayball", "tayball", "tayBall", "TayBall"])
async def tay_ball(ctx, *, question):
    """Sends Taylorized 8ball answers"""
    # Only exists for the New Romantics/Wiledst Dreams test
    question = question.lower()
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
               "Taylor thinks it's definite",
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
    selected_message = random.randint(0, len(answers) - 1)
    # Providing a positive answer if someone asks if New Romantics/Wildest Dreams are good songs
    if question.find("new romantics") != -1 or question.find("wildest dreams") != -1:
        if question.find("best") != -1 or question.find("good") != -1 \
                or question.find("fantastic") != -1 or question.find("great") != -1:
                selected_message = random.randint(0, 9)
        elif question.find("worst") != -1 or question.find("bad") != -1 \
                or question.find("trash") != -1 or question.find("garbage") != -1:
                selected_message = random.randint(14, len(answers) - 1)
    await ctx.send(answers[selected_message])


@client.command(aliases=["Event"])
async def event(ctx, *, event_name=""):
    """sends either a random image of taylor swift or the first image on google images from a given query"""
    # Creates a proper search query
    query = "Taylor Swift " + event_name
    if event_name.strip() == "":
        query = "Taylor Swift " + random.choice("123456789") + random.choice("123456789") + \
                random.choice("123456789")
    try:
        await ctx.send(gis.search(search_params={'q': query, 'num': 1}))
        # TODO check what is the failure error
    #except FALIUREERROR:
        #await ctx.send("sorry, try again")
    except:
        await ctx.send("sorry, try again tomorrow")



def main():
    with open("token.txt", "rt") as token_file:
        token = token_file.read()
    client.run(token)


if __name__ == "__main__":
    main()
