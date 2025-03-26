import os
import discord
from discord import app_commands
import random
import json
import logging
import shutil
import atexit

from dotenv import load_dotenv

load_dotenv()

FUHRER_IMAGES = [
    'https://cdn.discordapp.com/attachments/1329672215871885385/1344097518685913098/IMG_1888.jpg?ex=67c24edc&is=67c0fd5c&hm=49441768ec2fef65341cb9ef5c4f5178653188a970e23d76d314492e26329138&', 
    'https://cdn.discordapp.com/attachments/1329672215871885385/1343242519949082675/IMG_6177.jpg?ex=67c1d594&is=67c08414&hm=77dd3e85d0715165087a4781b6d012895f1ebfcb2e0fff9e37acf0add4e41631&', 
    'https://cdn.discordapp.com/attachments/1329672215871885385/1342355433490481193/ChalantKingsty.jpg?ex=67c1e72b&is=67c095ab&hm=af7952f27bc9f7786ebbc25a9594fba238bc2a879872ba83e42f3a94d4dd2510&',
    'https://cdn.discordapp.com/attachments/1329672215871885385/1342229693654503494/IMG_1027.png?ex=67c21ad0&is=67c0c950&hm=e14f5a6994c4e75eda167a4bd520fdb13a232a7a307e8d812994b6194520bea0&',
    'https://cdn.discordapp.com/attachments/1329672215871885385/1340902790196625512/IMG_5980.jpg?ex=67c1e449&is=67c092c9&hm=d295565883d4d854b6c3b15b5ad9998691c6ef1a816139f71ed968c88aedee40&',
    'https://media.discordapp.net/attachments/1342337498491392093/1342664802513850408/image.jpg?ex=67c25e8a&is=67c10d0a&hm=cca7d69de2f8536721501558e13d63502743567b74245a76365ad14887877825&=&format=webp&width=612&height=816',
    'https://media.discordapp.net/attachments/1329672215871885385/1340220389820993588/IMG_1118.jpg?ex=67c20bc1&is=67c0ba41&hm=31540f55ae82efc6d313f0820e014b3f6cd9ac0da992972cb0c1bfd69e249262&=&format=webp&width=726&height=968',
    'https://media.discordapp.net/attachments/1329672215871885385/1340218737223139391/IMG_0729.png?ex=67c20a37&is=67c0b8b7&hm=38b940ac7bb0ded393900090bb18e305adbfdaaa91a755117270fcd1aa782078&=&format=webp&quality=lossless&width=501&height=350',
    'https://media.discordapp.net/attachments/1329672215871885385/1340217274090651668/image.jpg?ex=67c208da&is=67c0b75a&hm=8eec2829e4d0a43a8d41a941f923802a16ef85c3bfbc1787f5d8bdd083e77cb0&=&format=webp&width=726&height=968',
    'https://media.discordapp.net/attachments/1329672215871885385/1340124003876212818/IMG_5284.jpg?ex=67c25abc&is=67c1093c&hm=948c954624976a648daff74a077dff00a7afa95e2271dad37636dce763427b1b&=&format=webp&width=726&height=968',
    'https://media.discordapp.net/attachments/1329672215871885385/1340123901249978378/image.jpg?ex=67c25aa4&is=67c10924&hm=605d00cbf5bf986af6630691b3688b7e21802d3d394e755e55f0a26b7bc9b379&=&format=webp&width=726&height=968',
    'https://media.discordapp.net/attachments/1329672215871885385/1339827526138331167/IMG_2007.jpg?ex=67c1ef5f&is=67c09ddf&hm=387a31d3b608f07ed37f5ce7005ae23209c91e3f1065728c452d2d7979f637ac&=&format=webp&width=726&height=968',
    'https://media.discordapp.net/attachments/1329672215871885385/1339826524483878932/IMG_4832.jpg?ex=67c1ee70&is=67c09cf0&hm=fb3fa2dc9f6b92f21df46a03bbe87c3e8e0e905723692343a1863bd5808468de&=&format=webp&width=726&height=968',
    'https://cdn.discordapp.com/attachments/1329672215871885385/1339825450267971595/IMG_0158.jpg?ex=67c1ed70&is=67c09bf0&hm=21a8d6aba1c0c87e1eac23cce0666cd27c6c5c69470981074b118f05bd8d06e8&',
    'https://media.discordapp.net/attachments/1342337498491392093/1344886224183234600/image.png?ex=67c28a66&is=67c138e6&hm=0bdab8f7b37abd72d8320bb0207aa0ecd6c72294564d3d823510a178acb0c23a&=&format=webp&quality=lossless',
    'https://media.discordapp.net/attachments/1342337498491392093/1344886518493478982/image.png?ex=67c28aac&is=67c1392c&hm=ec6a0ec902569ff8b4a77db6baa010d2455f2b62f5383272d05fdc143a5620c6&=&format=webp&quality=lossless'
]

