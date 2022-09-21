from config import Config
from nextcord import Embed
from nextcord.ext import commands
import os


client = commands.Bot(command_prefix=Config.prefix,
                      owner_ids=Config.ids,
                      intents=Config.intents,
                      help_command=None)

client.remove_command("help")


@client.command(aliases=['load', 'подгрузить'])
@commands.is_owner()
async def _load(ctx, cog: str = None):
    if cog is None:
        emd = Embed(title='Ошибка', description='Вы не указали ког')
    else:
        try:
            client.load_extension(f'cogs.{cog}')
            emd = Embed(
                title='Ког', description=f'Ког {cog} был успешно загружен', color=0xFF7F50)
        except Exception:
            return await ctx.reply(embed=Embed(title='Ошибка', description=f'Не найден ког {cog}', color=0xff0000))
    return await ctx.reply(embed=emd)


@client.command(aliases=['unload', 'отгрузить'])
@commands.is_owner()
async def _unload(ctx, cog: str = None):
    if cog is None:
        emd = Embed(title='Ошибка', description='Вы не указали ког')
    else:
        try:
            client.unload_extension(f'cogs.{cog}')
            emd = Embed(
                title='Ког', description=f'Ког {cog} был успешно отгружен', color=0xFF7F50)
        except Exception:
            return await ctx.reply(embed=Embed(title='Ошибка', description=f'Не найден ког {cog}', color=0xff0000))
    return await ctx.reply(embed=emd)


@client.command(aliases=['reload', 'перегрузить', 'перезапустить'])
@commands.is_owner()
async def _reload(ctx, cog: str = None):
    if cog is None:
        emd = Embed(title='Ошибка', description='Вы не указали ког')
    else:
        try:
            client.unload_extension(f'cogs.{cog}')
            client.load_extension(f'cogs.{cog}')
            emd = Embed(
                title='Ког', description=f'Ког {cog} был успешно перезагружен', color=0xFF7F50)
        except Exception:
            return await ctx.reply(embed=Embed(title='Ошибка', description=f'Не найден ког {cog}', color=0xff0000))
    return await ctx.reply(embed=emd)

# + load all cogs
print('Загрузка всех когов')
for x in os.listdir("./cogs"):
    if x.endswith(".py"):
        print(f'Successfully loaded cog {x[:-3]}')
        client.load_extension(f"cogs.{x[:-3]}")

print('Коги загружены!')

client.run(Config.test_token)
