import os
from dotenv import load_dotenv
import discord
import random

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True  

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

# Dictionary to store active CTF events.
active_ctf = {}

@bot.event
async def on_ready():
    await tree.sync()  # Sync slash commands with Discord
    print(f"Logged in as {bot.user}")

@tree.command(name="ctf_lfg", description="Start a CTF looking-for-group event.")
async def ctf_lfg(interaction: discord.Interaction, ctf_name: str):
    """
    Starts a CTF looking-for-group event.
    Example: /ctf_lfg HackTheBox
    """
    message = await interaction.channel.send(f"**React with ✅ if you are looking for a team for {ctf_name}!**")
    await message.add_reaction("✅")
    
    active_ctf[interaction.channel.id] = {
        "ctf_name": ctf_name,
        "message_id": message.id,
        "participants": set()
    }
    await interaction.response.send_message(f"CTF event for {ctf_name} started!", ephemeral=True)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    
    channel = reaction.message.channel
    if channel.id in active_ctf:
        event = active_ctf[channel.id]
        if reaction.message.id == event["message_id"] and str(reaction.emoji) == "✅":
            event["participants"].add(user)

@tree.command(name="ctf_simulate", description="Simulate dummy participants for testing.")
async def ctf_simulate(interaction: discord.Interaction, count: int = 8):
    if interaction.channel.id not in active_ctf:
        await interaction.response.send_message("**No active CTF event found! Use /ctf_lfg first.**", ephemeral=True)
        return
    
    event = active_ctf[interaction.channel.id]
    for i in range(count):
        dummy_user = f"DummyUser{i+1}"
        event["participants"].add(dummy_user)
    
    await interaction.response.send_message(f"**Simulated {count} participants for testing!**", ephemeral=True)

@tree.command(name="ctf_team", description="Create teams from participants.")
async def ctf_team(interaction: discord.Interaction, team_size: int):
    if interaction.channel.id not in active_ctf:
        await interaction.response.send_message("**No active CTF event found!**", ephemeral=True)
        return

    event = active_ctf[interaction.channel.id]
    participants = list(event["participants"])
    
    if not participants:
        await interaction.response.send_message("**No participants found. Make sure people have reacted!**", ephemeral=True)
        return

    random.shuffle(participants)
    teams = [participants[i:i + team_size] for i in range(0, len(participants), team_size)]
    
    team_msg = f"CTF Teams for {event['ctf_name']}:\n\n"
    for idx, team in enumerate(teams, 1):
        team_mentions = " ".join(getattr(member, "mention", member) for member in team)
        team_msg += f"Team {idx}: {team_mentions}\n\n"

    await interaction.response.send_message(f"**{team_msg}**")
    del active_ctf[interaction.channel.id]

bot.run(os.environ.get("DISCORD_BOT_TOKEN"))