#Setting up my leader
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#Json
class LotteryManager:
    def __init__(self, filename='lottery.txt'):
        self.filename = os.path.join(os.getcwd(), filename)
        self.users = self.load_tickets()
        atexit.register(self.save_tickets)

    def load_tickets(self):
        try:
            if not os.path.exists(self.filename):
                return {}

            with open(self.filename, 'r') as f:
                return json.load(f)

        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading tickets: {e}. Resetting file.")
            return {}

    def add_ticket(self, user_id):
        ticketnumber = str(random.randrange(1,100000000))
        self.users[str(ticketnumber)] = user_id
        self.save_tickets()
        return ticketnumber

    def save_tickets(self):
        try:
            temp_filename = self.filename + ".tmp"
            
            with open(temp_filename, 'w') as f:
                json.dump(self.users, f, indent=4)
            
            shutil.move(temp_filename, self.filename)  # Atomically replace file
            logging.info(f"Successfully saved {len(self.users)} tickets to {self.filename}")
        except IOError as e:
            logging.error(f"Error saving tickets: {e}")

    def clear_data(self):
        self.users = {}
        self.save_tickets()
        logging.warning("All lottery tickets cleared")

    def pick_ticket(self):
        if not self.users:  
            logging.warning("No tickets in the lottery")
            return None
        
        picked = random.choice(list(self.users.values()))
        self.clear_data()
        return picked
    
Lottery = LotteryManager()


class MoneyManager:
    def __init__(self, filename='money.txt', default_balance=200):
        self.filename = filename
        self.default_balance = default_balance
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filename='money_manager.log')
        self.users = self.load_users()

    def load_users(self):
        try:
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            
            if not os.path.exists(self.filename):
                with open(self.filename, 'w') as f:
                    json.dump({}, f)
                logging.info(f"Created new {self.filename}")
                return {}

            with open(self.filename, 'r') as f:
                data = json.load(f)
                logging.info(f"Loaded {len(data)} users from {self.filename}")
                return data

        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading users: {e}")
            return {}

    def add_user(self, user_id):
        user_id = str(user_id)
        if user_id not in self.users:
            self.users[user_id] = self.default_balance
            logging.info(f"Added new user {user_id} with default balance {self.default_balance}")
            self.save_users()

    def get_balance(self, user_id):
        user_id = str(user_id)
        if user_id not in self.users:
            self.add_user(user_id)
        
        return self.users.get(user_id, self.default_balance)

    def update_balance(self, user_id, amount):
        user_id = str(user_id)
        
        if user_id not in self.users:
            self.add_user(user_id)
        
        current_balance = self.users[user_id]
        new_balance = current_balance + amount
        
        if new_balance <= 0:
            new_balance = self.default_balance
        
        self.users[user_id] = new_balance
        
        logging.info(f"User {user_id}: Balance changed from {current_balance} to {new_balance} (delta: {amount})")
        
        self.save_users()
        
        return new_balance

    def save_users(self):
        try:
            users_copy = self.users.copy()
            
            with open(self.filename, 'w') as f:
                json.dump(users_copy, f, indent=4)
            
            logging.info(f"Successfully saved {len(users_copy)} users to {self.filename}")
        except IOError as e:
            logging.error(f"Error saving users: {e}")

