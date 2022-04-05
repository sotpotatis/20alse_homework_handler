import logging, datetime, pytz
from discord_bot import data_handler

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

logger.info("Homework Filehandler by 20alse.")
#Get the homework file
homework_file_contents = data_handler.get_homework_file()

#Clean up old things
today = datetime.datetime.now(tz=pytz.timezone("Europe/Stockholm"))
today_date = today.date() #Get the current date
new_homework_file_contents = homework_file_contents
for homework in homework_file_contents:
    if datetime.datetime.fromisoformat(homework["due"]).date() < (today - datetime.timedelta(days=3)).date(): #Clean up homework that are more than 3 days old
        logger.info(f"Removing old homework: {homework['title']}...")
        new_homework_file_contents.remove(homework)
data_handler.upload_homework_file(new_homework_file_contents)
logger.info("Code done.")
