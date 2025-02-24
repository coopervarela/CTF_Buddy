import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import random

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True  

bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store active CTF events.
# Keyed by channel id so you can have one active event per channel.
active_ctf = {}

@bot.command()
async def ctf_lfg(ctx, ctf_name: str):
    """
    Starts a CTF looking-for-group event.
    Example: !ctf_lfg HackTheBox
    """
    # Send a bold message asking users to react.
    message = await ctx.send(f"**React with ✅ if you are looking for a team for {ctf_name}!**")
    await message.add_reaction("✅")
    
    # Store event details: CTF name, message id, and an empty set for participants.
    active_ctf[ctx.channel.id] = {
        "ctf_name": ctf_name,
        "message_id": message.id,
        "participants": set()
    }

@bot.event
async def on_reaction_add(reaction, user):
    # Ignore bot reactions
    if user.bot:
        return
    
    channel = reaction.message.channel
    # Check if there is an active CTF event in this channel.
    if channel.id in active_ctf:
        event = active_ctf[channel.id]
        # Ensure the reaction is on the correct message and is the ✅ emoji.
        if reaction.message.id == event["message_id"] and str(reaction.emoji) == "✅":
            event["participants"].add(user)

@bot.command()
async def ctf_simulate(ctx, count: int = 8):
    """
    Simulates a given number of dummy participants for testing purposes.
    Example: !ctf_simulate 8
    """
    if ctx.channel.id not in active_ctf:
        await ctx.send("**No active CTF event found! Use !ctf_lfg to start one first.**")
        return
    
    event = active_ctf[ctx.channel.id]
    for i in range(count):
        dummy_user = f"DummyUser{i+1}"
        event["participants"].add(dummy_user)
    await ctx.send(f"**Simulated {count} participants for testing!**")

@bot.command()
async def ctf_team(ctx, TS: str):
    """
    Creates teams from the users who reacted.
    Example: !ctf_team TS=4
    """
    try:
        # Extract team size from the TS parameter (format: TS=<number>)
        team_size = int(TS.split('=')[1])
    except Exception:
        await ctx.send("**Invalid team size. Please use the format: TS=<number>**")
        return

    if ctx.channel.id not in active_ctf:
        await ctx.send("**No active CTF event found in this channel!**")
        return

    event = active_ctf[ctx.channel.id]
    participants = list(event["participants"])
    
    if not participants:
        await ctx.send("**No participants found. Make sure people have reacted!**")
        return

    random.shuffle(participants)
    
    # Split participants into teams of the specified size.
    teams = [participants[i:i + team_size] for i in range(0, len(participants), team_size)]
    
    # Build the team message in bold with an extra newline between teams.
    team_msg = f"CTF Teams for {event['ctf_name']}:\n\n"
    for idx, team in enumerate(teams, 1):
        # Use .mention if member is a Discord member; otherwise, use the string (dummy user)
        team_mentions = " ".join(getattr(member, "mention", member) for member in team)
        team_msg += f"Team {idx}: {team_mentions}\n\n"

    await ctx.send(f"**{team_msg}**")
    
    # Clear the event after creating teams.
    del active_ctf[ctx.channel.id]

bot.run(os.environ.get("DISCORD_BOT_TOKEN"))