Money = MoneyManager()

#Main commands

@tree.command(name="fuhrermoney", description="The amount of money a user has")
@app_commands.describe(
    member="The memebers money u want to see"
)
async def fuhrermoney(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"User {member.mention} has: {Money.get_balance(member.id)}")

@tree.command(name="fuhrerrole", description="Modify a user's role")
@app_commands.describe(
    member="The user whose role you want to change",
    role="The role you want to assign"
)
async def fuhrerrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message("You don't have permission to manage roles.", ephemeral=True)
        return
    
    try:
        await member.edit(roles=[interaction.guild.default_role])
        
        await member.add_roles(role)
        
        await interaction.response.send_message(f"Roled {role.mention} to {member.mention}.")
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to manage roles.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

@tree.command(name="fuhrerban", description="Ban a user from the server")
@app_commands.describe(
    member="The user you want to ban",
    reason="Reason for the ban (optional)"
)
async def fuhrerban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("You don't have permission to ban members.", ephemeral=True)
        return
    
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"Permanently Deported {member.mention}. Reason: {reason}")
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to ban this member.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

@tree.command(name="fuhrerkick", description="Kick a user from the server")
@app_commands.describe(
    member="The user you want to kick",
    reason="Reason for the kick (optional)"
)
async def fuhrerkick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("You don't have permission to kick members.", ephemeral=True)
        return
    
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"Deported {member.mention}. Reason: {reason}")
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to kick this member.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

@tree.command(name="fuhrer", description="Send a random image")
async def fuhrer(interaction: discord.Interaction):
    random_image = random.choice(FUHRER_IMAGES)
    await interaction.response.send_message(random_image)

#gambling yummy no addiction i can stop whenever i want
@tree.command(name="fuhrerroulletewheel", description="Bet on roulette")
async def fuhrerroulletewheel(
    interaction: discord.Interaction, 
    bet: int,
    color: str,
    number: int = None
):
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

    if bet <= 0:
        await interaction.response.send_message("Bet amount must be a positive integer. ❌", ephemeral=True)
        return 
    
    if bet > Money.get_balance(interaction.user.id):
        await interaction.response.send_message(f"You don't have enough money for this bet! ❌ You Have: {Money.get_balance(interaction.user.id)}" , ephemeral=True)
        return 

    color = color.lower()

    if color not in ['red', 'black']:
        await interaction.response.send_message("Color must be either 'red' or 'black'. ❌", ephemeral=True)
        return 
    
    if number is not None and (number not in red_numbers and color == 'red'):
        await interaction.response.send_message("Red must have an odd number'. ❌", ephemeral=True)
    if number is not None and (number not in black_numbers and color == 'black'):
        await interaction.response.send_message("Black must have an even number'. ❌", ephemeral=True)

    number_c = random.randint(1, 36)

    if number_c in red_numbers:
        color_c = 'red'
    elif number_c in black_numbers:
        color_c = 'black'
    else:
        color_c = 'green' #just incase prob wont happen

    color_print = 'black 👨🏿' if color_c == 'black' else 'red 👺' if color_c == 'red' else 'green 🟢'

    await interaction.response.send_message(f"Spin result - Color: {color_print}, Number: {number_c}", ephemeral=True)

    try:
        if number is None:
            if color_c == color:
                Money.update_balance(interaction.user.id, bet)
                await interaction.followup.send(f"Your color was correct! ✅ You won {bet} dollars. New balance: {Money.get_balance(interaction.user.id)}", ephemeral=True)
            else:
                Money.update_balance(interaction.user.id, -bet)
                await interaction.followup.send(f"Your color was incorrect. ❌ You lost {bet} dollars. New balance: {Money.get_balance(interaction.user.id)}", ephemeral=True)
        
        else:
            if number < 1 or number > 36:
                await interaction.followup.send("Number must be between 1 and 36. ❌", ephemeral=True)
                return

            if number == number_c and color == color_c:
                winnings = bet * 35
                Money.update_balance(interaction.user.id, winnings)
                await interaction.followup.send(f"JACKPOT! Your color and number were correct! ✅✅✅ You won {winnings} dollars. New balance: {Money.get_balance(interaction.user.id)}", ephemeral=True)
            else:
                Money.update_balance(interaction.user.id, -bet)
                await interaction.followup.send(f"Your guess was incorrect. ❌ You lost {bet} dollars. New balance: {Money.get_balance(interaction.user.id)}", ephemeral=True)

    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)


