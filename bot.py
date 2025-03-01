import discord
import random
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv  # Import dotenv
from flask import Flask
import threading

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    print("Error: DISCORD_BOT_TOKEN not found in the .env file!")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True  # Add this line to enable the message content intent

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Create a Flask app to simulate HTTP traffic (needed for Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=8000)

# Start the Flask server in a separate thread
thread = threading.Thread(target=run_flask)
thread.start()

# List of random images
FUHRER_IMAGES = [
    'https://cdn.discordapp.com/attachments/1329672215871885385/1344097518685913098/IMG_1888.jpg?ex=67c24edc&is=67c0fd5c&hm=49441768ec2fef65341cb9ef5c4f5178653188a970e23d76d314492e26329138&', 
    'https://cdn.discordapp.com/attachments/1329672215871885385/1343242519949082675/IMG_6177.jpg?ex=67c1d594&is=67c08414&hm=77dd3e85d0715165087a4781b6d012895f1ebfcb2e0fff9e37acf0add4e41631&', 
    'https://cdn.discordapp.com/attachments/1329672215871885385/1342355433490481193/ChalantKingsty.jpg?ex=67c1e72b&is=67c095ab&hm=af7952f27bc9f7786ebbc25a9594fba238bc2a879872ba83e42f3a94d4dd2510&',
    'https://cdn.discordapp.com/attachments/1329672215871885385/1342229693654503494/IMG_1027.png?ex=67c21ad0&is=67c0c950&hm=e14f5a6994c4e75eda167a4bd520fdb13a232a7a307e8d812994b6194520bea0&',
    'https://cdn.discordapp.com/attachments/1329672215871885385/1340902790196625512/IMG_5980.jpg?ex=67c1e449&is=67c092c9&hm=d295565883d4d854b6c3b15b5ad9998691c6ef1a816139f71ed968c88aedee40&',
    'I hate Niggers',
    'https://media.discordapp.net/attachments/1342337498491392093/1342664802513850408/image.jpg?ex=67c25e8a&is=67c10d0a&hm=cca7d69de2f8536721501558e13d63502743567b74245a76365ad14887877825&=&format=webp&width=612&height=816',
    'https://media.discordapp.net/attachments/1329672215871885385/1340220389820993588/IMG_1118.jpg?ex=67c20bc1&is=67c0ba41&hm=31540f55ae82efc6d313f0820e014b3f6cd9ac0da992972cb0c1bfd69e249262&=&format=webp&width=726&height=968',
    'https://media.discordapp.net/attachments/1329672215871885385/1340218737223139391/IMG_0729.png?ex=67c20a37&is=67c0b8b7&hm=38b940ac7bb0ded393900090bb18e305adbfdaaa91a755117270fcd1aa782078&=&format=webp&quality=lossless&width=501&height=350',
    'https://media.discordapp.net/attachments/1329672215871885385/1340217274090651668/image.jpg?ex=67c208da&is=67c0b75a&hm=8eec2829e4d0a43a8d41a941f923802a16ef85c3bfbc1787f5d8bdd083e77cb0&=&format=webp&width=726&height=968',
    'https://media.discordapp.net/attachments/1329672215871885385/1340124003876212818/IMG_5284.jpg?ex=67c25abc&is=67c1093c&hm=948c954624976a648daff74a077dff00a7afa95e2271dad37636dce763427b1b&=&format=webp&width=726&height=968',
    'https://media.discordapp.net/attachments/1329672215871885385/1340123901249978378/image.jpg?ex=67c25aa4&is=67c10924&hm=605d00cbf5bf986af6630691b3688b7e21802d3d394e755e55f0a26b7bc9b379&=&format=webp&width=726&height=968',
    'stfu nigger',
    'https://media.discordapp.net/attachments/1329672215871885385/1339827526138331167/IMG_2007.jpg?ex=67c1ef5f&is=67c09ddf&hm=387a31d3b608f07ed37f5ce7005ae23209c91e3f1065728c452d2d7979f637ac&=&format=webp&width=726&height=968',
    'https://media.discordapp.net/attachments/1329672215871885385/1339826524483878932/IMG_4832.jpg?ex=67c1ee70&is=67c09cf0&hm=fb3fa2dc9f6b92f21df46a03bbe87c3e8e0e905723692343a1863bd5808468de&=&format=webp&width=726&height=968',
    'https://cdn.discordapp.com/attachments/1329672215871885385/1339825450267971595/IMG_0158.jpg?ex=67c1ed70&is=67c09bf0&hm=21a8d6aba1c0c87e1eac23cce0666cd27c6c5c69470981074b118f05bd8d06e8&',
    'https://media.discordapp.net/attachments/1342337498491392093/1344886224183234600/image.png?ex=67c28a66&is=67c138e6&hm=0bdab8f7b37abd72d8320bb0207aa0ecd6c72294564d3d823510a178acb0c23a&=&format=webp&quality=lossless',
    'https://media.discordapp.net/attachments/1342337498491392093/1344886518493478982/image.png?ex=67c28aac&is=67c1392c&hm=ec6a0ec902569ff8b4a77db6baa010d2455f2b62f5383272d05fdc143a5620c6&=&format=webp&quality=lossless'
]

# Event: Bot ready
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()  # Force sync commands
        print(f"Logged in as {bot.user.name}")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# /fuhrer command - Sends a random image
@tree.command(name="fuhrer", description="Sends a random Fuhrer image")
async def fuhrer(interaction: discord.Interaction):
    try:
        image = random.choice(FUHRER_IMAGES)
        await interaction.response.send_message(image)
    except Exception:
        await interaction.response.send_message("An error occurred while sending the image.", ephemeral=True)

# /fuhrerban command - Bans a user
@tree.command(name="fuhrerban", description="Bans a user from the server")
@app_commands.describe(member="The member to ban", reason="Reason for the ban")
async def fuhrerban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("🚫 You don't have permission to ban members!", ephemeral=True)
        return

    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"✅ {member.mention} was banned for: {reason}")
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to ban this member!", ephemeral=True)
    except Exception:
        await interaction.response.send_message("⚠️ An error occurred while banning the member.", ephemeral=True)

# /fuhrerkick command - Kicks a user
@tree.command(name="fuhrerkick", description="Kicks a user from the server")
@app_commands.describe(member="The member to kick", reason="Reason for the kick")
async def fuhrerkick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("🚫 You don't have permission to kick members!", ephemeral=True)
        return

    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"✅ {member.mention} was kicked for: {reason}")
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to kick this member!", ephemeral=True)
    except Exception:
        await interaction.response.send_message("⚠️ An error occurred while kicking the member.", ephemeral=True)

# /fuhrerrole command - Changes a user's role (removes previous roles)
@tree.command(name="fuhrerrole", description="Assigns a new role and removes old roles")
@app_commands.describe(member="The member to change role", role="The new role to assign")
async def fuhrerrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message("🚫 You don't have permission to manage roles!", ephemeral=True)
        return

    try:
        # Remove all roles except @everyone
        for old_role in member.roles[1:]:  
            await member.remove_roles(old_role)

        # Assign new role
        await member.add_roles(role)
        await interaction.response.send_message(f"✅ {member.mention} is now assigned the role: {role.name}")
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to manage this role!", ephemeral=True)
    except Exception:
        await interaction.response.send_message("⚠️ An error occurred while changing the role.", ephemeral=True)

# Run the bot
bot.run(TOKEN)
