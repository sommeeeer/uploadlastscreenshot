import os
from pathlib import Path

import paramiko
import pyperclip
from dotenv import load_dotenv

load_dotenv()

folder_path = "~/Pictures/Screenshots"
folder = Path(folder_path).expanduser()

file_timestamps = [(file, file.stat().st_mtime) for file in folder.glob("*")]
newest_file_path, newest_timestamp = max(file_timestamps, key=lambda x: x[1])

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(
    hostname=os.getenv("SFTP_HOSTNAME"),
    port=os.getenv("SFTP_PORT"),
    username=os.getenv("SFTP_USERNAME"),
    password=os.getenv("SFTP_PASSWORD"),
    look_for_keys=False,
    allow_agent=False,
)

sftp = ssh.open_sftp()
file_to_save = newest_file_path.name.replace(" ", "_")
sftp.put(
    newest_file_path.absolute(),
    Path(os.getenv("REMOTE_PATH")).joinpath(file_to_save),
),

pyperclip.copy(f"{os.getenv('URL_TO_SERVER')}{file_to_save}")
print(f'File "{newest_file_path.name}" uploaded to "{os.getenv("REMOTE_PATH")}"')
print(f"Link: {os.getenv('URL_TO_SERVER')}{file_to_save}")

sftp.close()
ssh.close()
