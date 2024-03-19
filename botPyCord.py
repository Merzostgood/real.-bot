import json,asyncio,logging,discord,random
from discord import Option, SelectOption
from discord.ui import View, Button, Select
from discord.ext import commands,tasks
from datetime import datetime
intents = discord.Intents.default()
logging.basicConfig(
    filename='Logs.log',
    format='%(asctime)s |:| LEVEL: %(levelname)s |:| %(message)s ',
    datefmt='"%y/%b/%Y %H:%M:%S',
)

bot = discord.Bot(test_guilds=1168481058031931422)

@tasks.loop(minutes=5)
async def updater():
    statuses = ['/premium','use /premium', '/premium_activate','/premium','/premium','/premium','/premium','/premium','/premium','/premium','/premium','/premium','/premium','/premium','free key "1PQYC-ND7UO-T1AEH-IXGQ4-VM6QC7"','/premium','/premium','/premium','/premium','/premium','/premium','/premium','/premium']
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=statuses[random.randint(0,22)]))
    data = await reader()
    day = datetime.now().strftime("%d");day = int(day);Year = datetime.now().strftime("%y");Year = int(Year); Month = datetime.now().strftime("%m");Month = int(Month)
    LastUpdate = data["LastUpdate"]
    if (day > LastUpdate["Day"]) or (Month > LastUpdate["Month"]) or (Year > LastUpdate["Year"]):
        for i in data["MessagesLeft"]:
            data["MessagesLeft"][i] = 1000
        logging.error('All messages updated!')
        data["LastUpdate"]["Day"] = day;data["LastUpdate"]["Month"] = Month;data["LastUpdate"]["Year"] = Year
        await JSONUpdate(data)

@bot.event
async def on_ready():
    updater.start()
    logging.error(' ')
    logging.error(' ')
    logging.error(' ')
    logging.error('Bot starter!')


async def spamDef(channels, arg1, j, arg3, arg5, creator):
    channelNow = bot.get_channel(channels[j])
    for i in range(arg1):
        await channelNow.send(f"{arg3.mention} {arg5} _(by {creator})_", delete_after=3600)
    return 1

async def JSONUpdate(data):
    with open("database.json", "w") as f:
        f.write(json.dumps(data, indent=4))
    f.close()
    logging.error("JSON updated")
    return data

async def reader():
    with open("database.json", "r") as f:
        data = json.loads(f.read())
    f.close()
    return data

