import discord
from discord.ext import commands
import asyncio
from parse import parse
import numpy as np
from itertools import groupby
import random
import copy

# 自分のBotのアクセストークン
TOKEN = '入力: アクセストークン'

bot = commands.Bot(command_prefix='/')

#インセインの狂気カード管理
# インセインの狂気カードについて
cards = ['狂気カード名']
#本当は怖い現代日本
japan =['狂気カード名']
# 狂乱の20年代
frenzy = ['狂気カード名']
# 暗黒のヴィクトリア
victoria = ['狂気カード名']

# カードの種類
addition_card = {'日本':japan, '狂乱':frenzy, 'ヴィクトリア': victoria}

# 繰り返される惨劇 
effect = {'狂気カード名':('オープン条件', 'カード効果')}

deck = []
# 公開された狂気カード pl名(name):[カードの名前]
open_cards = {}

# アカウントIDを message.author.id　で取得
# pcのクローズカードは pc_card, オープンカードは open_cards
pc_card = {}
# /insane　の実行者(.author.id)
gm = ""

# 山札とPCのカードリストのリセット
def reset(num):
    global deck
    global pc_card
    global open_cards
    deck.clear()
    #deck = copy.copy(cards)
    #random.shuffle(deck)
    deck = random.sample(cards, num)
    pc_card.clear()
    open_cards.clear()

# 山札とPCのカードリストのリセット
def reset2(num, names):
    global deck
    global pc_card
    global open_cards
    deck.clear()
    candidate = copy.copy(cards)
    if names[0] == 'all':
        for x in addition_card.values():
            candidate.extend(x)
    else:
        for x in names:
            candidate.extend(addition_card[x])
    deck = random.sample(candidate, num)
    pc_card.clear()
    open_cards.clear()

# 山札から1枚ドロー
def draw_card():
    global deck
    return deck.pop(0)

async def hello(ctx):
    await ctx.send(f"どうも、{ctx.message.author.name}さん！")

# 起動時の動作処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理

@bot.command()
async def insane(ctx, message:int, *args):
    try:
        global gm
        # メッセージ送信者がBotだった場合は無視する
        if ctx.author.bot:
            return
        if len(args) == 0:
            reset(message)
        else:
            reset2(message, args)
        gm = ctx.author.id
        await ctx.send("山札をセットしました")
    except:
        await ctx.send("false2")
        return

# /draw カードを引く
@bot.command()
async def draw(ctx):
    try:
        global deck
        global open_cards
        global pc_card
        global effect
        # メッセージ送信者がBotだった場合は無視する
        if ctx.author.bot:
            return
        pc = ctx.author.name
        # デッキからカードを引く
        card = draw_card()
        # 狂気の濁流判定
        if len(deck) <= 0:
            await ctx.send("狂気カードが全てでた、「狂気の濁流」")
            return
        detail = effect[card]
        m = "||" + "[ " + card + " ]\n条件: " + detail[0] + "\n内容: " + detail[1] + "||"
        # プレイヤーの手持ちにカード(名)を加える
        if not(pc in pc_card):
            pc_card[pc] = []
        pc_card[pc].append(card)
        await ctx.send(m)
        # ４枚以上カードを引いたらカードを１枚ランダムで公開
        if len(pc_card[pc]) >= 4:
            random.shuffle(pc_card[pc])
            open_card = pc_card[pc].pop(0)
            open_detail = effect[open_card]
            if not(pc in open_cards):
                open_cards[pc] = []
            open_cards[pc].append(open_card)
            m2 = "狂気顕在化\n" + "[ " +  open_card + " ]\n条件: " +open_detail[0] + "\n内容: " + open_detail[1]
            await ctx.send(m2)
    except:
        await ctx.send("error")
        return

# 自身の狂気カードの確認 closed card check
# /ccc a 名前、条件のみ /ccc b 内容も
@bot.command()
async def ccc(ctx, message:str):
    try:
        global deck
        global open_cards
        global pc_card
        global effect
        # メッセージ送信者がBotだった場合は無視する
        if ctx.message.author.bot:
            return
        pc = ctx.message.author.name
        m = ""
        if not(pc in pc_card):
            await ctx.send("狂気カードはありません")
            return
        # a 内容なし、 b 内容も
        if message.lower() == "a":
            for x in pc_card[pc]:
                m += "[ " + x + " ]\n条件: " + effect[x][0] +  "\n"
            await ctx.send("||" + m + "||")
            return
        elif message.lower() == "b":
            for x in pc_card[pc]:
                m += "[ " + x + " ]\n条件: " + effect[x][0] + "\n内容: "+ effect[x][1] +  "\n"
            await ctx.send("|| " + m + " ||") 
            return
        else:
            await ctx.send("ccc a　か ccc b")
            return
        await ctx.send(m)
    except:
        await ctx.send("ccc a　か ccc b")
        return

