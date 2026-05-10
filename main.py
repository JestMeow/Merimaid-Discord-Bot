import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

import zlib
import json
import base64



load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="..", intents=intents)


def parse(input):
    text = input.replace('\\"', '"')
    if text.startswith("(```") and text.endswith("```)"):
        parsed = text[4:-4].strip()
        return parsed
    return

def gen_json(input):
    data = {
        'code': input,
        'mermaid': {
            'theme': 'light'
        }
    }

    return data


def gen_embed_url(obj):
    json_str = json.dumps(obj)
    compressed = zlib.compress(json_str.encode('utf-8'))
    encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')
    url = f'https://mermaid.ink/img/pako:{encoded}'
    
    return url


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


# ==================================================
# ---------------------COMMANDS---------------------
# ==================================================


@bot.command(name='mermaid', description='Test command.')
async def mermaid(ctx, *, arg):
    url = gen_embed_url(gen_json(parse(arg)))
    embed = discord.Embed(
        title='Output',
    )

    embed.set_image(url=url)


    await ctx.send(embed=embed)


@bot.command(name='test', description='Test command.')
async def test(ctx, *, arg):
    await ctx.send(f'Test command received with argument: {arg}')



bot.run(discord_token)