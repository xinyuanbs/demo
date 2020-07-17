import os
import sys
import json
from functools import reduce
	
def create_wav_scp():
	with open("/nfs/data/raid0/public/primewords_md_2018_set1/data/set1_transcript.json",'r') as f:
		load_dict = json.load(f)
	#sorted
	load_dict = sorted(load_dict, key = lambda e:(e.__getitem__('user_id'),e.__getitem__('id')))

	wav_scp_dir = open("wav.scp", "w+")
	wav_scp_dir_notexist = open("wav_notexist.scp", "w+")
	
	#去重
	list_dict_duplicate_removal = lambda x, y: x if y in x else x + [y]
	load_dict = reduce(list_dict_duplicate_removal, [[], ] + load_dict)
	print("len(load_dict)=" + str(len(load_dict)))

	i = 0
	n = 0
	# N = 0
	for i in range(len(load_dict)):
		########## test
		# if(load_dict[i]['id'] and load_dict[i]['file'] and load_dict[i]['user_id'] and load_dict[i]['length'] and load_dict[i]['text']):
		# 	N += 1
		# print(len(load_dict))
		########## end test


		k = 10001
		num = 0
		n = i
		while(load_dict[n]['user_id'] == load_dict[n-1]['user_id']):
			num += 1
			n -= 1
		k += num

		path = "/nfs/data/raid0/public/primewords_md_2018_set1/data/audio_files/"
		path += load_dict[i]['file'][0]
		path += "/"
		path += load_dict[i]['file'][0:2]
		path += "/"
		path += load_dict[i]['file']

		if(os.path.isfile(path)):
			wav_scp_dir.write(load_dict[i]['user_id'] + 'XX_' + str(k) + ' ')
			wav_scp_dir.write(path + "\n")
		else:
			wav_scp_dir_notexist.write(load_dict[i]['user_id'] + 'XX_' + str(k) + ' ')
			wav_scp_dir_notexist.write(path + '\n')
		i = i + 1
	# print(i)
	# print(N)

def create_spk2utt():
	spk2utt_dir = open("spk2utt", 'w+')
	tmp = None
	for line in open("wav.scp", 'r'):
		uttid = line.split()[0]
		spkid = uttid.split('_')[0]
		# print(spkid + ',' + uttid)
		if(tmp == spkid):
			spk2utt_dir.write(uttid + ' ')
		else:
			if(tmp == None):
				spk2utt_dir.write(spkid + ' ' + uttid + ' ')
			else:
				spk2utt_dir.write('\n' + spkid + ' ' + uttid + ' ')
		tmp = spkid

def create_utt2spk():
	utt2spk_dir = open("utt2spk", 'w+')
	for line in open("wav.scp", 'r'):
		uttid = line.split()[0]
		spkid = uttid.split('_')[0]
		utt2spk_dir.write(uttid + ' ' + spkid + '\n')

def create_spk2gender():
	spk2gender_dir = open("spk2gender", 'w+')
	tmp = None
	for line in open("wav.scp", 'r'):
		uttid = line.split()[0]
		spkid = uttid.split('_')[0]
		if(tmp != spkid):
			spk2utt_dir.write(uttid + ' ')
		else:
			spk2utt_dir.write('\n' + spkid + ' ')
		tmp = spkid

if __name__ == "__main__":
	create_wav_scp()
	create_spk2utt()
	create_utt2spk()
