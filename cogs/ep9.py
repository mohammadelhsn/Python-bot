import discord
from discord.ext import commands
import random


class Channels(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(aliases=['cs'])
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channelstats(self, ctx):
        """
        Sends a nice fancy embed with some channel stats
        !channelstats
        """
        channel = ctx.channel
        embed = discord.Embed(
            title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}", color=random.choice(self.bot.colour_list))
        embed.add_field(name="Channel Guild",
                        value=ctx.guild.name, inline=False)
        embed.add_field(name="Channel Guild",
                        value=ctx.guild.name, inline=False)
        embed.add_field(name="Channel Id", value=channel.id, inline=False)
        embed.add_field(name="Channel Topic",
                        value=f"{channel.topic if channel.topic else 'No topic.'}", inline=False)
        embed.add_field(name="Channel Position",
                        value=channel.position, inline=False)
        embed.add_field(name="Channel Slowmode Delay",
                        value=channel.slowmode_delay, inline=False)
        embed.add_field(name="Channel is nsfw?",
                        value=channel.is_nsfw(), inline=False)
        embed.add_field(name="Channel is news?",
                        value=channel.is_news(), inline=False)
        embed.add_field(name="Channel Creation Time",
                        value=channel.created_at, inline=False)
        embed.add_field(name="Channel Permissions Synced",
                        value=channel.permissions_synced, inline=False)
        embed.add_field(name="Channel Hash", value=hash(channel), inline=False)

        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def category(self, ctx, role: discord.Role, *, name):
        overwrites = {
            ctx.guld.default_role: discord.PermissionOverwrite(read_messages=True),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites)
        await ctx.send(f"Hey! I made {channel.name} for you! :slight_smile:")


def setup(bot):
    bot.add_cog(Channels(bot))
