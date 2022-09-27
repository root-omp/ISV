from nextcord import Embed, Member
from nextcord.ext import commands
from nextcord.utils import utcnow
from humanfriendly import parse_timespan
from datetime import timedelta


class mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['clear', 'очистить'])
    @commands.has_permissions(manage_messages=True)
    async def _clear(self, ctx, amount: int = None, member: Member = None):
        await ctx.channel.purge(limit=1)
        if amount > 100:
            return await ctx.send(f'{ctx.author.mention} нельзя удалять больше 100 сообщений')

        deleted = await ctx.channel.purge(limit=amount) if not member else await ctx.channel.purge(limit=amount, check=lambda message: message.author.id == member.id)

        await ctx.send(
            embed=Embed(
                description=f':white_check_mark: Удалено  {len(deleted)} сообщений от пользователя {member}', color=0xff0000),
            delete_after=10)

    @commands.command(aliases=['ban', 'бан'])
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx, member: Member = None, *, reason=None):
        await ctx.channel.purge(limit=1)
        if member is None:
            return await ctx.send(f'{ctx.author.metnion} укажите пользователя')
        if member.top_role > ctx.author.top_role:
            return await ctx.send(f'{ctx.author.metnion} Вы не можете забанить пользователя с ролью выше вашей')
        if member.top_role > ctx.guild.get_member(self.client.user.id).top_role:
            return await ctx.send(f'{ctx.author.metnion} Я не могу забанить пользователя с ролью выше моей')
        await member.ban(reason=reason)
        await ctx.send(embed=Embed(title="Учатсник успешно забанен!", description=f'Модератор: {ctx.author.mention} забанили {member.name} по причине: {reason}'))

    @commands.command(aliases=['kick', 'кик'])
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx, member: Member = None, *, reason=None):
        await ctx.channel.purge(limit=1)
        if member is None:
            return await ctx.send(f'{ctx.author.metnion} укажите пользователя')
        if member.top_role > ctx.author.top_role:
            return await ctx.send(f'{ctx.author.metnion} Вы не можете кикнуть пользователя с ролью выше вашей')
        if member.top_role > ctx.guild.get_member(self.client.user.id).top_role:
            return await ctx.send(f'{ctx.author.metnion} Я не могу кикнуть пользователя с ролью выше моей')
        await member.kick(reason=reason)
        await ctx.send(embed=Embed(title="Учатсник успешно кикнут!", description=f'Модератор: {ctx.author.mention} забанили {member.name} по причине: {reason}'))

    @commands.command(aliases=['mute', 'timeout', 'мут', 'мьют'])
    @commands.has_permissions(moderate_members=True)
    async def _mute(self, ctx, member: Member = None, time=None, *, reason=None):
        if member is None:
            return await ctx.send(f'{ctx.author.mention} укажите пользователя')
        if time is None:
            return await ctx.send(f'{ctx.author.mention} укажите время')
        if member.top_role > ctx.author.top_role:
            return await ctx.send(f'{ctx.author.metnion} Вы не можете замутить пользователя с ролью выше вашей')
        if member.top_role > ctx.guild.get_member(self.client.user.id).top_role:
            return await ctx.send(f'{ctx.author.metnion} Я не могу замутить пользователя с ролью выше моей')
        time = parse_timespan(time)
        await member.edit(timeout=utcnow()+timedelta(seconds=time), reason=reason)
        await ctx.send(embed=Embed(title="Учатсник успешно замучен!", description=f'Модератор: {ctx.author.mention} забанили {member.name} по причине: {reason}'))


def setup(client):
    client.add_cog(mod(client))
