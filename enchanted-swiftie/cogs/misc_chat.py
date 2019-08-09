import random
from google_images_search import GoogleImagesSearch
from discord.ext import commands

# Stores the feature current status - True for on False for off


with open(r"support files\google shit.txt", "rt") as codes:
    gis = GoogleImagesSearch(codes.readline().rstrip(), codes.readline().strip())


class MiscChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.answers = ["Taylor thinks it is certain",
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

    @commands.command(aliases=["Tayball", "tayball", "tayBall", "TayBall"])
    async def tay_ball(self, ctx, *, question):
        """Sends Taylorized 8ball self.answers"""
        await ctx.send(self.answer_selector(question))

    @commands.command(aliases=["Event"])
    async def event(self, ctx, *, event_name=""):
        """sends either a random image of taylor swift or the first image on google images from a given query"""
        try:
            url = gis.search(search_params={'q': self.query_creator(event_name), 'num': 1})
            await ctx.send(url)
        except Exception as e:
            # User quota filled so google won't provide a url, error type doesn't exist
            # So have to manually search for error message
            if str(e).find("400 BAD REQUEST") != -1 or str(e).find("HttpError") != -1:
                await ctx.send("User image quota filled, please wait a minute and try again")
            # Daily quota filled, google won't provide more urls
            else:
                await ctx.send("sorry, try again tomorrow")

    def answer_selector(self, question) -> int:
        """Provides random answer, unless new romantics/wildest dreams are mentioned"""
        question = question.lower()
        if question.find("new romantics") != -1 or question.find("wildest dreams") != -1:
            if question.find("best") != -1 or question.find("good") != -1 \
                    or question.find("fantastic") != -1 or question.find("great") != -1:
                return random.choice(self.answers[0:10])
            elif question.find("worst") != -1 or question.find("bad") != -1 \
                    or question.find("trash") != -1 or question.find("garbage") != -1:
                return random.choice(self.answers[14:])
        return random.choice(self.answers)

    def query_creator(self, event_name) -> str:
        # Creates a proper search query
        query = "Taylor Swift " + event_name
        if event_name.strip() == "":
            # Really dumb way to create a random search
            query = "Taylor Swift " + random.choice("123456789") + random.choice("123456789") + \
                    random.choice("123456789")
        return query
