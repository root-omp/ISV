from nextcord import Embed, Status
from nextcord.ext import commands


class activity(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['send'])
    @commands.is_owner()
    async def _send(self, ctx):
        members = list(
            filter(lambda member: not member.bot, ctx.guild.members))
        await ctx.send(embeds=[
            Embed(
                title="Активность на сервере",
                description=f"""
            Онлайн: {len(list(filter(lambda member: member.status != Status.offline, members.copy())))}

            В войсе: {len(list(filter(lambda member: member.voice != None, members.copy())))}
            """,
                color=0x00c4ff),

            Embed(
                title="Участники в сети",
                description=str([i for i in members if [j.id for j in i.roles] in [557933393007083531,
                                                                                   557938454852403200,
                                                                                   557934371953180682,
                                                                                   774863001483477002,
                                                                                   557934061042270228,
                                                                                   809497438330552361,
                                                                                   745516823298048011,
                                                                                   557932429109886977,
                                                                                   960552810301227028]].sort(key=lambda member:member.top_role.position)),
                color=0x00c4ff),
        ])


def setup(client):
    client.add_cog(activity(client))
