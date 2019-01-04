import boto3

ec2=boto3.resource('ec2')
security_groups=ec2.security_groups.all()

for security_group in security_groups:
    for rule in security_group.ip_permissions:
        port = str(rule['FromPort'])
        protocol = rule['IpProtocol']
        for ip_address in rule['IpRanges']:
            if ip_address['CidrIp'] == '195.26.158.190/32':

                print(security_group.group_name, port, protocol, ip_address['CidrIp'])
