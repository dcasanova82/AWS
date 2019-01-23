import boto3
import paramiko
from pathlib import Path


# # define Boto3 objects
ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])


def get_instance_name(id):
    ec2_instance = ec2.Instance(id)
    for tag in ec2_instance.tags:
        if tag['Key'] == 'Name':
            return tag['Value']


def find_username(host, key):
    usernames = ['centos', 'ec2-user', 'ubuntu']
    for username in usernames:
        # print("Trying with username ", username)
        try:
            client.connect(hostname=host, username=username, pkey=key)
            print("Connected to " + instance_name)
            print("Username: " + username)
            if username in ('centos', 'ec2-user'):
                command = "cat /etc/system-release"
                return command
            elif username == 'ubuntu':
                command = "lsb_release -a"
                return command
        except paramiko.ssh_exception.AuthenticationException:
            pass
            # print("User ", username, " invalid")


for instance in instances:
    instance_name = get_instance_name(instance.id)
    key_name = instance.key_name + ".ssh"
    host = instance.public_dns_name

    # define data folder and file
    data_folder = Path("C:/Users/dcasa")
    key_file = data_folder / key_name

    # define Paramiko objects
    key = paramiko.RSAKey.from_private_key_file(key_file)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # print("Connecting to " + instance_name)
    command = find_username(host, key)
    print("Executing {}".format(command))
    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read().decode('utf-8'))
    print(stderr.read().decode('utf-8'))