async def premiumEmbed(ctx, command_name):
    embed = discord.Embed(title=command_name, color=0xc800ff, timestamp=datetime.now())
    embed.set_author(name="")
    embed.set_thumbnail(url="https://graph.digiseller.ru/img.ashx?id_d=3564600")
    embed.add_field(name="",
                    value=f"{ctx.author.name}, похоже что у вас нету премиума? Узнать больше:",
                    inline=False)
    embed.add_field(name="/premium", value="", inline=False)
    embed.set_footer(text="by bot_real.",
                     icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")
    return embed

async def whitelist_check(ctx):
    data = await reader()
    return ctx.author.id in data["whitelist"]


@bot.slash_command(name='spam', description='Спамит уведомлениями')
async def spam(ctx, arg1: Option(int, min_value=1, max_value=14881488, description="Введите количество сообщений.", required=True),
               arg2: Option(discord.Member, description='Упоминание участника.',required=True),
               *, arg3: Option(str, description="Текст который будет отправляться вместе с вашим соощением(Не обязательно)", required=False)):
    ID = ctx.author.id;IDstr = str(ID);arg3 = str(arg3);arg3 = arg3.replace("None", " ")
    if await whitelist_check(ctx) == True:
        data = await reader()
        await ctx.defer()
        Messages = data["MessagesLeft"][IDstr]
        if (Messages >= arg1) or (ID in data["ExtraPremium"]):
            if ID not in data["ExtraPremium"]:
               data["MessagesLeft"][IDstr] = Messages - arg1
               logging.error(f"{ctx.author.name} used spam command. Messages used : {arg1}. Message : {arg3}. Player : {arg2.name}")
               await JSONUpdate(data)
            else:
                logging.error(f"{ctx.author.name} used spam command. ExtraPremium used. Messages used : {arg1}. Message : {arg3}. Player : {arg2.name}")
            for i in range(arg1):
                await ctx.send(f"{arg2.mention} {arg3} (by {ctx.author.name})", delete_after=1200)
            await ctx.respond(f"Успешно было отпралено {arg1} сообщений!", delete_after=1200)
        else:
            embed = discord.Embed(
                title=f"У вас осталось {Messages} сообщений. Сообщения обновляются каждый день в 10 часов утра.",
                color=0xc800ff,timestamp=datetime.now())
            embed.set_author(name="Вы привысили лимит!")
            embed.set_thumbnail(
            url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ934piXDEG0qsRbrWE1SDvK8z4YELyUxlPgJBnBRQbFg&s")
            embed.set_footer(text="by bot_real.",
                             icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")
            await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)
    else:
        embed = await premiumEmbed(ctx, "Spam")
        await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)

@bot.slash_command(name='all', description='Спамит @everyone но тратит в 5 раз больше сообщений оставшихся за день.')
async def all(ctx, arg1: Option(int, min_value=1,max_value=355,description="Введите количество сообщений", required=True),
              *, arg2: Option(str, description="Введите любой текст к @everyone(необязательно).", required=False)):

    if await whitelist_check(ctx) == True:
        ID = ctx.author.id;IDstr = str(ID);arg2 = str(arg2);arg2 = arg2.replace('None', ' ');data = await reader()
        await ctx.defer()
        Messages = data["MessagesLeft"][IDstr]
        if (Messages >= arg1) or (ID in data["ExtraPremium"]):
            if ID not in data["ExtraPremium"]:
                data["MessagesLeft"][IDstr] = Messages - arg1 * 5
                logging.error(f"{ctx.author.name} used all command. Messages used : {arg1 * 5}. Message : {arg2}")
                await JSONUpdate(data)
            else:
                logging.error(
                    f"{ctx.author.name} used all command. Extra Premium used. Messages used : {arg1 * 5}. Message : {arg2}")
            for i in range(arg1):
                await ctx.send(f"@everyone {arg2} *(by {ctx.author.name})*", delete_after=1200)
            await ctx.respond(f"Успешно было отправлено {arg1} сообщений!", delete_after=1200)
        elif Messages < arg1:
            embed = discord.Embed(
                title=f"У вас осталось {Messages} сообщений. Сообщения обновляются каждый день в 10 часов утра.",
                color=0xc800ff, timestamp=datetime.now())
            embed.set_author(name="Вы привысили лимит!")
            embed.set_thumbnail(
                url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ934piXDEG0qsRbrWE1SDvK8z4YELyUxlPgJBnBRQbFg&s")
            embed.set_footer(text="by bot_real.",
                             icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")
            await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)
    else:
        embed = await premiumEmbed(ctx, "All")
        await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)

@bot.slash_command(name='spam_channels', description='Спамит в каналы которые создает но тратит в 3 раза больше сообщений.')
async def spamChannels(ctx,arg1: Option(int, min_value=1, max_value=500, description="Количество сообщений в 1 канале", required=True),
                       arg2: Option(int,min_value=1, max_value=15, description="Количество каналов куда будет спамить", required=True),
                       arg3: Option(discord.Member, description='Человек', required=True),
                       arg4: Option(str, max_length=30, min_length=1, default="channel", description='Назввание канал(а/ов)', required=False),
                       * ,arg5: Option(str, max_length=1488, description='Сообщение', required=False)):
    if await whitelist_check(ctx) == True:
        ID = ctx.author.id;ID1 = arg3.name;IDstr = str(ID);arg5 = str(arg5);arg5 = arg5.replace('None', ' ');creator = ctx.author.name; arg4 = str(arg4)
        data = await reader()
        await ctx.defer()
        arg4 = arg4.replace(' ', '-');arg4 = arg4.lower()
        try:
            Messages = data["MessagesLeft"][IDstr]
        except:
            Messages = 0
        if (Messages >= arg1) or (ID in data["ExtraPremium"]):
            if ID not in data["ExtraPremium"]:
                mes = arg1*3
                data["MessagesLeft"][IDstr] = Messages - mes
                logging.error(f"{ctx.author.name} used spamChannels command. Messages used : {arg1 * 3}. Name channels : {arg4}. Message : {arg5}. Mention : {arg3}. Channels : {arg2}. Mesagges : {arg1}")
                await JSONUpdate(data)
            else:
                logging.error(f"{ctx.author.name} used spamChannels command. ExtraPremium used. Messages used : {arg1 * 3}. Name channels : {arg4}. Message : {arg5}. Mention : {arg3}. Channels : {arg2}")
            channels = []

             # Создание каналов

            for i in range(arg2):
                await ctx.guild.create_text_channel(f"{arg4}{i}")

            # Получение айди каналов
            for k in range(arg2):
                given_name = arg4+str(k)
                channels.append(discord.utils.get(ctx.guild.channels, name=given_name).id)


            # Спам в созданные каналы
            enable = asyncio.get_event_loop().create_task(spamDef(channels, arg1, 0, arg3, arg5, creator))

            for j in range(1, arg2, 1):
                asyncio.get_event_loop().create_task(spamDef(channels, arg1, j, arg3, arg5, creator))

            e = await enable

            await asyncio.sleep(5)

            # Удаление каналов

            for i in range(arg2):
                given_name = arg4+str(i)
                existing_channel = discord.utils.get(ctx.guild.channels, name=given_name)
                await existing_channel.delete()

            await ctx.respond(f"Успешно было отправлено {arg1} сообщений. В {arg2} каналов. В общем {arg1*arg2} сообщений!", delete_after=1200)

        elif Messages/arg2 < arg1:
            embed = discord.Embed(
                title=f"У вас осталось {Messages} сообщений. Сообщения обновляются каждый день в 10 часов утра.",
                color=0xc800ff, timestamp=datetime.now())
            embed.set_author(name="Вы привысили лимит!")
            embed.set_thumbnail(
                url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ934piXDEG0qsRbrWE1SDvK8z4YELyUxlPgJBnBRQbFg&s")
            embed.set_footer(text="by bot_real.",
                             icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")
            await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)
    else:
        embed = await premiumEmbed(ctx, "Spam_Channels")
        await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)

    # Премиум и т.д

@bot.slash_command(name='left_messages', description='Дает узнать сколько сообщений осталось.')
async def leftMessages(ctx):
    ID = ctx.author.id;IDstr = str(ID)
    data = await reader()
    if await whitelist_check(ctx) == True:
        try:
            MessagesLeft = data["MessagesLeft"][IDstr]
            embed = discord.Embed(
                title=f"У вас осталось {MessagesLeft} сообщений. Сообщения обновляются каждый день.",
                color=0xc800ff,timestamp=datetime.now())
            embed.set_author(name="Сообщений осталось")
            embed.set_thumbnail(
                url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ934piXDEG0qsRbrWE1SDvK8z4YELyUxlPgJBnBRQbFg&s")
            embed.set_footer(text="by bot_real.",
                             icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")
            await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)
        except:
            embed = discord.Embed(
                title=f"У вас нет лимита по отправке сообщений за день!",
                color=0xc800ff,timestamp=datetime.now())
            embed.set_author(name="Сообщений осталось")
            embed.set_thumbnail(
                url="https://avatars.yandex.net/get-games/11374519/2a0000018da3fe471f93632cdda8f3b07ebf/pjpg160x160")
            embed.set_footer(text="by bot_real.",
                             icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")
            await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)
    else:
        embed = await premiumEmbed(ctx, "Left_Messages")
        await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)

@bot.slash_command(name='premium', description='Возможности премиума')
async def premium(ctx):
    embed = discord.Embed(title="**Премиум**", description="Дает все возможности спама и различных команд по типу:",
                          color=0xc800ff,timestamp=datetime.now())
    embed.set_thumbnail(url="https://graph.digiseller.ru/img.ashx?id_d=3564600")
    embed.add_field(name="**spam, spam_channels, all.**",
                    value="Эти команды хороши но у обычного премиума в день только 1000 сообщений. Но есть возможность убрать ограничение по количеству сообщений и это EXTRAPremium. ",
                    inline=True)
    embed.add_field(name="**Стоимости премиума**",
                    value="Обычный премиум - 35 рублей\n EXTRAPremium - нужен обычный премиум + доплата 30 рублей",
                    inline=True)
    embed.set_footer(text="by bot_real.", icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")
    await ctx.response.send_message(embed=embed, delete_after=180)

@bot.slash_command(name='premium_activate', description='Возможности премиума')
async def premiumActivate(ctx, key: Option(str, min_length=29, max_length=29, description="Введите ключ такого формата XXXXX-XXXXX-XXXXX-XXXXX-XXXXX", required=True)):

    ID = ctx.author.id
    data = await reader()

    if (ID in data["whitelist"]) and (ID not in data["ExtraPremium"]):
        embed = discord.Embed(title="Активация премиума", color=0xc800ff, timestamp=datetime.now())
        embed.set_author(name=f"{ctx.author.name}")
        embed.set_thumbnail(url="https://graph.digiseller.ru/img.ashx?id_d=3564600")
        embed.add_field(name="",
                        value="Похоже что у вас уже есть премиум? Мы предлагаем вам купить ExtraPremium чтобы избавиться от лимита сообщений 1000 в день! Узнать больше :",
                        inline=False)
        embed.add_field(name="/premium", value="", inline=False)
        embed.set_footer(text="by bot_real.", icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")

        await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)
    elif key in data["Keys"]:
        data["whitelist"].append(ID)
        data["Keys"].remove(key)
        ID = str(ID)
        data["MessagesLeft"][ID] = 1000
        await JSONUpdate(data)

        embed = discord.Embed(title="Активация премиума", color=0xc800ff, timestamp=datetime.now())
        embed.set_author(name=f"{ctx.author.name}")
        embed.set_thumbnail(url="https://graph.digiseller.ru/img.ashx?id_d=3564600")
        embed.add_field(name="",
                        value=f"Вы успешно активировали ключ ⟪{key}⟫. Теперь вы можете наслаждаться такими функциями как:",
                        inline=True)
        embed.add_field(name="spam, spam_channels, all",
                        value="Но к сожалению у вас еще нету EXTRAPremium поэтому у вас остался лимит 1000 сообщений в день. Узнать сколько сообщений осталось:",
                        inline=True)
        embed.add_field(name="/left_messages", value="", inline=True)
        embed.set_footer(text="by bot_real.", icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")

        await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)
    if (ID in data["whitelist"]) and (ID in data["ExtraPremium"]):
        embed = discord.Embed(title="Активация премиума", color=0xc800ff, timestamp=datetime.now())
        embed.set_author(name=f"{ctx.author.name}")
        embed.set_thumbnail(url="https://graph.digiseller.ru/img.ashx?id_d=3564600")
        embed.add_field(name="",
                        value="У вас уже есть премиум и экстра премиум! Узнать команды:",
                        inline=False)
        embed.add_field(name="/premium", value="", inline=False)
        embed.set_footer(text="by bot_real.", icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")
        await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)
    else:

        embed = discord.Embed(title="Активация премиума", color=0xc800ff, timestamp=datetime.now())
        embed.set_author(name=f"{ctx.author.name}")
        embed.set_thumbnail(url="https://graph.digiseller.ru/img.ashx?id_d=3564600")
        embed.add_field(name="",
                        value=f"К сожалению ключ ⟪{key}⟫ не верен и вы не получили премиум и доступа к командам. Если вы все такие утверждаете что ваш ключ верен тогда обращайтесь в лс администратору. Узнать больше :",
                        inline=False)
        embed.add_field(name="/premium", value="", inline=False)
        embed.set_footer(text="by bot_real.", icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")

        await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)

@bot.slash_command(name='extra_activate', description='Возможности премиума')
async def premiumExtraActivate(ctx, key: Option(str, min_length=30, max_length=30, description="Введите ключ такого формата XXXXX-XXXXX-XXXXX-XXXXX-XXXXXX", required=True)):

    ID = ctx.author.id
    data = await reader()

    if ID not in data["whitelist"]:
        embed = discord.Embed(title="Активация ExtraПремиума", color=0xc800ff, timestamp=datetime.now())
        embed.set_author(name=f"{ctx.author.name}")
        embed.set_thumbnail(url="https://graph.digiseller.ru/img.ashx?id_d=3564600")
        embed.add_field(name="",
                        value="Похоже что у вас нету премиума? Узнать больше:",
                        inline=False)
        embed.add_field(name="/premium", value="", inline=False)
        embed.set_footer(text="by bot_real.", icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")

        await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)
    elif key in data["KeysExtra"]:
        data["ExtraPremium"].append(ID)
        data["KeysExtra"].remove(key)
        ID = str(ID)
        del data["MessagesLeft"][ID]
        await JSONUpdate(data)

        embed = discord.Embed(title="Активация ExtraПремиума", color=0xc800ff, timestamp=datetime.now())
        embed.set_author(name=f"{ctx.author.name}")
        embed.set_thumbnail(url="https://graph.digiseller.ru/img.ashx?id_d=3564600")
        embed.add_field(name="",
                        value=f"Вы успешно активировали ключ ⟪{key}⟫. Теперь вы можете наслаждаться такими функциями как:",
                        inline=True)
        embed.add_field(name="spam, spam_channels, all",
                        value="Но теперь у вас нет лимита по сообщениям в день!",
                        inline=True)
        embed.set_footer(text="by bot_real.", icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")

        await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)
    if (ID in data["whitelist"]) and (ID in data["ExtraPremium"]):
        embed = discord.Embed(title="Активация премиума", color=0xc800ff, timestamp=datetime.now())
        embed.set_author(name=f"{ctx.author.name}")
        embed.set_thumbnail(url="https://graph.digiseller.ru/img.ashx?id_d=3564600")
        embed.add_field(name="",
                        value="У вас уже есть премиум и экстра премиум! Узнать команды:",
                        inline=False)
        embed.add_field(name="/premium", value="", inline=False)
        embed.set_footer(text="by bot_real.", icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")
        await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)

    else:

        embed = discord.Embed(title="Активация ExtraПремиума", color=0xc800ff, timestamp=datetime.now())
        embed.set_author(name=f"{ctx.author.name}")
        embed.set_thumbnail(url="https://graph.digiseller.ru/img.ashx?id_d=3564600")
        embed.add_field(name="",
                        value=f"К сожалению ключ ⟪{key}⟫ не верен и вы не получили ExtraПремиум и доступа к командам. Если вы все такие утверждаете что ваш ключ верен тогда обращайтесь в лс администратору. Узнать больше :",
                        inline=False)
        embed.add_field(name="/premium", value="", inline=False)
        embed.set_footer(text="by bot_real.", icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")

        await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)


@bot.slash_command(name='admin', description='...', guild=1168481058031931422)
async def admin(ctx, arg1: Option(str, required=True), *, arg2: Option(str, default='None', required=False)):
    if ctx.author.id == 794249479389839470:
        if arg1 == 'Get':
            data = await reader()
            embed = discord.Embed(color=0xc800ff,timestamp=datetime.now())
            embed.set_thumbnail(url="https://graph.digiseller.ru/img.ashx?id_d=3564600")
            embed.add_field(name="Data", value=f"{data}", inline=False)
            embed.set_footer(text="by bot_real.", icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")
            await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=10)
        elif arg1 == 'Set':
            arg2 = eval(arg2)
            await JSONUpdate(arg2)
            embed = discord.Embed(color=0xc800ff,timestamp=datetime.now())
            embed.set_thumbnail(url="https://graph.digiseller.ru/img.ashx?id_d=3564600")
            embed.add_field(name="Data succesfull updated!", value=f"New data = {arg2}", inline=False)
            embed.set_footer(text="by bot_real.", icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=4096")
            await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=10)
        else:
            await ctx.response.send_message(f'Arg1 = "Get" or "Set"', ephemeral=True, delete_after=10)


bot.run("MTE5ODk1ODA2MzIwNjUzOTI4NQ.G4DuUi.U9usc0-KG-p8R1roQ5GWR9ibWymqLl84DRWpu4")
