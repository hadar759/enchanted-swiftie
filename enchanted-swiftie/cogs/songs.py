import billboard
import datetime as dt
from discord.ext import commands


class Songs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.singles_dict = {}
        self.last_checked = None

    @commands.command(aliases=["Singles"])
    async def singles(self, ctx):
        """Returns all of Taylor's singles that peaked in the hot 100"""
        # Goes over all the charts up to current date
        while self.last_checked + dt.timedelta(7) < dt.datetime.date(dt.datetime.now()):
            # Creates a chart list for the week
            chart = billboard.ChartData("hot-100", str(self.last_checked))
            self.add_singles_to_dict(chart)
            # Goes over to the next chart
            self.last_checked += dt.timedelta(7)

        message = self.format_message()
        with open(r"support files\billboard.txt", "w") as file:
            # Updates the file
            file.write(f"{self.last_checked}\n{message[34:]}")

        await ctx.send(message)

    def add_singles_to_dict(self, chart):
        """Goes over all songs on the chart, to check if they're made by Taylor Swift"""
        for entry_place in range(len(chart)):
            entry = chart[entry_place]
            if entry.artist == "Taylor Swift":
                # Checks if we checked the single already
                if entry.title not in self.singles_dict.keys():
                    self.singles_dict[entry.title] = entry_place + 1
                # Updates the single's place if needed
                elif entry_place < self.singles_dict[entry.title]:
                    self.singles_dict[entry.title] = entry_place + 1

    def format_message(self) -> str:
        """Formatting the dict into a message the bot can send"""
        message = "All of Taylor's hot 100 singles:\n"

        for single in self.singles_dict.items():
            message += f"{single[0]} - {single[1]}\n"

        return message

    def read_singles_info(self):
        with open(r"support files\billboard.txt", "r") as file:
            """Reading the file and converting it to a last checked date and a singles dictionary"""
            date_str = file.readline()

            # Turns the string into a Year, month and day variables by hand
            year = int(date_str[0:4])
            month = int(date_str[5:7])
            day = int(date_str[8:10])

            # Creating a last checked variable, so i know where to check from instead of going over the last 10 years
            self.last_checked = dt.datetime(year, month, day).date()
            for line in file.readlines():
                # Turns the string into a 2 length list with the song name in the 0th place and the peak in the 1st
                single = line.split(" - ")
                self.singles_dict[single[0]] = int(single[1])
