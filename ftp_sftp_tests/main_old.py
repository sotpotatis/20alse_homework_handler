import logging, datetime, pytz, os
from discord_bot import data_handler
from ftplib import FTP_TLS

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

logger.info("HomeWork Filer handler by 20alse.")
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

#Start an FTP session
logger.debug(f"Connecting to FTP with username {os.environ['SSIS_USERNAME']}, password {os.environ['SSIS_PASSWORD']}")
ftp = FTP_TLS("hem.ssis.nu", user=os.environ["SSIS_USERNAME"], passwd=os.environ["SSIS_PASSWORD"])
logger.info("Logging in to FTP server...")
ftp.login()
logger.info("Logged in to FTP server.")
#Replace file content with new  content
logger.info("Replacing file content...")
with open("homework.json", "wb") as homework_file:
    ftp.storbinary("STOR homework.json", homework_file)
logger.info("Done replacing file content. Logging out...")
ftp.quit()
