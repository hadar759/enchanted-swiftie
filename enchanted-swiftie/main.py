from discord.ext import commands
from cogs import *

cog_list = [MiscChat, Songs]


def main():
    bot = commands.Bot(command_prefix="t!")

    for cog in cog_list:
        bot.add_cog(cog(bot))

    with open(r"support files\token.txt", "rt") as token_file:
        token = token_file.read()
    bot.run(token)


if __name__ == "__main__":
    main()
