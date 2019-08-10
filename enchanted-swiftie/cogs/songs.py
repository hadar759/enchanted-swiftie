import datetime as dt
from typing import Dict

import billboard
from discord.ext import commands


class Songs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.singles_dict: Dict[str, int] = {}
        self.last_checked_billboard: dt.datetime = dt.datetime.now()
        self.read_singles_info()

    @commands.command(name="singles", aliases=["Singles"])
    async def command_singles(self, ctx: commands.context):
        """Returns all of Taylor's singles that peaked in the hot 100"""
        # Goes over all the charts up to current date
        while self.last_checked_billboard + dt.timedelta(weeks=1) < dt.datetime.date(dt.datetime.now()):
            # Creates a chart list for the week
            chart = billboard.ChartData("hot-100", str(self.last_checked_billboard))
            self.add_singles_to_dict(chart)
            # Goes over to the next chart
            self.last_checked_billboard += dt.timedelta(weeks=1)

        message = self.format_singles(self.singles_dict)
        with open(r"resources\billboard.txt", "w") as singles_file:
            # Updates the file
            singles_file.write(f"{self.last_checked_billboard}\n{message[33:]}")

        await ctx.send("All of Taylor's hot 100 singles:\n" + message)

    def add_singles_to_dict(self, chart: billboard.ChartData):
        """Goes over all songs on the chart, to check if they're made by Taylor Swift"""
        for entry_place, entry in enumerate(chart):
            if entry.artist == "Taylor Swift":
                # Adds/updates the single if needed
                if entry.title not in self.singles_dict or entry_place < self.singles_dict[entry.title]:
                    self.singles_dict[entry.title] = entry_place + 1

    @staticmethod
    def format_singles(singles_dict: Dict[str, int]) -> str:
        """Formats the singles dict into a message the bot can send"""
        message = "\n".join(f"{single_name} - {single_place}" for single_name, single_place in singles_dict.items())
        for single_name, single_place in singles_dict.items():
            message += f"{single_name} - {single_place}"

        return message

    def read_singles_info(self):
        """Reads the file and updates the last_checked and singles_dict class variables"""
        with open(r"resources\billboard.txt", "r") as singles_file:
            # Creating a last checked variable, so i know where to check from instead of going over the last 10 years
            self.last_checked_billboard = dt.datetime.strptime(singles_file.readline()[:-1], "%Y-%m-%d").date()
            print(self.last_checked_billboard)
            # Reads the file and populates the singles_dict with the single name and it's peak place
            # noinspection PyTypeChecker
            self.singles_dict = dict(single.split(" - ") for single in singles_file.readlines())
