# Ten-Second Drop Discord Bot

Ten-Second Drop is a Discord bot for timed drops: the owner starts a drop with `/drop`, members see a 10-second countdown and an optional image, then the first person to click the claim button wins and is shown by profile.

## Install

1. Install Python 3.10 or later.
2. Download the project files: `main.py`, `requirements.txt`, and `.env.example`.
3. Create a Discord application and bot in the Discord Developer Portal. Invite the bot to your server with the permissions needed to send messages, embed links, and use application commands.
4. Copy `.env.example` to `.env` and set `DISCORD_TOKEN` to your bot token and `OWNER_ID` to your Discord user ID. Optionally set `DROP_MESSAGE` and `DROP_IMAGE_URL`.
5. Install dependencies and start the bot:

```bash
python -m pip install -r requirements.txt
python main.py
```

## Use

1. Keep the bot running and wait for its slash command to sync.
2. In a server where the bot is installed, run `/drop`. Only the Discord user whose ID is configured as `OWNER_ID` can start drops.
3. Optionally enter a message for that drop. If omitted, the bot uses `DROP_MESSAGE`.
4. The bot posts a 10-second countdown, then enables the Claim drop button. The first member to click wins; the bot updates the post with the winner’s profile.
5. If nobody claims the drop, the button is disabled when the view times out.

---

More Discord bot projects by EnderDevelopment: https://github.com/EnderDevelopment

Project page: https://dash.enderdevelopment.com/community/82808b87-8cd9-45db-9c1f-ebd8eac97e3d?utm_source=github&utm_medium=readme&utm_campaign=auto_publish&utm_content=82808b87-8cd9-45db-9c1f-ebd8eac97e3d