# 自身の狂気カードの確認 gm check
# /gmc a 全員のクローズカード確認(条件のみ),/gmc b 全員のクローズカード確認(内容も)
@bot.command()
async def gmc(ctx, message:str):
    try:
        global deck
        global open_cards
        global pc_card
        global effect
        # メッセージ送信者がBotだった場合は無視する
        if ctx.message.author.bot:
            return
        pc = ctx.message.author.name
        m = ""
        if ctx.author.id != gm:
            await ctx.send("GM のみ実行できます")
            return
        if len(pc_card) < 1:
            await ctx.send("誰も狂気カードを伏せてません")
            return
        # a 内容なし、 b 内容も
        if message.lower() == "a":
            for x in pc_card:
                m += "< " + x + " >\n"
                if len(pc_card[x]) == 0:
                    m += "0枚\n"
                    continue
                for y in pc_card[x]:
                    m += "[ " + y + " ]\n条件: " + effect[y][0]  +  "\n"
            await ctx.send("|| " + m + " ||") 
            return
        elif message.lower() == "b":
            for x in pc_card:
                m += "< " + x + " >\n"
                if len(pc_card[x]) == 0:
                    m += "0枚\n"
                    continue
                for y in pc_card[x]:
                    m += "[ " + y + " ]\n条件: " + effect[y][0] + "\n内容: "+ effect[y][1] +  "\n"
            await ctx.send("|| " + m + " ||") 
            return
        else:
            await ctx.send("gm a　か gm b ")
            return
        await ctx.send(m)
    except:
        await ctx.send("gm a か gm b")
        return

# オープンカードの確認(名前と内容のみ) open card check
# /occ 名前, /occ all
@bot.command()
async def occ(ctx, message:str):
    try:
        global deck
        global open_cards
        global pc_card
        global effect
        # メッセージ送信者がBotだった場合は無視する
        if ctx.message.author.bot:
            return
        pc = ctx.message.author.name
        m = ""
        # all　ならpc全員
        if message.lower() == "all":
            if len(open_cards) < 1:
                await ctx.send("誰も狂気が顕在化していない")
                return
            for x in open_cards:
                m += "< " + x + " >\n"
                pc_cards = open_cards[x]
                n = ""
                for y in pc_cards:
                    n += "[ " + y + " ]\n内容: " + effect[y][1] + "\n"
                m += n
        else:
            n = ""
            if not(message in open_cards):
                await ctx.send(message + " の狂気は顕在化していない")
                return
            for x in open_cards[message]:
                n += "[ " + x + " ]\n内容: " + effect[x][1] + "\n"
            m = "< " + message + " >\n" + n
        await ctx.send(m)
    except:
        await ctx.send("false2")
        return

# オープンカードの確認(条件含め) open card check detail
# /occd 名前, /occd all
@bot.command()
async def occd(ctx, message:str):
    try:
        global deck
        global open_cards
        global pc_card
        global effect
        # メッセージ送信者がBotだった場合は無視する
        if ctx.message.author.bot:
            return
        pc = ctx.message.author.name
        m = ""
        # all　ならpc全員
        if message.lower() == "all":
            if len(open_cards) < 1:
                await ctx.send("誰も狂気が顕在化していない")
                return
            for x in open_cards:
                m += "< " + x + " >\n"
                pc_cards = open_cards[x]
                n = ""
                for y in pc_cards:
                    n += "[ " + y + " ]\n条件: " + effect[y][0] + "\n内容: " + effect[y][1] + "\n"
                m += n
        else:
            n = ""
            if not(message in open_cards):
                await ctx.send(message + " の狂気は顕在化していない")
                return
            for x in open_cards[message]:
                n += "[ " + x + " ]\n条件: " + effect[x][0] + "\n内容: " + effect[x][1] + "\n"
            m = "< " + message + " >\n" + n
        await ctx.send(m)
    except:
        await ctx.send("false2")
        return

# 狂気カードの顕在化
@bot.command()
async def oc(ctx, message:str):
    try:
        global deck
        global open_cards
        global pc_card
        global effect
        # メッセージ送信者がBotだった場合は無視する
        if ctx.message.author.bot:
            return
        pc = ctx.message.author.name
        m = ""
        if not(pc in pc_card):
            await ctx.send("対応の狂気カードを持っていません")
            return
        # pc が その狂気カードを持っていれば公開
        if message in pc_card[pc]:
            m = "狂気カード [" + message + "] 公開" + "\n条件: " + effect[message][0] + "\n内容: " + effect[message][1] 
            # 狂気カードをクローズからオープンへ
            pc_card[pc].remove(message)
            if not(pc in open_cards):
                open_cards[pc] = []
            open_cards[pc].append(message)
        else:
            await ctx.send("対応の狂気カードを持っていません")
            return
        await ctx.send(m)
    except:
        await ctx.send("false2")
        return

