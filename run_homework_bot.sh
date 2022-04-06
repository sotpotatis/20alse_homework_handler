#!/bin/bash
#Set environment variables
export PYTHONPATH="/home/ubuntu/20alse_homework_handler"
export SSIS_USERNAME="<USERNAME>"
export SSIS_PASSWORD="<PASSWORD>"
export HOMEWORK_BOT_TOKEN="<DISCORD TOKEN>"
python3 /home/ubuntu/20alse_homework_handler/discord_bot/main.py
