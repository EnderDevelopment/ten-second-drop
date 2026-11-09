# Discord Timed Drop Bot

Ten-Second Drop is a Discord bot that creates timed drops with a countdown, an optional image, and a claim button. The Discord bot includes an owner-only `/drop` slash command, configurable countdown duration, custom drop messages, winner announcements, and winner profile images.

## Install

1. Install Python 3.10 or newer.
2. Download or clone this project.
3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment:

   Windows:

   ```bash
   .venv\Scripts\activate
   ```

   macOS or Linux:

   ```bash
   source .venv/bin/activate
   ```

5. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Create a `.env` file based on `.env.example`.
7. Set the following values in `.env`:

   ```env
   DISCORD_TOKEN=your_bot_token_here
   OWNER_ID=your_discord_user_id_here
   DROP_MESSAGE=A special drop is here! Be ready to claim it.
   DROP_IMAGE_URL=https://example.com/drop-image.png
   DROP_COUNTDOWN_SECONDS=10
   ```

8. Invite the bot to your Discord server with permissions to use slash commands and send, edit, and embed messages.
9. Start the bot:

   ```bash
   python main.py
   ```

## Use

1. Start the bot and open a channel where it has permission to send messages.
2. Run `/drop`.
3. Optionally provide a custom `message`.
4. Optionally provide a countdown `seconds` value from 1 to 3600.
5. The bot posts a drop embed with the countdown and disables the claim button.
6. When the countdown ends, the claim button becomes available.
7. The first user to click `Claim drop` wins.
8. The bot edits the message to show the winner's mention, display name, and avatar.

Only the Discord user whose ID is set in `OWNER_ID` can start a drop. Other users receive a private permission message. A drop automatically disables its button after the view timeout if it has not been claimed.

---

More Discord bot projects by EnderDevelopment: https://github.com/EnderDevelopment

Project page: https://dash.enderdevelopment.com/community/82808b87-8cd9-45db-9c1f-ebd8eac97e3d?utm_source=github&utm_medium=readme&utm_campaign=auto_publish&utm_content=82808b87-8cd9-45db-9c1f-ebd8eac97e3d
