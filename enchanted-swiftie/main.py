import discord
from discord.ext import commands
import random
import billboard
from google_images_search import GoogleImagesSearch
import datetime as dt


# Stores the feature current status - True for on False for off
tayball = True
event_status = True
singles_dict = {}
last_checked = None
with open("billboard.txt", "r") as file:
    """Reading the file and converting it to a last checked date and a singles dictionary"""
    date_str = file.readline()
    # Turns the string into a Year, month and day variables by hand
    year = int(date_str[0:4])
    month = int(date_str[5:7])
    day = int(date_str[8:10])
    # Creating a last checked variable, so i know where to check from instead of going over the last 10 years
    last_checked = dt.datetime(year, month, day).date()
    for line in file.readlines():
        # Turns the string into a 2 length list with the song name in the 0th place and the peak in the 1st
        single = line.split(" - ")
        singles_dict[single[0]] = int(single[1])

client = commands.Bot(command_prefix="t!")
with open("google shit.txt", "rt") as codes:
    gis = GoogleImagesSearch(codes.readline().rstrip(), codes.readline().strip())


# TODO move this to chat:
@client.command(aliases=["Tayball", "tayball", "tayBall", "TayBall"])
async def tay_ball(ctx, *, question):
    """Sends Taylorized 8ball answers"""
    global tayball
    if question == "off":
        tayball = False
        await ctx.send("Tayball feature is now turned off")
    if question == "on":
        tayball = True
        await ctx.send("Tayball feature is now turned on")
        return
    if tayball:
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
    global event_status
    # Turns the feature on or off
    if event_name == "off":
        event_status = False
        await ctx.send("Image feature is now turned off")
    if event_name == "on":
        event_status = True
        await ctx.send("Image feature is now turned on")
        return
    if event_status:
        # Creates a proper search query
        query = "Taylor Swift " + event_name
        if event_name.strip() == "":
            query = "Taylor Swift " + random.choice("123456789") + random.choice("123456789") + \
                    random.choice("123456789")
        try:
            url = gis.search(search_params={'q': query, 'num': 1})
            await ctx.send(url)
        except Exception as e:
            # User quota filled so google won't provide a url, error type doesn't exist
            # So have to manually search for error message
            if str(e).find("400 BAD REQUEST") != -1 or str(e).find("HttpError") != -1:
                await ctx.send("User image quota filled, please wait a minute and try again")
            # Daily quota filled, google won't provide more urls
            else:
                await ctx.send("sorry, try again tomorrow")


@client.command(aliases=["Singles"])
async def singles(ctx):
    global singles_dict, last_checked
    # The first chart after Taylor's first single was released
    # Goes over all the charts up to this date
    while last_checked < dt.datetime.date(dt.datetime.now()):
        print(last_checked)
        # Creates a chart list for the week
        chart = billboard.ChartData("hot-100", str(last_checked))
        # Goes over all songs on the chart, to check if they're made by Taylor Swift
        for entry_place in range(len(chart)):
            entry = chart[entry_place]
            if entry.artist == "Taylor Swift":
                # Checks if we checked the single already
                if entry.title not in singles_dict.keys():
                    singles_dict[entry.title] = entry_place + 1
                # Updates the single's place if needed
                elif entry_place < singles_dict[entry.title]:
                    singles_dict[entry.title] = entry_place + 1
        # Goes over to the next chart
        last_checked = last_checked + dt.timedelta(7)
    # Formatting the dict into a message the bot can send
    message = "All of Taylor's hot 100 singles:\n"
    for single in singles_dict.items():
        message += f"{single[0]} - {single[1]}\n"
    with open("billboard.txt", "w") as file:
        # Updates the file
        file.write(f"{last_checked}\n{message[34:]}")
    await ctx.send(message)



def main():
    with open("token.txt", "rt") as token_file:
        token = token_file.read()
    client.run(token)


if __name__ == "__main__":
    main()
