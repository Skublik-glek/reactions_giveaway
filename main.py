from cgitb import text
from dis import dis
import discord
from discord.commands import Option
import asyncio
import random
import datetime

from vars import bot


@bot.slash_command(name="start", description="Начать розыгрыш")
async def start(ctx, prize: Option(str, "Что будем разыгрывать?", required = True), 
                time: Option(str, "Укажите еденицу времени", choices=["days", "seconds", "minutes", "hours"], required = True),
                number: Option(int, "Укажите длительность", required = True),
                channel: Option(discord.abc.GuildChannel, "Укажите канал для отправки", required = False)="this",
                requirements: Option(str, "Условия", required = False)="",
                winners: Option(int, "Число победителей", required = False)=1):
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond(f"{ctx.author.mention}, для этого действия необходимо исеть правва администратора!", ephemeral=True)
        return
    if channel == "this":
        channel = ctx
    if winners < 1:
        await ctx.respond(f"{ctx.author.mention}, не указывайте значение меньше 1!", ephemeral=True)
    mnoz = {"days": 60*60*24, "seconds": 1, "minutes": 60, "hours": 60*60}
    embed = discord.Embed(title="Розыгрыш!", 
                          description=f"Приз: `{prize}`\nЗакончится через: `{number} {time}`\nКол-во победителей: `{winners}`\nУсловия: **Поставить реакцию под этим сообщением**\n{requirements}",
                          color=0xFF1493,
                          timestamp=datetime.datetime.utcnow())
    await ctx.respond(f"{ctx.author.mention}, розыгрыш отправлен в канал {channel}", ephemeral=True)
    mess = await channel.send("@everyone", embed=embed)
    await mess.add_reaction('✅')
    mess = mess.id
    await asyncio.sleep(number * mnoz[time])
    mess: discord.Message = await channel.fetch_message(mess)
    yes_react = discord.utils.get(mess.reactions, emoji='✅')
    vse = await yes_react.users().flatten()
    if len(vse) - 1 < winners:
        await channel.send("Слишком мало людей поставили реакции!")
        return
    win = random.sample(vse[1::], winners)
    text = ""
    for us in win:
        text += f"{us.mention}, "
    await channel.send(f"{text}выиграл(и) {prize}")

@bot.slash_command(name="reroll", description="Начать розыгрыш")
async def start(ctx, id: Option(str, "id сообщения бота", required = True)):
    mess: discord.Message = await ctx.channel.fetch_message(int(id))
    yes_react = discord.utils.get(mess.reactions, emoji='✅')
    vse = await yes_react.users().flatten()
    win = random.sample(vse[1::], 1)
    text = ""
    for us in win:
        text += f"{us.mention}"
    await ctx.send(f"{text}выиграл")


bot.run("")



