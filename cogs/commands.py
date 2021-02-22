import discord
from discord.ext import commands
import platform
import random

import cogs._json

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands Cog has been loaded\n-----")

    @commands.command()
    async def stats(self, ctx):
        """
        A useful command that displays bot statistics.
        """
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
                                                                            # This is pretty much a "blank character"
        embed = discord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF', colour=random.choice(self.bot.colour_list), timestamp=ctx.message.created_at)

        embed.add_field(name='Bot Version:', value=self.bot.version)    # the field for the bot version, which is defined in the bot.py file
        embed.add_field(name='Python Version:', value=pythonVersion) # Python version!
        embed.add_field(name='Discord.Py Version', value=dpyVersion) #Discord.py version!
        embed.add_field(name='Total Guilds:', value=serverCount) # total server count! 
        embed.add_field(name='Total Users:', value=memberCount) # Total member count
        embed.add_field(name='Bot Developers:', value="<@398264990567628812>") # owner id

        embed.set_footer(text=f"Hello there! | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['disconnect', 'close', 'stopbot'])
    @commands.is_owner()
    async def logout(self, ctx):
        """
        If the user running the command owns the bot then this will disconnect the bot from discord.
        """
        await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:")
        await self.bot.logout()

    @commands.command()
    async def echo(self, ctx, *, message=None):
        """
        A simple command that repeats the users input back to them.
        """
        message = message or "Please provide the message to be repeated."
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send("Hey, you cannot blacklist yourself!")
            return

        self.bot.blacklisted_users.append(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"Hey, I have blacklisted {user.name} for you.")

    @commands.command()
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member):
        self.bot.blacklisted_users.remove(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"Hey, I have unblacklisted {user.name} for you.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx, *, pre='/'):
        """
        Sets a custom prefix for the server
        """
        data = cogs._json.read_json('prefixes')
        data[str(ctx.message.guild.id)] = pre
        cogs._json.write_json(data, "prefixes")
        await ctx.send(f"The servers prefix has been changed to **`{pre}`**! Use `{pre}prefix <prefix> to change it again!")

def setup(bot):
    bot.add_cog(Commands(bot))