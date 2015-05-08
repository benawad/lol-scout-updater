import requests
from random import shuffle
import time

key = 'YOUR-API-KEY'

region = 'na'

def changeTextFile(sum_name, region, champ, sum1, sum2, item1, item2, item3, item4, item5, item6, rune_list):
	s_rune = ''
	for i in rune_list:
		s_rune += ',(%s)[%s]' % (i[0], i[1])
	text = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (sum_name, region, champ, sum1, sum2, item1, item2, item3, item4, item5, item6) + s_rune
	print text

	dropbox_filepath = 'FILE-TO-EDIT'

	f = open(filepath, 'w')

	f.write(text)

	f.close()

def getMostWinsChampion(j, potential_champions):
	champion_data = {}
	for i in range(len(j['champions'])):
		champ_id = j['champions'][i]['id']
		if champ_id in potential_champions:
			champion_data[champ_id] = j['champions'][i]['stats']

	highest_champ_id = -1
	highest_wins = -1

	for i in potential_champions:
		if champion_data[i]['totalSessionsWon'] > highest_wins:
			highest_wins = champion_data[i]['totalSessionsWon']
			highest_champ_id = i

	return highest_champ_id


def getSummonerInfo(j):
	potential_champions = []
	item_builds = []
	summoner_spells = []
	rune_list = []
	for i in range(len(j['matches'])):
		participants = j['matches'][i]['participants'][0]
		stats = participants['stats']
		item1 = stats.get('item0', 0)
		item2 = stats.get('item1', 0)
		item3 = stats.get('item2', 0)
		item4 = stats.get('item3', 0)
		item5 = stats.get('item4', 0)
		item6 = stats.get('item5', 0)
		if(item1 == 0 or item2 == 0 or item3 == 0 or item4 == 0 or item5 == 0 or item6 == 0):
			continue
		if(len(participants['runes']) > 8 or len(participants['runes']) < 4):
			continue
		potential_champions.append(participants['championId'])
		item_builds.append([item1, item2, item3, item4, item5, item6])
		runes = []
		for b in range(len(participants['runes'])):
			runes.append([participants['runes'][b]['rank'], participants['runes'][b]['runeId']])
		rune_list.append(runes)
		summoner_spells.append([participants['spell1Id'], participants['spell2Id']])

	return potential_champions, item_builds, summoner_spells, rune_list

def getChampName(id):
	champ_id_r = requests.get('https://global.api.pvp.net/api/lol/static-data/' + region + '/v1.2/champion/' + str(id) + '?api_key=' + key)

	if(champ_id_r.status_code == 200):
		champ_id_j = champ_id_r.json()
		return champ_id_j['name']
	else:
		raise KeyError('cound not connect when getting the name of the champion for the id = ' + str(highest_champ_id))

# def getItemNames(item_build):
# 	item_names = []
# 	for i in range(len(item_build)):
# 		item = item_build[i]
# 		item_r = requests.get('https://global.api.pvp.net/api/lol/static-data/'+region+'/v1.2/item/'+str(item)+'?api_key=' + key)
# 		if (item_r.status_code == 200):
# 			item_names.append(item_r.json()['name'])
# 		else:
# 			print 'https://global.api.pvp.net/api/lol/static-data/'+region+'/v1.2/item/'+str(item)+'?api_key=' + key
# 			raise KeyError('could not connect when getting this item id = ' + str(item))
# 	return item_names

def getSummonerSpellName(summoner_spell1, summoner_spell2):
	one_r = requests.get('https://global.api.pvp.net/api/lol/static-data/'+region+'/v1.2/summoner-spell/'+str(summoner_spell1)+'?api_key=' + key)
	two_r = requests.get('https://global.api.pvp.net/api/lol/static-data/'+region+'/v1.2/summoner-spell/'+str(summoner_spell2)+'?api_key=' + key)
	if (one_r.status_code == 200 and two_r.status_code == 200):
		j1 = one_r.json()
		j2 = two_r.json()
		return j1['name'], j2['name']
	else:
		raise KeyError('could not connect when getting the summoner spell id for ' + str(summoner_spell1) + ' or ' + str(summoner_spell2))

def meets_requirements(sum_name):
	id_r = requests.get('https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.4/summoner/by-name/' + sum_name + '?api_key=' + key)
	if(id_r.status_code == 200):
		id_j = id_r.json()
		sum_name_stripped = sum_name
		sum_name_stripped = sum_name_stripped.lower()
		sum_name_stripped = sum_name_stripped.encode('utf8')
		sum_name_stripped = sum_name_stripped.replace(" ", "")
		sum_id = id_j[sum_name_stripped]['id']

		rg_r = requests.get('https://' + region + '.api.pvp.net/api/lol/' + region + '/v2.2/matchhistory/' + str(sum_id) + '?api_key=' + key)
		if(rg_r.status_code == 200):
			potential_champions, item_builds, summoner_spells, rune_list = getSummonerInfo(rg_r.json())
			
			if(not potential_champions):
				return False

			rs_r = requests.get('https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.3/stats/by-summoner/' + str(sum_id) + '/ranked?api_key=' + key)

			if(rs_r.status_code == 200):
				rs_j = rs_r.json()
				highest_champ_id = getMostWinsChampion(rs_j, potential_champions)

				champion_id = highest_champ_id
				loc = potential_champions.index(champion_id)
				item_build = item_builds[loc]
				summoner_spell1 = summoner_spells[loc][0]
				summoner_spell2 = summoner_spells[loc][1]
				rune_page = rune_list[loc]

				try:
					champ_name = getChampName(champion_id)
					item_build_name = item_build
					spell_name1, spell_name2 = getSummonerSpellName(summoner_spell1, summoner_spell2)
					changeTextFile(sum_name, region, champ_name, spell_name1, spell_name2, item_build_name[0], item_build_name[1], item_build_name[2], item_build_name[3], item_build_name[4], item_build_name[5], rune_page)
					return True
				except KeyError as e:
					print e
			else:
				print 'cound not connect when getting ' + sum_name + ' ranked stats'

		else:
			print 'could not connect when getting ' + sum_name + ' recent games'
	else:
		print id_r.text
		print 'could not connect when getting ' + sum_name + ' id'

	return False



chall_r = requests.get('https://' + region + '.api.pvp.net/api/lol/' + region + '/v2.5/league/challenger?type=RANKED_SOLO_5x5&api_key=' + key)

if(chall_r.status_code == 200):

	chall_J = chall_r.json()

	potential_players  = []

	for i in range(len(chall_J['entries'])):
		potential_players.append(chall_J['entries'][i]['playerOrTeamName'])

	shuffle(potential_players)

	for i in potential_players:
		if(meets_requirements(i)):
			break
		time.sleep(20)

else:
	print "could not connect when getting challenger players"


























