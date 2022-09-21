from nextcord import Embed, Status
from nextcord.ext import commands
from asyncio import sleep


class activity(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['send'])
    @commands.is_owner()
    async def _send(self, ctx):
        members = list(
            filter(lambda member: not member.bot, ctx.guild.members))

        roles_list = [557933393007083531,
                      557938454852403200,
                      557934371953180682,
                      774863001483477002,
                      557934061042270228,
                      809497438330552361,
                      745516823298048011,
                      557932429109886977,
                      960552810301227028]

        members = [i for i in list(filter(lambda member: not member.bot, ctx.guild.members)) if any(
            k in roles_list for k in [j.id for j in i.roles])]

        await ctx.send(embeds=[
            Embed(
                title="Активность на сервере",
                description=f"""
            Онлайн: {
                len(online := list(filter(lambda member: member.status != Status.offline, members.copy())))}

            В войсе: {len(list(filter(lambda member: member.voice != None, members.copy())))}
            """,
                color=0x00c4ff),

            Embed(
                title="Участники в сети",
                description="\n".join([mem.name for mem in sorted(
                    online, key=lambda member: member.top_role)]),
                color=0x00c4ff)
        ])

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            guild = self.client.get_guild(874575960819765278)
            msg = await (self.client.get_channel(960552084002963466)).fetch_message(1021929904423579698)

            members = list(
                filter(lambda member: not member.bot, guild.members))

            roles_list = [557933393007083531,
                          557938454852403200,
                          557934371953180682,
                          774863001483477002,
                          557934061042270228,
                          809497438330552361,
                          745516823298048011,
                          557932429109886977,
                          960552810301227028]

            members = [i for i in list(filter(lambda member: not member.bot, guild.members)) if any(
                k in roles_list for k in [j.id for j in i.roles])]

            await msg.edit(embeds=[
                Embed(
                    title="Активность на сервере",
                    description=f"""
                Онлайн: {
                    len(online := list(filter(lambda member: member.status != Status.offline, members.copy())))}

                В войсе: {len(list(filter(lambda member: member.voice != None, members.copy())))}
                """,
                    color=0x00c4ff),

                Embed(
                    title="Участники в сети",
                    description="\n".join([mem.name for mem in sorted(
                        online, key=lambda member: member.top_role)]),
                    color=0x00c4ff)
            ])
            await sleep(300)


def setup(client):
    client.add_cog(activity(client))
