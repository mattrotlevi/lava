import subprocess
import json
import pprint

def start(args):

	help_str = "usage:\n\texec cosmos_db_list ---> lists available cosmos db accounts in subscription"
	
	if(len(args)>0):

		if(args[0][0] == "?"):
			print(help_str)
			return
	
	print("[+] getting cosmos db accounts in subscription... [+]")

	stg_list = subprocess.run(['az','cosmosdb', 'list', '--query', '[].{acct_name:name, resource_group:resourceGroup, database_api:kind, public_access:publicNetworkAccess, firewall_rules:ipRules}'], stdout=subprocess.PIPE)
	stg_list_json = json.loads(stg_list.stdout.decode('utf-8'))

	pprint.pprint(stg_list_json)

