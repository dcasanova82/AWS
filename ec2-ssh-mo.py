import paramiko
from pathlib import Path


def main():
    # define connection parameters
    key_name = "main.ssh"
    hosts = ["ec2-52-202-56-43.compute-1.amazonaws.com",
             "ec2-54-173-195-183.compute-1.amazonaws.com"]
    username = "ec2-user"

    # define data folder and file
    data_folder = Path("C:/Users/dcasa")
    key_file = data_folder / key_name

    # define download folder
    download_folder = Path("D:/soapLog.zip")

    # define Paramiko objects
    key = paramiko.RSAKey.from_private_key_file(key_file)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for host in hosts:
        client.connect(hostname=host, username=username, pkey=key)
        # Download file
        ftp_client = client.open_sftp()
        ftp_client.get('/mnt/logs/ziplogs/soapLog.log_2019_01_13_13.zip', download_folder)
        ftp_client.close()


main()








