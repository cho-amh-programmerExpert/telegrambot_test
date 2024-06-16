import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# Define the choices for the action argument
action_choices = [
    app_commands.Choice(name="Kick", value="kick"),
    app_commands.Choice(name="Ban", value="ban"),
    app_commands.Choice(name="Message", value="message"),
    app_commands.Choice(name="Mute", value="mute"),
    app_commands.Choice(name="Unmute", value="unmute"),
    app_commands.Choice(name="Nickname", value="nickname"),
    app_commands.Choice(name="Add Role", value="add_role"),
    app_commands.Choice(name="Remove Role", value="remove_role")
]

# Slash command for various admin actions
@bot.tree.command(name="admin", description="Admin commands")
@app_commands.describe(action="Action to perform", member="Member to act upon", reason="Reason for the action")
@app_commands.choices(action=action_choices)
async def admin_interaction(interaction: discord.Interaction, action: str, member: discord.Member, reason: str = None):
    user = member  # The user object that can be kicked or banned
    channel = interaction.channel  # The channel object to send messages
    try:
        if action == "kick":
            await user.kick(reason=reason)
            await interaction.response.send_message(f"{user.name} has been kicked.")
        elif action == "ban":
            await user.ban(reason=reason)
            await interaction.response.send_message(f"{user.name} has been banned.")
        elif action == "message":
            await channel.send("This is a message from the bot.")
            await interaction.response.send_message("Message sent.")
        elif action == "mute":
            await user.edit(mute=True)
            await interaction.response.send_message(f"{user.name} has been muted.")
        elif action == "unmute":
            await user.edit(mute=False)
            await interaction.response.send_message(f"{user.name} has been unmuted.")
        elif action == "nickname":
            new_nickname = reason  # Using the reason field for the new nickname
            await user.edit(nick=new_nickname)
            await interaction.response.send_message(f"{user.name}'s nickname has been changed to {new_nickname}.")
        elif action == "add_role":
            role = discord.utils.get(interaction.guild.roles, name=reason)  # Using the reason field for the role name
            if role:
                await user.add_roles(role)
                await interaction.response.send_message(f"{role.name} role has been added to {user.name}.")
            else:
                await interaction.response.send_message("Role not found.", ephemeral=True)
        elif action == "remove_role":
            role = discord.utils.get(interaction.guild.roles, name=reason)  # Using the reason field for the role name
            if role:
                await user.remove_roles(role)
                await interaction.response.send_message(f"{role.name} role has been removed from {user.name}.")
            else:
                await interaction.response.send_message("Role not found.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I do not have permission to perform this action.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

# Message event listener
@bot.event
async def on_message(message: discord.Message):
    msg_content = message.content  # The content of the incoming message
    channel = message.channel  # The channel object to send messages
    if msg_content.lower() == "hello bot":
        await channel.send(f"Hello {message.author.name}!")
    await bot.process_commands(message)  # Ensure other commands still work

# Error handling for commands
@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I do not have the necessary permissions to execute this command.")
    else:
        await ctx.send(f"An error occurred: {error}")
 
# To use the command_prefix commands 
@bot.command(name="greet", help="Greets the user")
async def greet(ctx: commands.Context):
    await ctx.send(f"Hello, {ctx.author.name}!")

# Sync the command tree on bot startup
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}!')

# Run the bot
bot.run("MTI1MTkyMTA2NzcwNzIwNzcwMQ.G5j_9f.rSJ_HPM7PGakWS30CeeDo4XF0JcMg_uNUAj3Gw")
