# Zachary Smith
# CIT-93 Final Project
# Python Discord Moderation Bot
# built using discord.py

import os
import discord
import random
from random import choice
from discord.ext import commands, tasks

# Set the message intents
intents=discord.Intents.all()

# Create the bot
bot = commands.Bot(
    description='Moderation Bot',
    intents=intents,
    command_prefix="/",  # Change to desired prefix
    case_insensitive=True  # Commands aren't case-sensitive
)
# Remove the default help command
bot.remove_command("help")
bot.author_id = USER-ID-GOES-HERE

# Create custom help command that lists the commands
@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(
        title="Useful help commands",
        description=
        "`/kick` - Kicks a user\n"
        "`/ban` - Bans a user\n"
        "`/unban` - Unbans a user\n"
        "`/gr` - Gives a user a role\n"
        "`/rr` - Removes a role from a user\n"
        "`/cr` - Creates a new role\n"
        "`/8ball` - Consult the magic 8-ball\n"
        "`/rd` - Roll dice\n"
        "`/serverinfo` - Displays info about the server\n",
        color=discord.Color.blue())

    await ctx.send(embed=embed)



# Kick user
@bot.command(description="/kick <user> <reason>")
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kicks a user"""
    await member.kick(reason=reason)

# Ban an account
@bot.command(description="/ban <user> <reason>")
async def ban(ctx, member: discord.Member, *, reason=None):
    """Bans a user"""
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

# Unban an account
@bot.command(description="/unban <user>")
async def unban(ctx, *, member):
    """Unbans a user"""
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    # Loop through ban list
    for ban_entry in banned_users:
        user = ban_entry.user
        # Unban user from ban list
        if (user.name, user.discriminator) == (member_name,
                                                member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

# Give Roles
@bot.command(aliases = ["gr"], description="/give_role <user> <role>")
async def give_role(
    ctx,
    user: discord.Member,
    role: discord.Role,
):
    """gives a role to a specified user"""
    await user.add_roles(role)
    embed = discord.Embed(
        description=f"Successfully given {role.mention} to {user.mention}",
        color=0x336EFF)
    await ctx.send(embed=embed)

# Take Away Roles
@bot.command(aliases= ["rr"], description="/remove_role <user> <role>")
async def remove_role(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    embed = discord.Embed(
        description=
        f"Successfully removed {role.mention} from {user.mention}",
        color=0x336EFF)
    await ctx.send(embed=embed)

# Create Roles
@bot.command(aliases = ["cr"], description="/create_role <name> <color>")
async def CreateRole(ctx, name, *, colour=discord.Colour(0xffffff)):
    """Creates a discord role"""
    guild = ctx.guild
    await guild.create_role(name=name,
                            permissions=discord.Permissions(8),
                            colour=colour)
    embed = discord.Embed(description=f'Role `{name}` has been created',
                            color=0x336EFF)
    await ctx.send(embed=embed)

# .serverinfo - server creation date / unverified users / number of bots      / number of members

@bot.command(description="/serverinfo")
async def serverinfo(ctx):
    """Displays the server information"""
    role_count = len(ctx.guild.roles)
    list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

    serverinfoEmbed = discord.Embed(timestamp=ctx.message.created_at,
                                    color=ctx.author.color)
    serverinfoEmbed.add_field(name='Name',
                                value=f"{ctx.guild.name}",
                                inline=False)
    serverinfoEmbed.add_field(name='Member Count',
                                value=ctx.guild.member_count,
                                inline=False)
    serverinfoEmbed.add_field(name='Verification Level',
                                value=str(ctx.guild.verification_level),
                                inline=False)
    serverinfoEmbed.add_field(name='Highest Role',
                                value=ctx.guild.roles[-2],
                                inline=False)
    serverinfoEmbed.add_field(name='Number of Roles',
                                value=str(role_count),
                                inline=False)
    serverinfoEmbed.add_field(name='Bots',
                                value=','.join(list_of_bots),
                                inline=False)
    await ctx.send(embed=serverinfoEmbed)

# Rolls a dice, takes the number of sides of the dice, and the number of times to be rolled
@bot.command(aliases=["rd"], description="/roll_dice <sides> <amount>")
async def roll_dice(ctx, sides, amount=1):
    """Rolls the specified dice, only rolls one dice unless <amount> is specified"""
    min = 1
    max = int(sides)
    n = []
    for _ in range(int(amount)):
        n.append(random.randint(min, max))
    await ctx.send(f"you rolled {n}")

# Generates a random magic-8ball outcome
@bot.command(name='8ball')
async def magic_eight_ball(ctx):
    response = [
        'Without a doubt.',
        'Outlook good.',
        'Better not tell you now.',
        'Cannot predict now.',
        'My reply is no.',
        'Outlook not so good.',
    ]

    await ctx.send(random.choice(response))

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    change_status.start()

# Ping command to test if bot is online
@bot.command()  
async def ping(ctx):
    await ctx.send('Pong!')

# Set bot status
status = ["Type /help for Command help"]

# Can add more statuses above, and this will loop through them on a timer
@tasks.loop(minutes=30)
async def change_status():
    print("bot changing status")
    await bot.change_presence(activity=discord.Game(choice(status)))

# Create the bot
token = "BOT-TOKEN-GOES-HERE"
bot.run(token)  # Starts the bot
