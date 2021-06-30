import subprocess
import json
import pprint

def start(args):
	help_str = "usage:\n\texec cosmos_db_get_keys ---> list cosmos db account keys"
	if(len(args)>0):
		if(args[0][0] == "?"):
			print(help_str)
			return
	
	print("[+] getting names [+]")
	cosmos_info = subprocess.run(['az', 'cosmosdb', 'list', '--query', '[].{name:name, rgrp: resourceGroup} '], stdout=subprocess.PIPE)
	cosmos_info_json = json.loads(cosmos_info.stdout.decode('utf-8'))


	names = []
	rgrps = []
	for info in cosmos_info_json:
		names.append(info['name'])
		rgrps.append(info['rgrp'])

	print("[+] getting cosmos db accounts [+]")
	for i in range(len(names)):
		cosmos_info = subprocess.run(['az', 'cosmosdb', 'keys', 'list', '--name', names[i], '--resource-group', rgrps[i], '--type', 'connection-strings'], stdout=subprocess.PIPE)
		cosmos_info_json = json.loads(cosmos_info.stdout.decode('utf-8'))
		print(names[i], "\n")
		pprint.pprint(cosmos_info_json)



	#server = cosmos_info_json['name']
	#rgroup = cosmos_info_json['rgrp']



	
	


