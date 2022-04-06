import requests, logging, os, json, datetime
from paramiko import SSHClient, SFTPClient

logger = logging.getLogger(__name__)

def get_homework_file():
    #Make a request to get the homework file
    logger.info("Getting homework file...")
    request = requests.get("https://20alse.ssis.nu/homework.json")

    #Get the request data as JSON
    logger.info("Homework file retrieved.")
    logger.debug(f"File content: {request.json()}")
    return request.json()

def upload_homework_file(new_content:list):
    '''Uploads an updated homework file to the server.

    :param new_content: The new content to upload to the server.'''
    #We want the list to be in order so that the newest homework appears first, and vice versa.
    date_to_datetime = lambda assignment: datetime.datetime.strptime(assignment["due"], "%Y-m-d")
    logger.info("Sorting homework file content by date...")
    new_content = new_content.sort(key=date_to_datetime)
    logger.info("Homework file sorted by date.")
    #Start an SFTP session
    logger.debug(f"Connecting to SFTP with username {os.environ['SSIS_USERNAME']}, password {os.environ['SSIS_PASSWORD']}")
    client = SSHClient()
    logger.info("Logging in to SFTP server...")
    if os.getenv("SSH_HOST_KEYS_FILEPATH") != None:
        SSH_HOST_KEYS_PATH = os.getenv("SSH_HOST_KEYS_FILEPATH")
        logger.info(f"Loading host keys from custom file {SSH_HOST_KEYS_PATH}...")
        client.load_system_host_keys(filename=SSH_HOST_KEYS_PATH)
    else:
        logger.info("Loading host keys from default directory...")
        client.load_system_host_keys()
    logger.info("SSH keys loaded. Trying to log in to server...")
    client.connect(
        "hem.ssis.nu",
        username=os.environ["SSIS_USERNAME"],
        password=os.environ["SSIS_PASSWORD"],
        timeout=5000
    )
    logger.info("Logged in to FTP server.")
    #Replace file content with new content
    logger.info("Replacing file content...")
    #Replace the file content
    sftp = SFTPClient.from_transport(client.get_transport())
    sftp.open("public_html/homework.json", "w").write(json.dumps(new_content, indent=True))
    logger.info("Done replacing file content. Logging out...")
    client.close()

