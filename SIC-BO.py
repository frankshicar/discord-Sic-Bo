# https://github.com/Rapptz/discord.py/blob/master/examples/app_commands/basic.py
from typing import Optional
import random
import discord
from discord import app_commands
import datetime
import mysql.connector
import yaml


# 讀取 config.yml 文件
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

bot_token = config['bot_token']
MY_GUILD = discord.Object(id=config['guild_id'])
# API_KEY = AIzaSyBoC7nd0DCBg5RQSSmg4sh6YdE2whNfNfM
tenor_api_key = "AIzaSyBoC7nd0DCBg5RQSSmg4sh6YdE2whNfNfM"


mydb = mysql.connector.connect(
  host="localhost",        # 例如 "localhost"
  user="root",    # 例如 "root"
  password="frank0403",
  database="discord_player"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM players")
myresult = mycursor.fetchall()

logged_in_users = {}  # key: Discord ID, value: username
user_points = {}


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
    



#下拉式表單
class ButtonView(discord.ui.View):
    @discord.ui.select(placeholder = "選擇", min_values=1, max_values=1, options=[
            discord.SelectOption(label="大小", description="大小的規則及賠率"),
            discord.SelectOption(label="單雙", description="單雙的規則及賠率"),
            discord.SelectOption(label="圍骰", description="圍骰的規則及賠率"),
            discord.SelectOption(label="全圍", description="全圍的規則及賠率"),
            discord.SelectOption(label="下注在單一個點數", description="下注在單一個點數的規則及賠率"),
            discord.SelectOption(label="點數總和", description="點數總和的規則及賠率")
        ])
    async def select_callback(self, interaction:discord.Interaction,select:discord.ui.Select ):
            embed = discord.Embed(
                # title='骰寶歸則',
                # description='This is a rule',   
                colour=discord.Colour.purple()
            )
            self.disabled = True
            # await interaction.response.send_message(view=ButtonView())
            if select.values[0] == "大小":embed.add_field(name=":regional_indicator_b: 大", 
                    value="規則：總點數 11 至 17 ( 遇圍骰莊家通吃 )\n賠率：1 賠 1", 
                    inline=True) and embed.add_field(name=":regional_indicator_s:小" ,value="規則：總點數為 4 至 10 ( 遇圍骰莊家通吃 )\n賠率：1 賠 1\n",inline=True)
            elif select.values[0] == "單雙":embed.add_field(name="單", 
                    value="規則：總點數為 5, 7, 9, 11, 13, 15, 17 點 ( 遇圍骰莊家通吃 )\n賠率：1 賠 1\n", 
                    inline=True) and embed.add_field(name="雙",value="規則：總點數為 4, 6, 8, 10, 12, 14, 16 點 ( 遇圍骰莊家通吃 )賠率：1 賠 1\n",inline=True)
            elif select.values[0] == "圍骰":embed.add_field(name="圍骰", 
                    value="規則：3 顆骰子點數都一樣且是你指定的\n賠率：1 賠 180\n特別說明：「圍骰」跟「全圍」差別是在一個要指定點數一個不用。", 
                    inline=False)  
            elif select.values[0] == "全圍":embed.add_field(name="全圍（豹子）", 
                    value="規則：3 顆骰子點數都一樣但你不需指定點數\n賠率：1 賠 30\n特別說明：「圍骰」跟「全圍」差別是在一個要指定點數一個不用。", 
                    inline=True)  
            elif select.values[0] == "下注在單一個點數":embed.add_field(name="對子 ( 雙骰、長牌 )", 
                    value="規則：投注指定的雙骰 ( 如雙 1 點 ) ，至少開出 2 顆所投注的骰子\n賠率：1 賠 11\n", 
                    inline=True),embed.add_field(name="牌九式 ( 骨牌、短牌 )", 
                    value="規則：投注 15 種 2 顆骰子可能出現的組合 ( 如 1 、 2)\n賠率：1 賠 6\n", 
                    inline=True),embed.add_field(name="單骰", 
                    value="規則：投注每顆骰子 1 至 6 中指定的點數，點數出現 1 次\n賠率：1 賠 1\n", 
                    inline=False),embed.add_field(name="雙骰", 
                    value="規則：投注每顆骰子 1 至 6 中指定的點數，點數出現 2 次\n賠率：1 賠 2\n", 
                    inline=False),embed.add_field(name="全骰", 
                    value="規則：投注每顆骰子 1 至 6 中指定的點數，點數出現 3 次\n賠率：1 賠 3\n", 
                    inline=False) 
            elif select.values[0] == "點數總和":embed.add_field(name="點數總和", 
                    value="規則：4 或 17 點\n賠率：1 賠 60\n\n規則：5 或 16 點\n賠率：1 賠 20\n\n規則：6 或 15 點\n賠率：1 賠 18\n\n規則：7 或 14 點\n賠率：1 賠 12\n\n規則：8 或 13 點\n賠率：1 賠 8\n\n規則：9, 10, 11, 或 12點\n賠率：1 賠 6\n", 
                    inline=False)
            await interaction.response.send_message(embed=embed,view=ButtonView())

intents = discord.Intents.all()
client = MyClient(intents=intents)

# 注冊或登錄用戶
@client.tree.command()
async def register(interaction: discord.Interaction, username: str):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM players WHERE username = %s", (username,))
    result = mycursor.fetchone()
    if result:
        await interaction.response.send_message(f"用戶名 {username} 已存在。")
    else:
        mycursor.execute("INSERT INTO players (username, points) VALUES (%s, %s)", (username, 1000))
        mydb.commit()
        await interaction.response.send_message(f"用戶名 {username} 已註冊。")


# 查詢積分
@client.tree.command()
async def points(interaction: discord.Interaction, username: str):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT points FROM players WHERE username = %s", (username,))
    result = mycursor.fetchone()
    if result:
        await interaction.response.send_message(f"用戶名 {username} 的積分是: {result[0]}")
    else:
        await interaction.response.send_message(f"找不到用戶名 {username}。")

@client.tree.command()
async def login(interaction: discord.Interaction, username: str):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT points FROM players WHERE username = %s", (username,))
    result = mycursor.fetchone()
    if result:
        logged_in_users[interaction.user.id] = username
        user_points[interaction.user.id] = result[0]  # 儲存用戶的 points
        await interaction.response.send_message(f"用戶 {username} 已成功登錄。")
    else:
        await interaction.response.send_message("用戶名不存在。請先註冊。")



@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    print(myresult)


@client.event
async def on_member_join(member):
    channel = client.get_channel(991905864648753184)
    embed=discord.Embed(title="Welcome!",description=f"{member.mention} Just Joined")
    await channel.send(embed=embed)

@client.event 
async def on_member_join(member):
    channel = client.get_channel(991905864648753184)
    embed = discord.Embed(
        title='決戰骰寶!',
        description=f'{member.mention} has joined the server!\n歡迎遊玩骰寶',
        color=discord.Colour.purple()
    )
    await channel.send(embed=embed)

# 初始化基礎點數
points = 1000

# 定義各種玩法的賠率
multipliers = {
    '大': 1, 
    '小': 1,
    '圍骰': 180,
    '全圍': 30,
    '單骰': 1,
    '雙骰': 2,
    '全骰': 3,
    '對子': 11,
    '牌九式': 6,
    '4': 60,
    '17': 60,
    '5': 20,
    '16': 20,
    '6': 18,
    '15': 18,
    '7': 12,
    '14': 12,
    '8': 8,
    '13': 8,
    '9': 6,
    '10': 6,
    '11': 6,
    '12': 6,
    '單': 1,
    '雙': 1,
}

dice_gifs = {
    1 : 'https://media.tenor.com/BZGKCKH8Wp4AAAAi/dice-roll-dice.gif',
    2 :'https://media.tenor.com/VB6lPcSFiVgAAAAi/dice2-dice.gif',
    3 : 'https://media.tenor.com/Pq2avhc9XvkAAAAi/dice-roll-dice.gif',
    4 : 'https://media.tenor.com/cHiHze95e3cAAAAi/dice-roll-dice.gif',
    5 : 'https://media.tenor.com/iBb9CXPm3icAAAAi/dice-roll-dice.gif',
    6 : 'https://media.tenor.com/HcK7RSiai-AAAAAi/dice-roll-dice.gif'
}

#設定骰子
def roll_dice():
    return [random.randint(1, 6) for _ in range(3)]


#比大小判斷式
@client.tree.command()
async def 大小(interaction, 大或小: str, 賭資: int):
    global points
    dice_roll = roll_dice()
    total = sum(dice_roll)

    user_id = interaction.user.id
    if user_id not in logged_in_users:
        await interaction.response.send_message("您必須先登錄才能使用此命令。")
        return

    username = logged_in_users[user_id]
    points = user_points[interaction.user.id]
    # 創建一個嵌入列表來存儲每個骰子的嵌入
    embeds = []
    for i, result in enumerate(dice_roll, start=1):
        embed = discord.Embed(title=f"Dice {i} point is {result}", color=0x00ff00)
        embed.set_thumbnail(url=dice_gifs[result])
        embeds.append(embed)

    # 判斷勝負並更新基礎點數
    if 賭資 <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return
    if points < 賭資:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return

    if (大或小 == '大' and total >= 11 and total <= 17) or (大或小 == '小' and total >= 4 and total <= 10):
        points += int(賭資 * multipliers[大或小])
        result_message = f"你猜的總和是{大或小}\n骰子點數為:{dice_roll}, 總點數為:{total}\n恭喜,你贏了!你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()

    else:
        points -= 賭資
        result_message = f"你猜的總和是{大或小}\n骰子點數為:{dice_roll}, 總點數為:{total}\n很遺憾,你輸了,你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()

    # 創建一個顯示結果的嵌入
    result_embed = discord.Embed(description=result_message, color=discord.Color.blue())
    embeds.append(result_embed)

    # 發送嵌入列表
    await interaction.response.send_message(embeds=embeds)

#全圍判斷式
@client.tree.command()
async def 全圍(interaction, 賭資: int):
    global points
    dice_roll = roll_dice()

    user_id = interaction.user.id
    if user_id not in logged_in_users:
        await interaction.response.send_message("您必須先登錄才能使用此命令。")
        return

    username = logged_in_users[user_id]
    points = user_points[interaction.user.id]

    # 創建一個嵌入列表來存儲每個骰子的嵌入
    embeds = []
    for i, result in enumerate(dice_roll, start=1):
        embed = discord.Embed(title=f"Dice {i} point is {result}", color=0x00ff00)
        embed.set_thumbnail(url=dice_gifs[result])
        embeds.append(embed)

    if 賭資 <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return
    if points < 賭資:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return
    if dice_roll[0] == dice_roll[1] == dice_roll[2]:
        points += int(賭資 * multipliers['全圍'])  # 贏得下注金額,加上賠率獎勵
        result_message = f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    else:
        points -= 賭資  # 輸掉下注金額
        result_message = f"骰子點數為:{dice_roll}\n很遺憾,你輸了,你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    # 創建一個顯示結果的嵌入
    result_embed = discord.Embed(description=result_message, color=discord.Color.blue())
    embeds.append(result_embed)
    # 發送嵌入列表
    await interaction.response.send_message(embeds=embeds)

#總和判斷式
@client.tree.command()
async def 總和(interaction, 你指定的總和: int, 賭資: int):
    global points
    dice_roll = roll_dice()
    total = sum(dice_roll)

    user_id = interaction.user.id
    if user_id not in logged_in_users:
        await interaction.response.send_message("您必須先登錄才能使用此命令。")
        return

    username = logged_in_users[user_id]
    # 創建一個嵌入列表來存儲每個骰子的嵌入
    embeds = []
    for i, result in enumerate(dice_roll, start=1):
        embed = discord.Embed(title=f"Dice {i} point is {result}", color=0x00ff00)
        embed.set_thumbnail(url=dice_gifs[result])
        embeds.append(embed)

    if 賭資 <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return
    if points < 賭資:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return
    if 你指定的總和 == total:
        points += int(賭資 * multipliers[你指定的總和])  # 贏得下注金額,加上賠率獎勵
        result_message = f"你猜的總和是{你指定的總和}\n骰子點數為:{dice_roll},總點數為:{total}\n恭喜,你贏了!你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    else:
        points -= 賭資  # 輸掉下注金額
        result_message = f"你猜的總和是{你指定的總和}\n骰子點數為:{dice_roll},總點數為:{total}\n很遺憾,你輸了,你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    # 創建一個顯示結果的嵌入
    result_embed = discord.Embed(description=result_message, color=discord.Color.blue())
    embeds.append(result_embed)
    # 發送嵌入列表
    await interaction.response.send_message(embeds=embeds)

#單雙判斷式
@client.tree.command()
async def 單雙(interaction, 你指定的種類: str, 賭資: int):
    global points
    dice_roll = roll_dice()
    total = sum(dice_roll)

    user_id = interaction.user.id
    points = user_points[interaction.user.id]
    if user_id not in logged_in_users:
        await interaction.response.send_message("您必須先登錄才能使用此命令。")
        return

    username = logged_in_users[user_id]
    # 創建一個嵌入列表來存儲每個骰子的嵌入
    embeds = []
    for i, result in enumerate(dice_roll, start=1):
        embed = discord.Embed(title=f"Dice {i} point is {result}", color=0x00ff00)
        embed.set_thumbnail(url=dice_gifs[result])
        embeds.append(embed)

    if 賭資 <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return
    if points < 賭資:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return
    if 你指定的種類 == '雙' and total % 2 == 0:
        points += int(賭資 * multipliers[你指定的種類])  # 贏得下注金額,加上賠率獎勵
        result_message = f"你猜的是{你指定的種類}\n骰子點數為:{dice_roll},總點數為:{total}\n恭喜,你贏了!你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    if 你指定的種類 == '單' and total % 2 == 1:
        result_message = f"你猜的是{你指定的種類}\n骰子點數為:{dice_roll},總點數為:{total}\n恭喜,你贏了!你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    else:
        points -= 賭資  # 輸掉下注金額
        result_message = f"你猜的是{你指定的種類}\n骰子點數為:{dice_roll},總點數為:{total}\n很遺憾,你輸了,你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()

    # 創建一個顯示結果的嵌入
    result_embed = discord.Embed(description=result_message, color=discord.Color.blue())
    embeds.append(result_embed)
    # 發送嵌入列表
    await interaction.response.send_message(embeds=embeds)

#圍骰判斷式
@client.tree.command()
async def 圍骰(interaction, 你指定的圍骰點數: int, 賭資: int):
    global points
    dice_roll = roll_dice()

    user_id = interaction.user.id
    if user_id not in logged_in_users:
        await interaction.response.send_message("您必須先登錄才能使用此命令。")
        return

    username = logged_in_users[user_id]
    points = user_points[interaction.user.id]
    # 創建一個嵌入列表來存儲每個骰子的嵌入
    embeds = []
    for i, result in enumerate(dice_roll, start=1):
        embed = discord.Embed(title=f"Dice {i} point is {result}", color=0x00ff00)
        embed.set_thumbnail(url=dice_gifs[result])
        embeds.append(embed)

    if 賭資 <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return
    if points < 賭資:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return
    if dice_roll[0] == dice_roll[1] == dice_roll[2] == 你指定的圍骰點數:
        points += int(賭資 * multipliers[你指定的圍骰點數])  # 贏得下注金額,加上賠率獎勵
        result_message = f"你猜的圍骰為：{你指定的圍骰點數}{你指定的圍骰點數}{你指定的圍骰點數}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    else:
        points -= 賭資  # 輸掉下注金額
        result_message = f"你猜的圍骰為：{你指定的圍骰點數}{你指定的圍骰點數}{你指定的圍骰點數}\n骰子點數為:{dice_roll}\n很遺憾,你輸了,你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
  
    # 創建一個顯示結果的嵌入
    result_embed = discord.Embed(description=result_message, color=discord.Color.blue())
    embeds.append(result_embed)
    # 發送嵌入列表
    await interaction.response.send_message(embeds=embeds)

#對子判斷式
@client.tree.command()
async def 對子(interaction, 你指定的對子點數: int, 賭資: int):
    global points
    dice_roll = roll_dice()

    user_id = interaction.user.id
    if user_id not in logged_in_users:
        await interaction.response.send_message("您必須先登錄才能使用此命令。")
        return

    username = logged_in_users[user_id]
    points = user_points[interaction.user.id]
    # 創建一個嵌入列表來存儲每個骰子的嵌入
    embeds = []
    for i, result in enumerate(dice_roll, start=1):
        embed = discord.Embed(title=f"Dice {i} point is {result}", color=0x00ff00)
        embed.set_thumbnail(url=dice_gifs[result])
        embeds.append(embed)

    if 賭資 <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return
    if points < 賭資:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return
    if dice_roll[0] == dice_roll[1] == 你指定的對子點數:
        points += int(賭資 * multipliers['對子'])  # 贏得下注金額,加上賠率獎勵
        result_message = f"你猜的對子為：{你指定的對子點數}{你指定的對子點數}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。"        
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    elif dice_roll[0] == dice_roll[2] == 你指定的對子點數:
        points += int(賭資 * multipliers['對子'])  # 贏得下注金額,加上賠率獎勵
        result_message = f"你猜的對子為：{你指定的對子點數}{你指定的對子點數}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。"  
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    elif dice_roll[1] == dice_roll[2] == 你指定的對子點數:
        points += int(賭資 * multipliers['對子'])  # 贏得下注金額,加上賠率獎勵
        result_message = f"你猜的對子為：{你指定的對子點數}{你指定的對子點數}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    else:
        points -= 賭資  # 輸掉下注金額
        result_message = f"你猜的對子為：{你指定的對子點數}{你指定的對子點數}\n骰子點數為:{dice_roll}\n很遺憾,你輸了,你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    # 創建一個顯示結果的嵌入
    result_embed = discord.Embed(description=result_message, color=discord.Color.blue())
    embeds.append(result_embed)
    # 發送嵌入列表
    await interaction.response.send_message(embeds=embeds)

#單骰判斷式
@client.tree.command()
async def 單骰(interaction, 你指定的單骰點數: int, 賭資: int):
    global points
    dice_roll = roll_dice()

    user_id = interaction.user.id
    if user_id not in logged_in_users:
        await interaction.response.send_message("您必須先登錄才能使用此命令。")
        return

    username = logged_in_users[user_id]
    points = user_points[interaction.user.id]
    # 創建一個嵌入列表來存儲每個骰子的嵌入
    embeds = []
    for i, result in enumerate(dice_roll, start=1):
        embed = discord.Embed(title=f"Dice {i} point is {result}", color=0x00ff00)
        embed.set_thumbnail(url=dice_gifs[result])
        embeds.append(embed)

    if 賭資 <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return
    if points < 賭資:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return
    if dice_roll[0] == 你指定的單骰點數:
        points += int(賭資 * multipliers['單骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的單骰點數為：{你指定的單骰點數}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。")  
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()      
    elif dice_roll[1] == 你指定的單骰點數:
        points += int(賭資 * multipliers['單骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的單骰點數為：{你指定的單骰點數}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。")    
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    elif dice_roll[2] == 你指定的單骰點數:
        points += int(賭資 * multipliers['單骰'])  # 贏得下注金額,加上賠率獎勵
        result_message = f"你猜的單骰點數為：{你指定的單骰點數}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。"   
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    else:
        points -= 賭資  # 輸掉下注金額
        result_message = f"你猜的單骰點數為：{你指定的單骰點數}\n骰子點數為:{dice_roll}\n很遺憾,你輸了,你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    # 創建一個顯示結果的嵌入
    result_embed = discord.Embed(description=result_message, color=discord.Color.blue())
    embeds.append(result_embed)
    # 發送嵌入列表
    await interaction.response.send_message(embeds=embeds)

#雙骰判斷式
@client.tree.command()
async def 雙骰(interaction, 你指定的雙骰點數: int, 賭資: int):
    global points
    dice_roll = roll_dice()

    user_id = interaction.user.id
    if user_id not in logged_in_users:
        await interaction.response.send_message("您必須先登錄才能使用此命令。")
        return

    username = logged_in_users[user_id]
    points = user_points[interaction.user.id]
    # 創建一個嵌入列表來存儲每個骰子的嵌入
    embeds = []
    for i, result in enumerate(dice_roll, start=1):
        embed = discord.Embed(title=f"Dice {i} point is {result}", color=0x00ff00)
        embed.set_thumbnail(url=dice_gifs[result])
        embeds.append(embed)

    if 賭資 <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return
    if points < 賭資:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return
    if dice_roll[0]== dice_roll[1] == 你指定的雙骰點數 :
        points += int(賭資 * multipliers['雙骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的雙骰點數為：{你指定的雙骰點數}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。")
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    elif dice_roll[0] == dice_roll[2] == 你指定的雙骰點數 :
        points += int(賭資 * multipliers['雙骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的雙骰點數為：{你指定的雙骰點數}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。")
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    elif dice_roll[1] == dice_roll[2] == 你指定的雙骰點數  :
        points += int(賭資 * multipliers['雙骰'])  # 贏得下注金額,加上賠率獎勵
        result_message = f"你猜的雙骰點數為：{你指定的雙骰點數}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    else:
        points -= 賭資  # 輸掉下注金額
        result_message = f"你猜的雙骰點數為：{你指定的雙骰點數}\n骰子點數為:{dice_roll}\n很遺憾,你輸了,你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    # 創建一個顯示結果的嵌入
    result_embed = discord.Embed(description=result_message, color=discord.Color.blue())
    embeds.append(result_embed)
    # 發送嵌入列表
    await interaction.response.send_message(embeds=embeds)


#全骰判斷式
@client.tree.command()
async def 全骰(interaction, 你指定全骰的點數: int, 賭資: int):
    global points
    dice_roll = roll_dice()

    user_id = interaction.user.id
    if user_id not in logged_in_users:
        await interaction.response.send_message("您必須先登錄才能使用此命令。")
        return

    username = logged_in_users[user_id]
    points = user_points[interaction.user.id]
    # 創建一個嵌入列表來存儲每個骰子的嵌入
    embeds = []
    for i, result in enumerate(dice_roll, start=1):
        embed = discord.Embed(title=f"Dice {i} point is {result}", color=0x00ff00)
        embed.set_thumbnail(url=dice_gifs[result])
        embeds.append(embed)

    if 賭資 <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return
    if points < 賭資:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return
    if dice_roll[0] == 你指定全骰的點數 == dice_roll[1] == dice_roll[2] :
        points += int(賭資 * multipliers['全骰'])  # 贏得下注金額,加上賠率獎勵
        result_message = f"你猜的全骰點數為：{你指定全骰的點數}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。"             
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    else:
        points -= 賭資  # 輸掉下注金額
        result_message = f"你猜的全骰點數為：{你指定全骰的點數}\n骰子點數為:{dice_roll}\n很遺憾,你輸了,你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    # 創建一個顯示結果的嵌入
    result_embed = discord.Embed(description=result_message, color=discord.Color.blue())
    embeds.append(result_embed)
    # 發送嵌入列表
    await interaction.response.send_message(embeds=embeds)

#牌九式判斷式
@client.tree.command()
async def 牌九式(interaction, 你指定的點數一: int, 你指定的點數二: int, 賭資: int):
    global points
    dice_roll = roll_dice() 

    user_id = interaction.user.id
    if user_id not in logged_in_users:
        await interaction.response.send_message("您必須先登錄才能使用此命令。")
        return

    username = logged_in_users[user_id]
    points = user_points[interaction.user.id]
    # 創建一個嵌入列表來存儲每個骰子的嵌入
    embeds = []
    for i, result in enumerate(dice_roll, start=1):
        embed = discord.Embed(title=f"Dice {i} point is {result}", color=0x00ff00)
        embed.set_thumbnail(url=dice_gifs[result])
        embeds.append(embed)

    if 賭資 <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return
    if points < 賭資:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return   
    if dice_roll[0] == 你指定的點數一 and dice_roll[1] == 你指定的點數二:
        points += int(賭資 * multipliers['牌九式'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的牌九式是:{你指定的點數一},{你指定的點數二}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。")
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    elif dice_roll[0] == 你指定的點數一 and dice_roll[2] == 你指定的點數二:
        points += int(賭資 * multipliers['牌九式'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的牌九式是:{你指定的點數一},{你指定的點數二}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。")
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    elif dice_roll[1] == 你指定的點數一 and dice_roll[2] == 你指定的點數二:
        points += int(賭資 * multipliers['牌九式'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的牌九式是:{你指定的點數一},{你指定的點數二}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。")
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    elif dice_roll[0] == 你指定的點數二 and dice_roll[1] == 你指定的點數一:
        points += int(賭資 * multipliers['牌九式'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的牌九式是:{你指定的點數一},{你指定的點數二}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。")
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    elif dice_roll[0] == 你指定的點數二 and dice_roll[2] == 你指定的點數一 :
        points += int(賭資 * multipliers['牌九式'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的牌九式是:{你指定的點數一},{你指定的點數二}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。")
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    elif dice_roll[1] == 你指定的點數二 and dice_roll[2] == 你指定的點數一 :
        points += int(賭資 * multipliers['牌九式'])  # 贏得下注金額,加上賠率獎勵
        result_message = f"你猜的牌九式是:{你指定的點數一},{你指定的點數二}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    else:
        points -= 賭資  # 輸掉下注金額
        result_message = f"你猜的牌九式是:{你指定的點數一},{你指定的點數二}\n骰子點數為:{dice_roll}\n很遺憾,你輸了,你現在有 {points} 基礎點數。"
        mycursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, username))
        mydb.commit()
    # 創建一個顯示結果的嵌入
    result_embed = discord.Embed(description=result_message, color=discord.Color.blue())
    embeds.append(result_embed)
    # 發送嵌入列表
    await interaction.response.send_message(embeds=embeds)

#rule embed加下拉式表單
@client.tree.command()
async def rule(interaction):
    embed = discord.Embed(
        title='Rule',
        description='骰寶規則',
        colour=discord.Colour.purple()
    )
    await interaction.response.send_message(embed=embed,view = ButtonView()
)

        
client.run(bot_token)