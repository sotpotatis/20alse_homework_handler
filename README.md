# 20alse homework.json data file handler

### Background

This project offers a simple Discord bot and a helper script for me to edit the file https://20alse.ssis.nu/homework.json.
This file is a file that contains data about homework for my class, and I wanted to be able to automatically update this data.

The Discord bot and SFTP tests are stored here on GitHub. Note that this is a quick evening project and therefore some parts of the code might miss comments and/or logging. 
I am partly storing this on GitHub for my own convience, but you are of course welcome to use/fork/edit the bot however you'd like.

### Setup

1. Install the requirements: `pip install -r requirements.txt`.
2. Set the following environment variables (if using the provided systemd service, you can edit these variables in `run_homework_bot.sh`):
   1. `SSIS_USERNAME` - The username for your SFTP login to `hem.ssis.nu`.
   2. `SSIS_PASSWORD` - The passwords for your SFTP login to `hem.ssis.nu`.
   3. `HOMEWORK_BOT_TOKEN` - The token that the Discord client should log in with (aka your Discord bot token
   4. Optionally, set `SSH_HOST_KEYS_FILEPATH` for the path to load SSH host key from. If not set, it will load from the default directory.

3. Optionally, use the provided systemctl service files and/or the script to make the bot run on startup
4. To start the Discord bot, run `python3 <CLONED REPO PATH>/discord_bot/main.py`
