import boto3

ec2 = boto3.resource('ec2')
# security_groups = ec2.security_groups.all()
instances = ec2.instances.all()

ip_add = '195.26.158.190/32'


def remove_sec_group(sg_id):
    for instance in instances:
        sg_list = [security_group['GroupId'] for security_group in instance.security_groups]
        if sg_id in sg_list:
            sg_list.remove(sg_id)
            instance.modify_attribute(Groups=sg_list)
            # print(instance.instance_id, security_group)


remove_sec_group('sg-01b6d21615d40f612')

# def search_groups_by_ip(ip):
#     for security_group in security_groups:
#         for rule in security_group.ip_permissions:
#             for ip_address in rule['IpRanges']:
#                 if ip_address['CidrIp'] == ip:
#                     if rule['IpProtocol'] == '-1':
#                         protocol = 'All'
#                         print(security_group.group_id, security_group.group_name, protocol, ip_address['CidrIp'])
#                         # security_group.revoke_ingress(CidrIp=ip, IpProtocol=rule['IpProtocol'])
#                     else:
#                         fromPort = rule['FromPort']
#                         toPort = rule['ToPort']
#                         protocol = rule['IpProtocol']
#                         print(security_group.group_id, security_group.group_name, protocol, fromPort, toPort,
#                               ip_address['CidrIp'])
#                 else:
#                     break
#     print('IP not found in Security Groups')
#
#
# search_groups_by_ip(ip_add)
#
