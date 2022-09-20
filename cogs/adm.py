import nextcord
from nextcord.ext import commands


class mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['clear', 'очистить'])
    @commands.has_permissions(manage_messages=True)
    async def _clear(self, ctx, amount: int = None, member: nextcord.Member = None):
        await ctx.channel.purge(limit=1)
        if amount > 100:
            return await ctx.send(f'{ctx.author.mention} нельзя удалять больше 100 сообщений')

        deleted = await ctx.channel.purge(limit=amount) if not member else await ctx.channel.purge(limit=amount, check=lambda message: message.author.id == member.id)

        await ctx.send(
            embed=nextcord.Embed(
                description=f':white_check_mark: Удалено  {len(deleted)} сообщений от пользователя {member}', color=0xff0000),
            delete_after=10)


def setup(client):
    client.add_cog(mod(client))
