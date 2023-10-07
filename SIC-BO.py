# https://github.com/Rapptz/discord.py/blob/master/examples/app_commands/basic.py
from typing import Optional
import random
import discord
from discord import app_commands
import datetime



MY_GUILD = discord.Object(id=991905864162226177)  # replace with your guild id

base_points = 1000


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


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


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
base_points = 1000

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

#設定骰子
def roll_dice():
    return [random.randint(1, 6) for _ in range(3)]

    # global base_points

    # if amount <= 0:
    #     await ctx.send("下注金額必須大於零。")
    #     return

    # if bet_type not in multipliers:
    #     await ctx.send("無效的下注類型。")
    #     return

    # if base_points < amount:
    #     await ctx.send("你的基礎點數不足以進行這個下注。")
    #     return


#比大小判斷式
@client.tree.command()
async def 大小(interaction, bet_type: str, amount: int):
    global base_points
    dice_roll = roll_dice()
    total = sum(dice_roll)
    if amount <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return

    if bet_type not in multipliers:
        await interaction.response.send_message("無效的下注類型。")
        return

    if base_points < amount:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return
    if bet_type == '大' and total >= 11 and total <= 17:
        base_points += int(amount * multipliers[bet_type])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll},總點數為:{total}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    elif bet_type == '小' and total >= 4 and total <= 10:
        base_points += int(amount * multipliers[bet_type])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll},總點數為:{total}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    else:
        base_points -= amount  # 輸掉下注金額
        await interaction.response.send_message(f"骰子點數為:{dice_roll},總點數為:{total}\n很遺憾,你輸了,你現在有 {base_points} 基礎點數。")


#全為判斷式
@client.tree.command()
async def 全圍(interaction, bet_value: int, amount: int):
    global base_points
    dice_roll = roll_dice()
    if amount <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return

    if bet_value not in multipliers:
        await interaction.response.send_message("無效的下注類型。")
        return

    if base_points < amount:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return
    if bet_value == dice_roll[0] == dice_roll[1] == dice_roll[2]:
        base_points += int(amount * multipliers[bet_value])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    else:
        base_points -= amount  # 輸掉下注金額
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n很遺憾,你輸了,你現在有 {base_points} 基礎點數。")



#總和判斷式
@client.tree.command()
async def 總和(interaction, bet_value: int, amount: int):
    global base_points
    dice_roll = roll_dice()
    total = sum(dice_roll)
    if amount <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return

    if bet_value not in multipliers:
        await interaction.response.send_message("無效的下注類型。")
        return

    if base_points < amount:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return
    if bet_value == total:
        base_points += int(amount * multipliers[bet_value])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll},總點數為:{total}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    else:
        base_points -= amount  # 輸掉下注金額
        await interaction.response.send_message(f"骰子點數為:{dice_roll},總點數為:{total}\n很遺憾,你輸了,你現在有 {base_points} 基礎點數。")


