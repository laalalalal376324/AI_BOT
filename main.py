import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import time
from ai_model import get_class

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MODEL_PATH = os.getenv('MODEL_PATH')
LABELS_PATH = os.getenv('LABELS_PATH')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Привет! Я бот {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def photo(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            if attachment.filename.endswith('.jpg') or attachment.filename.endswith('.png') or attachment.filename.endswith('.jpeg'):
                image_path = f'./images/{attachment.filename}'
                await attachment.save(f'./images/{attachment.filename}')
                #await ctx.send('Фото успешно сохранено!')
                msg = await ctx.send('Фото обрабатывается')
                class_name, confidence_procent = get_class(MODEL_PATH, LABELS_PATH, image_path)
                await msg.delete()
                if confidence_procent > 30:
                    await ctx.send(f'Кажется, что на фото {class_name} с вероятностью {confidence_procent}%')
                else:
                    await ctx.send('Упс, мне не понятно')
                os.remove(image_path)
            else:
                await ctx.send('Не тот формат файла')
                return 
    else:
        await ctx.send('Вы забыли отправить фото')        

bot.run(DISCORD_TOKEN)