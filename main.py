import asyncio
import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
DROP_IMAGE_URL = os.getenv("DROP_IMAGE_URL", "").strip()
DROP_MESSAGE = os.getenv("DROP_MESSAGE", "A special drop is here! Be ready to claim it.").strip()
try:
    DROP_COUNTDOWN_SECONDS = int(os.getenv("DROP_COUNTDOWN_SECONDS", "10"))
except ValueError as error:
    raise RuntimeError("DROP_COUNTDOWN_SECONDS must be a whole number from 1 to 3600.") from error
if not 1 <= DROP_COUNTDOWN_SECONDS <= 3600:
    raise RuntimeError("DROP_COUNTDOWN_SECONDS must be between 1 and 3600.")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


class DropView(discord.ui.View):
    def __init__(self, drop_message: str, countdown_seconds: int):
        super().__init__(timeout=300)
        self.drop_message = drop_message
        self.countdown_seconds = countdown_seconds
        self.available = False
        self.claimed = False
        self.message = None

    async def start_countdown(self, message: discord.Message):
        self.message = message
        for remaining in range(self.countdown_seconds, 0, -1):
            embed = discord.Embed(
                title="A drop is coming!",
                description=f"{self.drop_message}\n\n**Claim opens in {remaining} seconds...**",
                color=discord.Color.gold(),
            )
            if DROP_IMAGE_URL:
                embed.set_image(url=DROP_IMAGE_URL)
            await message.edit(embed=embed, view=self)
            await asyncio.sleep(1)

        self.available = True
        self.claim_button.disabled = False
        embed = discord.Embed(
            title="Drop available!",
            description=f"{self.drop_message}\n\nClick **Claim drop** to claim it.",
            color=discord.Color.green(),
        )
        if DROP_IMAGE_URL:
            embed.set_image(url=DROP_IMAGE_URL)
        await message.edit(embed=embed, view=self)

    @discord.ui.button(label="Claim drop", style=discord.ButtonStyle.success, disabled=True)
    async def claim_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.available:
            await interaction.response.send_message("The drop is not open yet.", ephemeral=True)
            return
        if self.claimed:
            await interaction.response.send_message("This drop has already been claimed.", ephemeral=True)
            return

        self.claimed = True
        button.disabled = True
        winner = interaction.user
        embed = discord.Embed(
            title="Drop claimed!",
            description=f"Winner: {winner.mention}\n**{discord.utils.escape_markdown(winner.display_name)}** claimed the drop!",
            color=discord.Color.blurple(),
        )
        embed.set_thumbnail(url=winner.display_avatar.url)
        if DROP_IMAGE_URL:
            embed.set_image(url=DROP_IMAGE_URL)
        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()

    async def on_timeout(self):
        if self.message is not None and not self.claimed:
            for item in self.children:
                item.disabled = True
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Logged in as {bot.user}; synced {len(synced)} slash command(s).")
    except discord.HTTPException as error:
        print(f"Could not sync slash commands: {error}")


@bot.tree.command(name="drop", description="Start a timed drop with a claim button.")
@app_commands.describe(
    message="Optional message to show with this drop",
    seconds="Optional countdown duration in seconds (1-3600)",
)
async def drop(
    interaction: discord.Interaction,
    message: str | None = None,
    seconds: app_commands.Range[int, 1, 3600] | None = None,
):
    if OWNER_ID == 0 or interaction.user.id != OWNER_ID:
        await interaction.response.send_message("You are not allowed to start drops.", ephemeral=True)
        return

    drop_message = message.strip() if message and message.strip() else DROP_MESSAGE
    countdown_seconds = seconds if seconds is not None else DROP_COUNTDOWN_SECONDS
    view = DropView(drop_message, countdown_seconds)
    initial_embed = discord.Embed(
        title="A drop is coming!",
        description=f"{drop_message}\n\n**Claim opens in {countdown_seconds} seconds...**",
        color=discord.Color.gold(),
    )
    if DROP_IMAGE_URL:
        initial_embed.set_image(url=DROP_IMAGE_URL)
    await interaction.response.send_message(embed=initial_embed, view=view)
    response_message = await interaction.original_response()
    asyncio.create_task(view.start_countdown(response_message))


if not TOKEN:
    raise RuntimeError("Set DISCORD_TOKEN in your .env file before starting the bot.")
bot.run(TOKEN)
