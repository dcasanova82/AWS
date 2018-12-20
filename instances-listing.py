import boto3
import csv

ec2=boto3.resource('ec2')
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
volumes = ec2.volumes.all()

gb_cost=0
instance_cost=0
vol_cost=0
storage_cost=0
ec2_cost=0
total_cost=0
vol_type=''
row=[]
tagged_instances=[]
# test, Disney, production
environment='Disney'
filename=environment+'.csv'
for instance in instances:
    for tag in instance.tags:
        if tag['Key'] == 'Env' and tag['Value'] == environment:
            tagged_instances.append(instance.instance_id)

with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    header=['Resource Nance','Resource Id','Resource Type','Resource SubType','Monthly Cost']
    writer.writerow(header)
    for tagged_instance in tagged_instances:
        for instance in instances:
            if instance.instance_id==tagged_instance:
                if instance.instance_type == 't2.micro':
                    ec2_per_hour = 0.0116
                elif instance.instance_type == 't2.small':
                    ec2_per_hour = 0.023
                elif instance.instance_type == 't2.medium':
                    ec2_per_hour = 0.0464
                elif instance.instance_type == 't2.large':
                    ec2_per_hour = 0.0928
                elif instance.instance_type == 'm5.large':
                    ec2_per_hour = 0.096
                elif instance.instance_type == 'm5.xlarge':
                    ec2_per_hour = 0.192
                elif instance.instance_type == 'm5.2xlarge':
                    ec2_per_hour = 0.384
                else:
                    ec2_per_hour = 0
                instance_cost = ec2_per_hour * 24 * 30
                for tag in instance.tags:
                    if tag['Key']=='Name' and tag['Value'] != '':
                        instance_name=tag['Value']
                instance_row = [instance_name, instance.instance_id, 'Server',instance.instance_type, '{0:.4g}'.format(instance_cost)]
                writer.writerow(instance_row)
                for volume in instance.block_device_mappings:
                    for vol in volumes:
                        if volume['Ebs']['VolumeId']==vol.volume_id:
                            if vol.volume_type=='standard':
                                gb_cost=0.05
                                vol_subtype='Magnetic'
                            elif vol.volume_type=='gp2':
                                gb_cost=0.10
                                vol_subtype = 'Solid State'
                            vol_cost=gb_cost*vol.size
                            vol_type=vol_subtype+' '+str(vol.size)+' GB'
                            volume_row = ['' ,volume['Ebs']['VolumeId'], 'Storage', vol_type, vol_cost]
                            writer.writerow(volume_row)
                            storage_cost=storage_cost+vol_cost
                ec2_cost=instance_cost+storage_cost
                total_cost=total_cost+ec2_cost
                row=['','','','Instance Cost',ec2_cost]
                storage_cost=0
                instance_cost=0
                writer.writerow(row)
                writer.writerow([])
    row = ['', '', '', 'Total Cost', total_cost]
    writer.writerow(row)
f.close()
