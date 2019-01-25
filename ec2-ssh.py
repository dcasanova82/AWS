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


def find_os_distro(host, key):
    username_list = ['centos', 'ec2-user', 'ubuntu']
    for username in username_list:
        try:
            client.connect(hostname=host, username=username)
            print("Connected to " + instance_name)
            print("Username: " + username)
            if username == 'centos':
                os_distro = "centos"
            elif username == 'ec2-user':
                os_distro = "amazon"
            elif username == 'ubuntu':
                os_distro = "ubuntu"
            return os_distro
        except paramiko.ssh_exception.AuthenticationException:
            pass


def commands_exec(os):
    if os in ('amazon', 'centos'):
        commands = ['cat /etc/system-release',
                    'sudo yum erase ntp*',
                    'sudo yum -y install chrony',
                    'sudo service chronyd start',
                    'sudo chkconfig chronyd on',
                    'chronyc sources -v']
    elif os == 'ubuntu':
        commands = ['lsb_release -a',
                    'clear']
    for command in commands:
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)
        output = stdout.read().decode('utf-8')
        print(output)
        error = stderr.read().decode('utf-8')
        print(error)


for instance in instances:
    instance_name = get_instance_name(instance.id)
    key_name = instance.key_name + ".ssh"
    host = instance.public_dns_name

    # define data folder and file
    data_folder = Path("C:/Users/dcasa")
    key_file = data_folder / key_name

    # define Paramiko objects
    key = paramiko.RSAKey.from_private_key_file(key_file)
    client = paramiko.SSHClient().invoke_shell(term='vt100', width=80, height=24)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    os_distro = find_os_distro(host, key)
    commands_exec(os_distro)











