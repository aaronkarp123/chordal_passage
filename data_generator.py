from pychord import Chord
import json

keys = ['Cmaj', 'Dmaj']

roman_chords = {
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
	'I/3': [1, ''],
	'I/5': [1, '']
	}

roman_connections = [
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
	['IV', 'I/3', 8],
	['I/3', 'iim', 8],
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
	['iim', 'I/5', 10],
	['bVI7', 'I/5', 8],
	['bVII9', 'I/5', 8],
	['#IVm7b5', 'I/5', 8],
	['I/5', 'V', 10],
	['IVm7', 'I', 8],
	['bII7', 'I', 8],
	['IV', 'I', 12],
	['I', 'V', 10]
]

roman_connections = [list(x) for x in set(tuple(x) for x in roman_connections)]

major_base_chords = {}
for roman, vals in roman_chords.items():
	major_base_chords[roman] = Chord.from_note_index(note=vals[0], quality=vals[1], scale='Cmaj')

chords = []
connections = []

def equivalents(chord):
	if 'Gb' in chord:
		chord = chord.replace('Gb', 'F#')
	return chord

for i in range(12):
	print(i)
	for roman, c in major_base_chords.items():
		c.transpose(i)
		name = str(c)
		notes = c.components()
		if '/' in roman:
			num = int(roman.split('/')[1])
			name += '/' + str(num)
			if num == 3:
				num = 1
			elif num == 5:
				num = 2
			elif num ==7:
				num = 3
			else:
				print(" ---- UNRECOGNIZED INVERSION ---- ")

			while num > 0:
				notes.append(notes.pop(0))
				num -= 1
		chords.append({'id':name, 'notes':notes})

	for edge in roman_connections:
		c1 = major_base_chords[edge[0]]
		c1.transpose(i)
		name1 = str(c1)
		if '/' in edge[0]:
			num = int(edge[0].split('/')[1])
			name1 += '/' + str(num)
		name1 = equivalents(name1)
		c2 = major_base_chords[edge[1]]
		c2.transpose(i)
		name2 = str(c2)
		if '/' in edge[1]:
			num = int(edge[1].split('/')[1])
			name2 += '/' + str(num)
		name2 = equivalents(name2)
		connections.append({'source':name1, 'target':name2, 'value':edge[2]})

chords = list({v['id']:v for v in chords}.values())
connections = [dict(s) for s in set(frozenset(d.items()) for d in connections)]

combined = {'nodes':chords, 'links':connections}

with open('combined.json', 'w') as outfile:
	json.dump(combined, outfile)

with open("chords.json", "w") as outfile:
    json.dump(chords, outfile)

with open("connections.json", "w") as outfile:
    json.dump(connections, outfile)