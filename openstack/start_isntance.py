# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, random, re
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session


flavor = "ssc" 
private_net = "SNIC Network"
floating_ip_pool_name = None
floating_ip = None
image_name = "image-ID"

identifier = random.randint(1000,9999)

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                #project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print ("user authorization completed.")

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
cfg_file_path =  os.getcwd()+'/consumer1-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata_consumer1= open(cfg_file_path)
else:
    sys.exit("prod-cloud-cfg.txt is not in current working directory")

cfg_file_path =  os.getcwd()+'/consumer2-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata_consumer2 = open(cfg_file_path)
else:
    sys.exit("dev-cloud-cfg.txt is not in current working directory")

cfg_file_path =  os.getcwd()+'/consumer3-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata_consumer3= open(cfg_file_path)
else:
    sys.exit("dev-cloud-cfg.txt is not in current working directory")    
    

secgroups = ['default']

print ("Creating instances ... ")
instance_prod = nova.servers.create(name="consumer1_group16", image=image, flavor=flavor, key_name='<KEY-NAME>',userdata=userdata_consumer1, nics=nics,security_groups=secgroups)
instance_prod2= nova.servers.create(name="consumer2_group16", image=image, flavor=flavor, key_name='<KEY-NAME>',userdata=userdata_consumer2, nics=nics,security_groups=secgroups)
instance_dev = nova.servers.create(name="consumer3_group16", image=image, flavor=flavor, key_name='<KEY-NAME>',userdata=userdata_consumer3, nics=nics,security_groups=secgroups)
inst_status_prod = instance_prod.status
inst_status_prod2 = instance_prod.status
inst_status_dev = instance_dev.status

print ("waiting for 10 seconds.. ")
time.sleep(10)

while inst_status_prod == 'BUILD' or inst_status_dev == 'BUILD' or  inst_status_dev == 'BUILD' :
    print ("Instance: "+instance_prod.name+" is in "+inst_status_prod+" state, sleeping for 5 seconds more...")
    print ("Instance: "+instance_prod2.name+" is in "+inst_status_prod2+" state, sleeping for 5 seconds more...")
    print ("Instance: "+instance_dev.name+" is in "+inst_status_dev+" state, sleeping for 5 seconds more...")
    time.sleep(5)
    instance_prod = nova.servers.get(instance_prod.id)
    inst_status_prod = instance_prod.status
    instance_dev = nova.servers.get(instance_dev.id)
    inst_status_dev = instance_dev.status
    instance_prod2 = nova.servers.get(instance_dev.id)
    inst_status_prod2 = instance_dev.status

ip_address_prod = None
for network in instance_prod.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_prod = network
        break
if ip_address_prod is None:
    raise RuntimeError('No IP address assigned!')

ip_address_prod2 = None
for network in instance_prod2.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_prod2= network
        break
if ip_address_prod2 is None:
    raise RuntimeError('No IP address assigned!')

ip_address_dev = None
for network in instance_dev.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_dev = network
        break
if ip_address_dev is None:
    raise RuntimeError('No IP address assigned!')

print ("Instance: "+ instance_prod.name +" is in " + inst_status_prod + " state" + " ip address: "+ ip_address_prod)
print ("Instance: "+ instance_prod2.name +" is in " + inst_status_prod2 + " state" + " ip address: "+ ip_address_prod2)
print ("Instance: "+ instance_dev.name +" is in " + inst_status_dev + " state" + " ip address: "+ ip_address_dev)