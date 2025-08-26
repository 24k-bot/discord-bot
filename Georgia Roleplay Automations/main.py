import discord
from discord.ext import commands
from datetime import timedelta, datetime
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("TOKEN")

# Vote tracking
session_voters = set()

# Role restriction
REQUIRED_ROLE_ID = 1383444841479933984

def has_required_role(interaction: discord.Interaction) -> bool:
    return any(role.id == REQUIRED_ROLE_ID for role in interaction.user.roles)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

class VoteView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Vote', style=discord.ButtonStyle.grey, emoji='<:checkmark:1397939627398008962>')
    async def vote_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in session_voters:
            await interaction.response.send_message("You have already voted!", ephemeral=True)
            return
        
        session_voters.add(interaction.user.id)
        vote_count = len(session_voters)
        
        embed = discord.Embed(
            title="Georgia Roleplay Session Vote",
            description="A session vote has been initiated.\nWe need 5 total votes to start the session.",
            color=0xff0000
        )
        
        embed.add_field(
            name="",
            value="Press the button below to cast your vote.\nLet's get this session rolling!",
            inline=False
        )
        
        embed.add_field(
            name="Vote Count:",
            value=f"{vote_count}/5 votes",
            inline=False
        )
        
        if vote_count >= 5:
            embed.add_field(
                name="✅ Session Ready!",
                value="5 votes reached! Session can now be started.",
                inline=False
            )
        
        embed.set_image(url="https://cdn.discordapp.com/attachments/1374063406402764881/1403380983302062160/image.png?ex=6898a963&is=689757e3&hm=11c8239482ed9456c6291cf9769492539b642c794e798a1fc93129f73da9e9b1&")
        
        await interaction.response.edit_message(embed=embed, view=self)
        
        if vote_count < 5:
            await interaction.followup.send(f"Thank you for voting! ({vote_count}/5)", ephemeral=True)
        else:
            await interaction.followup.send("Thank you for voting! Session is ready to start!", ephemeral=True)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.tree.command(name='votesession', description='Start a session vote')
async def vote_session(interaction: discord.Interaction):
    """Start a session vote"""
    if not has_required_role(interaction):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    
    global session_voters
    session_voters.clear()  # Reset votes
    
    embed = discord.Embed(
        title="Georgia Roleplay Session Vote",
        description="A session vote has been initiated.\nWe need 5 total votes to start the session.",
        color=0xff0000
    )
    
    embed.add_field(
        name="",
        value="Press the button below to cast your vote.\nLet's get this session rolling!",
        inline=False
    )
    
    embed.add_field(
        name="Vote Count:",
        value="0/5 votes",
        inline=False
    )
    
    embed.set_image(url="https://cdn.discordapp.com/attachments/1374063406402764881/1403380983302062160/image.png?ex=6898a963&is=689757e3&hm=11c8239482ed9456c6291cf9769492539b642c794e798a1fc93129f73da9e9b1&")
    
    view = VoteView()
    await interaction.response.send_message(content="<@&1383444896551010416>", embed=embed, view=view)

@bot.tree.command(name='session', description='Start a Georgia Roleplay session')
async def session_start(interaction: discord.Interaction):
    """Start a Georgia Roleplay session"""
    if not has_required_role(interaction):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    embed = discord.Embed(
        title="Georgia Roleplay Session Start!",
        description=" We are now officially in session.",
        color=0xff0000
    )
    
    embed.add_field(
        name="Server Information:",
        value="🔹 Owner: ghostbusta1\n🔹 Server Code: georgiaxxx",
        inline=False
    )
    
    embed.add_field(
        name="",
        value="Ensure you're in proper uniform, have your callsigns updated, and follow all community guidelines during this session. Let's keep it realistic, respectful, and professional throughout.\n\nEnjoy the roleplay!",
        inline=False
    )
    
    # Add voter list if there are voters
    if session_voters:
        voter_mentions = [f"<@{user_id}>" for user_id in session_voters]
        embed.add_field(
            name="Session Voters:",
            value=" ".join(voter_mentions),
            inline=False
        )
    
    embed.set_image(url="https://cdn.discordapp.com/attachments/1374063406402764881/1403380983302062160/image.png?ex=6898a963&is=689757e3&hm=11c8239482ed9456c6291cf9769492539b642c794e798a1fc93129f73da9e9b1&")
    
    # Ping role and voters
    ping_content = "<@&1383444896551010416>"
    if session_voters:
        voter_pings = " ".join([f"<@{user_id}>" for user_id in session_voters])
        ping_content += f" {voter_pings}"
    
    await interaction.response.send_message(content=ping_content, embed=embed)