# カード枚数の確認 デッキも
@bot.command()
async def cn(ctx, message:str):
    try:
        global deck
        global open_cards
        global pc_card
        global effect
        # メッセージ送信者がBotだった場合は無視する
        if ctx.message.author.bot:
            return
        m = ""
        if len(pc_card) < 1:
            m = "誰もカードを持ってません\n山札: " + str(len(deck)) + "枚\n"
            await ctx.send(m)
            return
        pc_name = pc_card.keys()
        # all　ならpc全員
        if message.lower() == "all":
            for x in pc_name:
                num = len(pc_card[x])
                num2 = 0
                if x in open_cards:
                    num2 = len(open_cards[x])
                total = num + num2
                m += "< " + x + " >" + "\nクローズ: "+ str(num)+ "枚\nオープン" + str(num2) + "枚\n計 " + str(total)+ "枚\n" 
            m += "山札: " + str(len(deck)) +"枚\n"
            await ctx.send(m)
            return
        elif not(message in pc_name):
            await ctx.send("そんな PL はいません")
            return
        num = len(pc_card[message])
        num2 = 0
        if message in open_cards:
            num2 += len(open_cards[message])
        total = num + num2
        m = "< " + message + " >" + "\nクローズ: " + str(num) + "枚\nオープン" + str(num2) + "枚\n計 " + str(total) + "枚\n"
        m += "山札: " + str(len(deck)) +"枚\n"
        await ctx.send(m)
    except:
        await ctx.send("false2")
        return

@bot.command()
async def test(ctx):
    try:
        global deck
        global open_cards
        global pc_card
        # メッセージ送信者がBotだった場合は無視する
        print("deck:", deck)
        print("cards:", cards)
        print("open_cards:", open_cards)
        print("pc_cards:", pc_card)
        print(ctx.author.name)
        print(ctx.author.bot)
        m = "deck: " + str(deck)
        m +="\ncards:"+ str(cards)
        m += "\nopen_cards:"+ str(open_cards)
        m += "\npc_cards:"+ str(pc_card)
        await ctx.send(m)
    except:
        await ctx.send("false2")
        return


#　ウタカゼ
def simple_dice(dice_size, dice_num):
    try:
        dice_array = np.random.randint(1, dice_size+1, dice_num).tolist()
        dice_array.sort()
        return dice_array
    except:
        return


async def hello(ctx):
    await ctx.send(f"どうも、{ctx.message.author.name}さん！")

# 起動時の動作処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@bot.command()
async def u(ctx, message:str):
    try:
        # メッセージ送信者がBotだった場合は無視する
        if ctx.message.author.bot:
            return
        info = parse('{}d{}', message)
        # 「/u」でウタカゼのダイス処理
        dice_size = int(info[1])
        dice_num = int(info[0])
        m = simple_dice(dice_size, dice_num)
        m.sort()
        result = ""
        success_num = 0
        set_num = 0
        for key, group in groupby(m):
            x = list(group)
            result += str(x) + "    "
            length = len(x)
            if length > 1:
                set_num += 1
                if length > success_num:
                    success_num = length
        m = result + "\n" + "{} 成功 {} セット".format(success_num, set_num)
        await ctx.send(m)
    except:
        await ctx.send("error")
        return

@bot.command()
async def uc(ctx, message:str, dragon:int):
    try:
        # メッセージ送信者がBotだった場合は無視する
        if ctx.message.author.bot:
            return
        info = parse('{}d{}', message)
        dice_size = int(info[1])
        dice_num = int(info[0])
        m = simple_dice(dice_size, dice_num)
        result = ""
        success_num = 0
        set_num = 0
        for key, group in groupby(m):
            x = list(group)
            result += str(x) + "    "
            num = x[0]
            if num == dragon:
                success_num = len(x) * 2
                set_num = 1
        m = result + "\n" + "{} 成功 {} セット".format(success_num, set_num)
        await ctx.send(m)
    except:
        await ctx.send("false2")
        return

@bot.command()
async def myhelp(ctx, message:str):
    try:
        # メッセージ送信者がBotだった場合は無視する
        if ctx.message.author.bot:
            return
        m = ""
        if message.lower() == "i":
            m += "デッキ生成(GMが実行)(セッション開始時に1回行う) /insane 山札の数 追加カード指定\n"
            m += "狂気カードドロー /draw\n"
            m += "自身の狂気カードの顕在化 /oc 狂気カード名\n"
            m += "自身の公開されていない狂気カードの確認(名前と条件) /ccc a\n"
            m += "自身の公開されていない狂気カードの確認(内容も) /ccc b\n"
            m += "全PLの公開されていない狂気カードの確認(名前と条件)(GMのみ可能) /gmc a\n"
            m += "全PLの公開されていない狂気カードの確認(内容も)(GMのみ可能) /gmc b\n"
            m += "公開された狂気カードの確認(全員)(名前・内容) /occ all\n"
            m +=  "公開された狂気カードの確認(指定)(名前・内容) /occ アカウント名\n"
            m += "公開された狂気カードの確認(全員)(条件も) /occd all\n"
            m +=  "公開された狂気カードの確認(指定)(条件も) /occd アカウント名\n"
            m += "全PLと山札の狂気カードの枚数確認 /cn all\n"
            m += "指定したPLと山札の狂気カードの枚数確認 /cn アカウント名\n"
        elif message.lower() == "u":
            m += "ダイスを振る /u nd6\n"
            m += "龍の目でダイスを振る /uc nd6 龍の目\n"
        await ctx.send(m)
    except:
        await ctx.send("/myhelp u か /myhelp i")
        return

# Botの起動とDiscordサーバーへの接続
bot.run(TOKEN)