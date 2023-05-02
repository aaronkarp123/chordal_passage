from pychord import Chord
import json

keys = ['Cmaj', 'Dmaj']

major_roman_chords = {
	'I': [1, ''],
	'IIIm7b5': [3, 'm7b5'],
	'#Idim7': [1, '#dim7'],
	'VI': [6, ''],
	'iim': [2, 'm'],
	'#IIdim7': [2, '#dim7'],
	'#IVm7b5': [4, '#m7b5'],
	'VII' : [7, ''],
	'iiim': [3, 'm'],
	'Vm': [5, 'm'],
	'Im6': [1, 'm6'],
	'II': [2, ''],
	'IV': [4, ''],
	'V': [5, ''],
	'bVI': [6, 'b'],
	'bVII': [7, 'b'],
	'#Vdim7': [5, '#dim7'],
	'III': [3, ''],
	'VIIm7b5': [7, 'm7b5'],
	'vim': [6, 'm'],
	'bVI7': [6, 'b7'],
	'IVm7': [4, 'm7'],
	'bII7': [2, 'b7'],
	'bVII9': [7, 'b9'],
	'I/6': [1, ''],
	'I/64': [1, ''],
	'V/64': [1, ''],
	'Idim/6':[1, 'dim'],
	'VIm7b5/64':[6, 'm7b5'],
	'IV/64':[4, '']
	}

major_roman_connections = [
	['IIIm7b5', 'VI', 5],
	['VI', 'iim', 8],
	['#Idim7', 'iim', 5],
	['#IVm7b5', 'VII', 5],
	['VII', 'iiim', 8],
	['#IIdim7', 'iiim', 5],
	['Vm', 'I', 8],
	['I', 'IV', 10],
	['IIIm7b5', 'IV', 5],
	['Im6', 'II', 5],
	['II', 'V', 10],
	['bVI', 'bVII', 5],
	['bVII', 'I', 8],
	['iim', 'V', 10],
	['iim', 'iiim', 10],
	['V', 'iiim', 10],
	['iiim', 'vim', 10],
	['iiim', 'IV', 10],
	['IV', 'iim', 10],
	['IV', 'I/6', 8],
	['I/6', 'iim', 8],
	['IV', 'V', 15],
	['V', 'I', 20],
	['II', 'V', 8],
	['#IVm7b5', 'V', 5],
	['V', 'vim', 10],
	['VIIm7b5', 'III', 5],
	['III', 'vim', 8],
	['#Vdim7', 'vim', 5],
	['IIIm7b5', 'VI', 5],
	['VI', 'iim', 8],
	['#Idim7', 'iim', 5],
	['vim', 'iim', 10],
	['IVm7', 'I', 8],
	['bII7', 'I', 8],
	['IV', 'I', 12],
	['I', 'V', 10],
	['iim', 'I/64', 10],
	['bVI7', 'I/64', 8],
	['bVII9', 'I/64', 8],
	['#IVm7b5', 'I/64', 8],
	['I/64', 'V', 10],
	['Im6', 'V/64', 5],
	['V/64', 'II', 5],
	['IV/64', 'I', 8],
	['I', 'IV/64', 8],
	['Idim/6', 'iim', 5],
	['VIm7b5/64', 'II', 5]
]

major_roman_connections = [list(x) for x in set(tuple(x) for x in major_roman_connections)]

major_base_chords = {}
for roman, vals in major_roman_chords.items():
	major_base_chords[roman] = Chord.from_note_index(note=vals[0], quality=vals[1], scale='Cmaj')

chords = []
connections = []

def invert(notes, inversion):
	if inversion == '6':
		notes.append(notes.pop(0))
	elif inversion == '64':
		notes.append(notes.pop(0))
		notes.append(notes.pop(0))
	return notes

for i in range(12):
	print(i)
	for roman, c in major_base_chords.items():
		c.transpose(1)
		name = str(c)
		notes = c.components()
		if '/' in roman:
			inv = roman.split('/')[1]
			notes = invert(notes, inv)
			name += '/' + inv
		chords.append({'id':name, 'notes':notes, 'mode':'Major'})

	for edge in major_roman_connections:
		c1 = major_base_chords[edge[0]]
		name1 = str(c1)
		if '/' in edge[0]:
			inv = edge[0].split('/')[1]
			name1 += '/' + inv
		c2 = major_base_chords[edge[1]]
		name2 = str(c2)
		if '/' in edge[1]:
			num = edge[1].split('/')[1]
			name2 += '/' + inv
		connections.append({'source':name1, 'target':name2, 'value':edge[2], 'mode':'Major'})

chords = list({v['id']:v for v in chords}.values())
connections = [dict(s) for s in set(frozenset(d.items()) for d in connections)]

ids = [v['id'] for v in chords]
print(ids)

for i in range(len(connections)):
	dic = connections[i]
	if dic['target'] not in ids:
		print("Missing target:", dic['target'])
	if dic['source'] not in ids:
		print("Missing source:", dic['source'])


combined = {'nodes':chords, 'links':connections}

with open('combined.json', 'w') as outfile:
	json.dump(combined, outfile)

with open("chords.json", "w") as outfile:
    json.dump(chords, outfile)

with open("connections.json", "w") as outfile:
    json.dump(connections, outfile)