@bot.tree.command(name='ssd', description='Shutdown a Georgia Roleplay session')
async def session_shutdown(interaction: discord.Interaction):
    """Shutdown a Georgia Roleplay session"""
    if not has_required_role(interaction):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    embed = discord.Embed(
        title="Georgia Roleplay Session Shutdown",
        description="The session for Georgia State Roleplay has now been officially shut down.",
        color=0xff0000
    )
    
    embed.add_field(
        name="",
        value="Thank you to everyone who participated. Please exit the server safely and ensure all roleplay scenes are properly concluded.\n\nStay tuned for future session announcements!",
        inline=False
    )
    
    embed.set_image(url="https://cdn.discordapp.com/attachments/1374063406402764881/1403380983302062160/image.png?ex=6898a963&is=689757e3&hm=11c8239482ed9456c6291cf9769492539b642c794e798a1fc93129f73da9e9b1&")
    
    await interaction.response.send_message(content="<@&1383444896551010416>", embed=embed)

@bot.tree.command(name='globban', description='Issue a global ban')
async def global_ban(interaction: discord.Interaction, discord_id: str, reason: str):
    """Issue a global ban with Discord ID and reason"""
    if not has_required_role(interaction):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    embed = discord.Embed(
        title="🚫 Global Ban Issued",
        description="A global ban has been issued by Georgia Roleplay.",
        color=0x8B0000
    )
    
    embed.add_field(
        name="Discord ID:",
        value=f"`{discord_id}`",
        inline=False
    )
    
    embed.add_field(
        name="Reason:",
        value=reason,
        inline=False
    )
    
    embed.add_field(
        name="Issued by:",
        value=interaction.user.mention,
        inline=False
    )
    
    embed.set_image(url="https://cdn.discordapp.com/attachments/1403028628480196710/1403049767067586591/Copy_of_GRP_Banners.png?ex=689774eb&is=6896236b&hm=21c8105f2c5940d32278613a1cb051757e710c092ba0f53aafcdcf8897b176b6&")
    
    await interaction.response.send_message(embed=embed)
    
    # Log to specific channel
    log_channel = bot.get_channel(1403028662231502918)
    if log_channel:
        await log_channel.send(embed=embed)

@bot.tree.command(name='unglobban', description='Remove a global ban')
async def unglob_ban(interaction: discord.Interaction, discord_id: str, reason: str):
    """Remove a global ban with Discord ID and reason"""
    if not has_required_role(interaction):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    embed = discord.Embed(
        title="✅ Global Ban Removed",
        description="A global ban has been removed by Georgia Roleplay.",
        color=0x00ff00
    )
    
    embed.add_field(
        name="Discord ID:",
        value=f"`{discord_id}`",
        inline=False
    )
    
    embed.add_field(
        name="Reason:",
        value=reason,
        inline=False
    )
    
    embed.add_field(
        name="Removed by:",
        value=interaction.user.mention,
        inline=False
    )
    
    embed.set_image(url="https://cdn.discordapp.com/attachments/1403028628480196710/1403049767067586591/Copy_of_GRP_Banners.png?ex=689774eb&is=6896236b&hm=21c8105f2c5940d32278613a1cb051757e710c092ba0f53aafcdcf8897b176b6&")
    
    await interaction.response.send_message(embed=embed)
    
    # Log to specific channel
    log_channel = bot.get_channel(1403028662231502918)
    if log_channel:
        await log_channel.send(embed=embed)