slots = ["🍒", "🍋", "🍊", "🍉", "🍇", "⭐", "💎"] 

@tree.command(name="fuhrerslotmachine", description="Slot machine to gamble your money.")
async def fuhrerslotmachine(interaction: discord.Interaction, bet: int):
    if bet <= 0:
        await interaction.response.send_message("Bet amount must be a positive integer. ❌", ephemeral=True)
        return 

    balance = Money.get_balance(interaction.user.id)
    
    if bet > balance:
        await interaction.response.send_message(f"You don't have enough money for this bet! ❌ You have: {balance}", ephemeral=True)
        return 

    slot1 = random.choice(slots)
    slot2 = random.choice(slots)
    slot3 = random.choice(slots)

    result_message = f"The slots were {slot1}{slot2}{slot3}!"
    
    if slot1 == slot2 == slot3:
        winnings = bet * 15
        Money.update_balance(interaction.user.id, winnings)
        result_message += f"\n🎉 JACKPOT! ✅✅✅ You won {winnings} dollars. New balance: {Money.get_balance(interaction.user.id)}"
    elif slot1 == slot2 or slot2 == slot3 or slot1 == slot3:
        winnings = bet * 3
        Money.update_balance(interaction.user.id, winnings)
        result_message += f"\n✅ Two slots matched! You won {winnings} dollars. New balance: {Money.get_balance(interaction.user.id)}"
    else:
        Money.update_balance(interaction.user.id, -bet)
        result_message += f"\n❌ You lost {bet} dollars. New balance: {Money.get_balance(interaction.user.id)}"

    await interaction.response.send_message(result_message, ephemeral=True)

@tree.command(name="fuhrerlotteryticket", description="Purchase a lottery ticket for $100000.")
async def fuhrerlotteryticket(interaction: discord.Interaction):
    balance = Money.get_balance(interaction.user.id)

    if balance >= 100000:
        Money.update_balance(interaction.user.id, -100000)
        ticket = Lottery.add_ticket(interaction.user.id)
        await interaction.response.send_message(f"🎟️ Successfully purchased a lottery ticket! Lottery ID: {ticket}. Remaining Balance: {Money.get_balance(interaction.user.id)}")
    else:
        await interaction.response.send_message(f"You do not have enough money for a lottery ticket. ❌ Current balance: {balance}", ephemeral=True)

@tree.command(name="runlottery", description="Only the bot owner can run this command.")
async def runlottery(interaction: discord.Interaction):
    owner_id = 701932525551091743  # Replace with your actual Discord ID

    if interaction.user.id != owner_id:
        await interaction.response.send_message("❌ You are not authorized to run this command.", ephemeral=True)
        return

    picked = Lottery.pick_ticket()
    
    if picked is None:  # Check if no tickets were in the lottery
        await interaction.response.send_message("❌ No lottery tickets were purchased.", ephemeral=True)
        return

    guild = interaction.guild 
    if guild is None:
        await interaction.response.send_message("❌ This command must be used in a server.", ephemeral=True)
        return

    member = guild.get_member(picked)  
    if member is None:  
        try:
            member = await guild.fetch_member(picked)
        except discord.NotFound:
            await interaction.response.send_message("❌ The winner is not in the server.")
            return

    await interaction.response.send_message(f"🎉 {member.mention} has won the lottery! @everyone")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await tree.sync()
    print(f'Commands synced')


client.run(os.getenv('DISCORD_BOT_TOKEN'))