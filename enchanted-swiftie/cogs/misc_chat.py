import random
from typing import List

from discord.ext import commands
from google_images_search import GoogleImagesSearch
from googleapiclient.errors import HttpError

GOOD_ADJECTIVES = ["best", "good", "fantastic", "great"]
BAD_ADJECTIVES = ["worst", "bad", "trash", "garbage"]
GOOD_SONGS = ["new romantics", "wildest dreams"]


class MiscChat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.answers: List[str] = []
        with open(r"resources\tayball-answers.txt", "rt") as raw_answers:
            for line in raw_answers.readlines():
                self.answers.append(line)
        with open(r"resources\google-token.txt", "rt") as gis_token_file:
            self.gis = GoogleImagesSearch(gis_token_file.readline().rstrip(), gis_token_file.readline().strip())

    @commands.command(name="tayball", aliases=["Tayball", "tayBall", "TayBall"])
    async def command_tayball(self, ctx: commands.Context, *, question: str):
        """Sends Taylorized 8ball answers"""
        await ctx.send(self.select_tayball_answer(question))

    @commands.command(name="event", aliases=["Event"])
    async def commmand_event(self, ctx: commands.Context, *, event_name: str = ""):
        """sends either a random image of taylor swift or the first image on google images from a given query"""
        try:
            url = self.gis.search(search_params={'q': self.create_search_query(event_name), 'num': 1})
            await ctx.send(url)
        except HttpError as e:
            print(e.content)
            if "dailyLimitExceeded" in str(e.content):
                # Daily quota filled, google won't provide more urls
                await ctx.send("sorry, try again tomorrow")
            else:
                # User quota filled so google won't provide a url
                await ctx.send("User image quota filled, please wait a minute and try again")

    def select_tayball_answer(self, question: str) -> int:
        """Provides random answer, unless new romantics/wildest dreams are mentioned"""
        question = question.lower()
        if any(substr in question for substr in GOOD_SONGS):
            if any(substr in question for substr in GOOD_ADJECTIVES):
                return random.choice(self.answers[0:10])
            elif any(substr in question for substr in BAD_ADJECTIVES):
                return random.choice(self.answers[14:])
        return random.choice(self.answers)

    @staticmethod
    def create_search_query(event_name: str) -> str:
        # Creates a proper search query
        query = "Taylor Swift " + event_name
        if event_name.strip() == "":
            # Really dumb way to create a random search
            query = f"Taylor Swift {random.randrange(1000)}"
        return query
