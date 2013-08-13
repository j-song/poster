from node import *
import cPickle as pickle
import sys
import re

f = open('hp.obo', 'r')

code_to_term = {}
line = ('','','')
curr_term = None

for l in f:
	line = str.partition(l.rstrip(),': ')
	if line[0] == '[Term]':
		curr_term = Term()
	elif line[0] == 'id':
		curr_term.code = line[2]
		code_to_term[curr_term.code] = curr_term
	elif line[0] == 'name':
		curr_term.name = line[2]
	elif line[0] == 'is_a':
		curr_term.parents.append(str.partition(line[2]," ")[0])
	elif line[0] == 'alt_id':
		code_to_term[line[2]] = curr_term
		
f.close()

for code in code_to_term:
	curr_term = code_to_term[code]
	if len(curr_term.parents)>0 and isinstance(curr_term.parents[0],str):
		for i in range(len(curr_term.parents)):
			curr_term.parents[i] = code_to_term[curr_term.parents[i]]
			curr_term.parents[i].children.append(curr_term)

hpo_root = code_to_term['HP:0000001']
hpo_root.map(Node.set_proper_children)
for node in hpo_root:
	node.clean()

terms = sorted(list(set(code_to_term.values())))

sys.setrecursionlimit(10000)
data = {'code_to_term': code_to_term, 'hpo_root': hpo_root, 'terms': terms}
out = open('hpo_data', 'wb')
pickle.dump(data, out)
out.close()