#單雙判斷式
@client.tree.command()
async def 單雙(interaction, bet_type: str, amount: int):
    global base_points
    dice_roll = roll_dice()
    total = sum(dice_roll)
    if amount <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return

    if bet_type not in multipliers:
        await interaction.response.send_message("無效的下注類型。")
        return

    if base_points < amount:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return
    if bet_type == '雙' and total % 2 == 0:
        base_points += int(amount * multipliers[bet_type])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll},總點數為:{total}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    if bet_type == '單' and total % 2 == 1:
        await interaction.response.send_message(f"骰子點數為:{dice_roll},總點數為:{total}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    else:
        base_points -= amount  # 輸掉下注金額
        await interaction.response.send_message(f"骰子點數為:{dice_roll},總點數為:{total}\n很遺憾,你輸了,你現在有 {base_points} 基礎點數。")



#圍骰判斷式
@client.tree.command()
async def 圍骰(interaction, bet_value: int, amount: int):
    global base_points
    dice_roll = roll_dice()
    if amount <= 0:
        await interaction.response.send_message("下注金額必須大於零。")
        return

    if bet_value not in multipliers:
        await interaction.response.send_message("無效的下注類型。")
        return

    if base_points < amount:
        await interaction.response.send_message("你的基礎點數不足以進行這個下注。")
        return
    if dice_roll[0] == dice_roll[1] == dice_roll[2] and bet_value == str(dice_roll[0]):
        base_points += int(amount * multipliers[bet_value])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    else:
        base_points -= amount  # 輸掉下注金額
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n很遺憾,你輸了,你現在有 {base_points} 基礎點數。")
  


#對子判斷式
@client.tree.command()
async def 對子(interaction, 你指定的對子點數: int, 賭資: int):
    global base_points
    dice_roll = roll_dice()
    if dice_roll[0] == dice_roll[1] == 你指定的對子點數:
        base_points += int(賭資 * multipliers['對子'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")        
    elif dice_roll[0] == dice_roll[2] == 你指定的對子點數:
        base_points += int(賭資 * multipliers['對子'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")  
    elif dice_roll[1] == dice_roll[2] == 你指定的對子點數:
        base_points += int(賭資 * multipliers['對子'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")  
    else:
        base_points -= 賭資  # 輸掉下注金額
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n很遺憾,你輸了,你現在有 {base_points} 基礎點數。")



#單骰判斷式
@client.tree.command()
async def 單骰(interaction, 你指定的點數: int, 賭資: int):
    global base_points
    dice_roll = roll_dice()
    if dice_roll[0] == 你指定的點數:
        base_points += int(賭資 * multipliers['單骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")        
    elif dice_roll[1] == 你指定的點數:
        base_points += int(賭資 * multipliers['單骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")    
    elif dice_roll[2] == 你指定的點數:
        base_points += int(賭資 * multipliers['單骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")   
    else:
        base_points -= 賭資  # 輸掉下注金額
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n很遺憾,你輸了,你現在有 {base_points} 基礎點數。")



#爽骰判斷式
@client.tree.command()
async def 雙骰(interaction, 你指定的點數: int, 賭資: int):
    global base_points
    dice_roll = roll_dice()
    if dice_roll[0] == 你指定的點數 == dice_roll[1]:
        base_points += int(賭資 * multipliers['雙骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    elif dice_roll[0] == dice_roll[2] == 你指定的點數 :
        base_points += int(賭資 * multipliers['雙骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    elif dice_roll[1] == dice_roll[2] == 你指定的點數  :
        base_points += int(賭資 * multipliers['雙骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    else:
        base_points -= 賭資  # 輸掉下注金額
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n很遺憾,你輸了,你現在有 {base_points} 基礎點數。")




#全骰判斷式
@client.tree.command()
async def 全骰(interaction, 你指定的點數一: int, 你指定的點數二: int, 你指定的點數三: int, 賭資: int):
    global base_points
    dice_roll = roll_dice()
    if dice_roll[0] == 你指定的點數一 and dice_roll[1] == 你指定的點數二 & dice_roll[2] == 你指定的點數三:
        base_points += int(賭資 * multipliers['全骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")             
    elif dice_roll[0] == 你指定的點數一 and dice_roll[2] == 你指定的點數二 & dice_roll[1] == 你指定的點數三:
        base_points += int(賭資 * multipliers['全骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。") 
    elif dice_roll[1] == 你指定的點數一 and dice_roll[0] == 你指定的點數二 & dice_roll[2] == 你指定的點數三:
        base_points += int(賭資 * multipliers['全骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。") 
    elif dice_roll[1] == 你指定的點數一 and dice_roll[2] == 你指定的點數二 & dice_roll[0] == 你指定的點數三:
        base_points += int(賭資 * multipliers['全骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    elif dice_roll[2] == 你指定的點數一 and dice_roll[1] == 你指定的點數二 & dice_roll[0] == 你指定的點數三:
        base_points += int(賭資 * multipliers['全骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    elif dice_roll[2] == 你指定的點數一 and dice_roll[0] == 你指定的點數二 & dice_roll[3] == 你指定的點數三:
        base_points += int(賭資 * multipliers['全骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    elif dice_roll[1] == 你指定的點數一 and dice_roll[0] == 你指定的點數二 & dice_roll[2] == 你指定的點數三:
        base_points += int(賭資 * multipliers['全骰'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    else:
        base_points -= 賭資  # 輸掉下注金額
        await interaction.response.send_message(f"你猜的是:{你指定的點數一},{你指定的點數二},{你指定的點數三}\n骰子點數為:{dice_roll}\n很遺憾,你輸了,你現在有 {base_points} 基礎點數。")



#牌九式判斷式
@client.tree.command()
async def 牌九式(interaction, 你指定的點數一: int, 你指定的點數二: int, 賭資: int):
    global base_points
    dice_roll = roll_dice()    
    if dice_roll[0] == 你指定的點數一 and dice_roll[1] == 你指定的點數二:
        base_points += int(賭資 * multipliers['牌九式'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的是:{你指定的點數一},{你指定的點數二}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    elif dice_roll[0] == 你指定的點數一 and dice_roll[2] == 你指定的點數二:
        base_points += int(賭資 * multipliers['牌九式'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的是:{你指定的點數一},{你指定的點數二}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    elif dice_roll[1] == 你指定的點數一 and dice_roll[2] == 你指定的點數二:
        base_points += int(賭資 * multipliers['牌九式'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的是:{你指定的點數一},{你指定的點數二}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    elif dice_roll[0] == 你指定的點數二 and dice_roll[1] == 你指定的點數一:
        base_points += int(賭資 * multipliers['牌九式'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的是:{你指定的點數一},{你指定的點數二}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    elif dice_roll[0] == 你指定的點數二 and dice_roll[2] == 你指定的點數一 :
        base_points += int(賭資 * multipliers['牌九式'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的是:{你指定的點數一},{你指定的點數二}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    elif dice_roll[1] == 你指定的點數二 and dice_roll[2] == 你指定的點數一 :
        base_points += int(賭資 * multipliers['牌九式'])  # 贏得下注金額,加上賠率獎勵
        await interaction.response.send_message(f"你猜的是:{你指定的點數一},{你指定的點數二}\n骰子點數為:{dice_roll}\n恭喜,你贏了!你現在有 {base_points} 基礎點數。")
    else:
        base_points -= 賭資  # 輸掉下注金額
        await interaction.response.send_message(f"你猜的是:{你指定的點數一},{你指定的點數二}\n骰子點數為:{dice_roll}\n很遺憾,你輸了,你現在有 {base_points} 基礎點數。")



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

        

client.run('MTEyMjkwMTQzNjk5NzU3ODc5Mg.GSP5iN.o3gvaEY_bUlz3kJkiDuvCpREy_vJ4a7_9rVG8w')