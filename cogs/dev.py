import nextcord
from nextcord.ext import commands
import ast
import datetime


class Dev(commands.Cog):

    def __init__(self, client):
        self.client = client

    # eval
    @commands.command(aliases=['eval', 'e'])
    @commands.is_owner()
    async def _eval(self, ctx, *, code: str = None):
        if code is not None:
            def insert_returns(body):
                if isinstance(body[-1], ast.Expr):
                    body[-1] = ast.Return(body[-1].value)
                    ast.fix_missing_locations(body[-1])

                if isinstance(body[-1], ast.If):
                    insert_returns(body[-1].body)
                    insert_returns(body[-1].orelse)

                if isinstance(body[-1], ast.With):
                    insert_returns(body[-1].body)

            try:
                time = datetime.datetime.today()
                fn_name = "_eval_expr"

                code = code.strip("` ")
                _code = code

                code = "\n".join(f"    {i}" for i in code.splitlines())

                body = f"async def {fn_name}():\n{code}"

                parsed = ast.parse(body)
                body = parsed.body[0].body

                insert_returns(body)

                env = {
                    'client': self.client,
                    'nextcord': nextcord,
                    'commands': commands,
                    'ctx': ctx,
                    'guild': ctx.guild,
                    '__import__': __import__,
                    'self': self,
                    'datetime': datetime
                }
                exec(compile(parsed, filename="<ast>", mode="exec"), env)

                lines = _code.splitlines()
                answer = True
                display_time = True
                if 'eflags.no_answer' in lines:
                    answer = False
                elif 'eflags.no_display_time' in lines:
                    display_time = False
                result = (await eval(f"{fn_name}()", env))

                result = result if type(result) != str else f'"{result}"'
                time = f"\nВремя выполнения: `{datetime.datetime.today()-time}`" if display_time else ""

                if answer:
                    return await ctx.reply(embed=nextcord.Embed(
                        title='Разработчикам | Eval',
                        description=f'Ввод:\n```py\n{_code}\n```\nВывод:\n```py\n{result}\n```\nТип: `{str(type(result))[:-2][8:]}`{time}',
                        color=0xb000
                    ))
            except Exception as e:
                embed = self.client.embeds.error(
                    'Произашла ошибка при выполнение кода', 'Разработчикам | Eval')
                embed.add_field(
                    name='Сама ошибка',
                    value=f'```py\n{repr(e)}\n```',
                    inline=False
                )
                return await ctx.reply(embed=embed)
        else:
            return await ctx.send(embed=self.client.embeds.error("Укажите код!"))


# setup
def setup(client):
    client.add_cog(Dev(client))
