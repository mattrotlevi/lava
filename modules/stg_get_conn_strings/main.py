import subprocess
import json
import pprint

def start(args):
	help_str = "usage:\n\texec stg_get_conn_strings ---> list storage account connection strings"
	if(len(args)>0):
		if(args[0][0] == "?"):
			print(help_str)
			return
	
	print("[+] getting storage account list [+]")
	storage_info = subprocess.run(['az', 'storage', 'account', 'list', '--query', '[].{name:name, rgrp: resourceGroup} '], stdout=subprocess.PIPE)
	storage_info_json = json.loads(storage_info.stdout.decode('utf-8'))


	names = []
	rgrps = []
	for info in storage_info_json:
		names.append(info['name'])
		rgrps.append(info['rgrp'])

	print("[+] getting storage account connection strings [+]")
	for i in range(len(names)):
		storage_info = subprocess.run(['az', 'storage', 'account', 'show-connection-string', '--name', names[i], '--resource-group', rgrps[i]], stdout=subprocess.PIPE)
		storage_info_json = json.loads(storage_info.stdout.decode('utf-8'))
		print(names[i], "\n")
		pprint.pprint(storage_info_json)



	#server = storage_info_json['name']
	#rgroup = storage_info_json['rgrp']



	
	