@bot.tree.command(name='nick', description='Change a user\'s nickname')
async def change_nick(interaction: discord.Interaction, user: discord.Member, new_nickname: str):
    """Change a user's nickname"""
    if not has_required_role(interaction):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    
    old_nickname = user.display_name
     
    try: 
        await user.edit(nick=new_nickname) 
         
        embed = discord.Embed( 
            title="📝 Nickname Changed", 
            description="A user's nickname has been updated.",
            color=0x0099ff
        )
        
        embed.add_field(
            name="User:",
            value=user.mention,
            inline=False
        )
        
        embed.add_field(
            name="Old Nickname:",
            value=old_nickname,
            inline=True
        )
        
        embed.add_field(
            name="New Nickname:",
            value=new_nickname,
            inline=True
        )
        
        embed.add_field(
            name="Changed by:",
            value=interaction.user.mention,
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to change this user's nickname.", ephemeral=True)
    except discord.HTTPException:
        await interaction.response.send_message("❌ Failed to change nickname. Please try again.", ephemeral=True)

@bot.tree.command(name='kick', description='Kick a user from the server')
async def kick_user(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    """Kick a user from the server"""
    if not has_required_role(interaction):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    try:
        await user.kick(reason=reason)
        embed = discord.Embed(title="👢 User Kicked", color=0xff9900)
        embed.add_field(name="User:", value=user.mention, inline=False)
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.add_field(name="Kicked by:", value=interaction.user.mention, inline=False)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to kick this user.", ephemeral=True)

@bot.tree.command(name='ban', description='Ban a user from the server')
async def ban_user(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    """Ban a user from the server"""
    if not has_required_role(interaction):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    try:
        await user.ban(reason=reason)
        embed = discord.Embed(title="🔨 User Banned", color=0x8B0000)
        embed.add_field(name="User:", value=user.mention, inline=False)
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.add_field(name="Banned by:", value=interaction.user.mention, inline=False)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to ban this user.", ephemeral=True)

@bot.tree.command(name='timeout', description='Timeout a user')
async def timeout_user(interaction: discord.Interaction, user: discord.Member, minutes: int, reason: str = "No reason provided"):
    """Timeout a user for specified minutes"""
    if not has_required_role(interaction):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    try:
        timeout_until = datetime.now() + timedelta(minutes=minutes)
        await user.timeout(timeout_until, reason=reason)
        embed = discord.Embed(title="⏰ User Timed Out", color=0xffaa00)
        embed.add_field(name="User:", value=user.mention, inline=False)
        embed.add_field(name="Duration:", value=f"{minutes} minutes", inline=False)
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.add_field(name="Timed out by:", value=interaction.user.mention, inline=False)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to timeout this user.", ephemeral=True)

@bot.tree.command(name='servermute', description='Server mute a user')
async def server_mute(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    """Server mute a user"""
    if not has_required_role(interaction):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    try:
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not muted_role:
            await interaction.response.send_message("❌ Muted role not found. Please create a 'Muted' role.", ephemeral=True)
            return
        await user.add_roles(muted_role, reason=reason)
        embed = discord.Embed(title="🔇 User Server Muted", color=0x666666)
        embed.add_field(name="User:", value=user.mention, inline=False)
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.add_field(name="Muted by:", value=interaction.user.mention, inline=False)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to mute this user.", ephemeral=True)

@bot.tree.command(name='unservermute', description='Remove server mute from a user')
async def unserver_mute(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    """Remove server mute from a user"""
    if not has_required_role(interaction):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    try:
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not muted_role:
            await interaction.response.send_message("❌ Muted role not found.", ephemeral=True)
            return
        await user.remove_roles(muted_role, reason=reason)
        embed = discord.Embed(title="🔊 User Server Unmuted", color=0x00ff00)
        embed.add_field(name="User:", value=user.mention, inline=False)
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.add_field(name="Unmuted by:", value=interaction.user.mention, inline=False)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to unmute this user.", ephemeral=True)

bot.run(token)