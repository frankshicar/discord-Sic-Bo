import random
import discord
from discord.ext import commands
import requests
import json
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)
bot_token = "MTEyMjkwMTQzNjk5NzU3ODc5Mg.G_Oldy.ukh1Ind1xzNvUaxff8QylVRozjglH0AoKf9HvQ"
tenor_api_key = "AIzaSyBoC7nd0DCBg5RQSSmg4sh6YdE2whNfNfM"
# url = 'https://media.tenor.com/BZGKCKH8Wp4AAAAi/dice-roll-dice.gif'
# url2 = 'https://media.tenor.com/VB6lPcSFiVgAAAAi/dice2-dice.gif'
# url3 = 'https://media.tenor.com/Pq2avhc9XvkAAAAi/dice-roll-dice.gif'
# url4 = 'https://media.tenor.com/cHiHze95e3cAAAAi/dice-roll-dice.gif'
# url5 = 'https://media.tenor.com/iBb9CXPm3icAAAAi/dice-roll-dice.gif'
# url6 = 'https://media.tenor.com/HcK7RSiai-AAAAAi/dice-roll-dice.gif'


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def roll_dice(ctx):
    # 隨機生成三個骰子的點數
    dice_results = [random.randint(1, 6) for _ in range(3)]

    # 為每個點數設置不同的 GIF 圖片網址
    dice_gifs = {
        1 : 'https://media.tenor.com/BZGKCKH8Wp4AAAAi/dice-roll-dice.gif',
        2 :'https://media.tenor.com/VB6lPcSFiVgAAAAi/dice2-dice.gif',
        3 : 'https://media.tenor.com/Pq2avhc9XvkAAAAi/dice-roll-dice.gif',
        4 : 'https://media.tenor.com/cHiHze95e3cAAAAi/dice-roll-dice.gif',
        5 : 'https://media.tenor.com/iBb9CXPm3icAAAAi/dice-roll-dice.gif',
        6 : 'https://media.tenor.com/HcK7RSiai-AAAAAi/dice-roll-dice.gif'
    }

    # 創建三個嵌入（Embed）對象，每個對應一個骰子的 GIF
    embeds = []
    for i, result in enumerate(dice_results, start=1):
        embed = discord.Embed(title=f"Dice {i} point is {dice_results[i-1]}", color=0x00ff00)
        embed.set_thumbnail(url=dice_gifs[result])
        embeds.append(embed)

    # 發送包含三個骰子動畫的嵌入消息
    await ctx.send(embeds=embeds)

# 只有呈現文字
# @bot.command()
# async def roll_dice(ctx):
#     # 创建一个嵌入（Embed）对象
#     embed = discord.Embed(title="Rolling Three Dice", color=0x00ff00)

#     # 随机生成三个骰子的点数
#     dice_results = [random.randint(1, 6) for _ in range(3)]
    
#     # 将点数添加到嵌入消息
#     embed.add_field(name="Dice 1", value=dice_results[0], inline=True)
#     embed.add_field(name="Dice 2", value=dice_results[1], inline=True)
#     embed.add_field(name="Dice 3", value=dice_results[2], inline=True)

#     # 发送包含骰子动画的嵌入消息
#     await ctx.send(embed=embed)


bot.run(bot_token)


