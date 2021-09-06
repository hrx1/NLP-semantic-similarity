#!/usr/bin/python3
from graph_extraction import dict_of_word_nodes, word_to_synset_map
from synSet import Synonyms, SynSet, Relation
import json

"""
    nodes       - lista idjeva
    data        - mapa: id -> synset
    relation    - relacija
"""
def get_roots_of_nodes(nodes, data, relation = Relation.HYPERNYM):
    roots = set()
    front = set(nodes)
    # next_front = list() 
    visited = set(nodes)
    while len(front) > 0:
        next_front = set()
        for node in front:
            if is_root_node_of_relation(data[node], relation):
                roots.add(node)
            else:
                next_front = next_front.union(data[node].relations[relation])
        front = next_front.difference(visited)
        
    return list(roots)

def is_root_node_of_relation(node : SynSet, relation = Relation.HYPERNYM):
    return (not relation in node.relations)

def is_root_node(node : SynSet):
    return len(node.relations) == 0

def extract_root_nodes_of_relation(dct, relation = Relation.HYPERNYM):
    result = list()
    for k,v in dct.items():
        if(is_root_node_of_relation(v, relation)):
            result.append(k)
    return result

def extract_root_nodes(dct):
    result = list()
    for k,v in dct.items():
        if(is_root_node(v)):
            result.append(k)
    return result

json_path = './crowordnet/cro_wn30_2012-12-13.json'

with open(json_path) as json_file:
    dct = json.load(json_file)

data = dict_of_word_nodes(dct)

print("Successfully extracted {} entities.".format(len(data)))


roots = [data[x] for x in extract_root_nodes(data)]
root_words = [w.word for syns in roots for w in syns.synonyms]

print("Creating word -> synset map")
word_synset = word_to_synset_map(data)

print("Ispis onih koji imaju 2 hiperonima ili vise")
for k,v in data.items():
    if Relation.HYPERNYM in v.relations and len(v.relations[Relation.HYPERNYM]) > 1:
            print(k)

print("Get roots of nodes")
roots_of = get_roots_of_nodes(["ENG30-00002325-v"], data)

if not __name__ == "__main__":
    print("This module should not be imported! Returning...")