### Program used to parse CroWn v1. into graph  

from synSet import SynSet, Synonyms

def dict_of_word_nodes(dct):
    result_list = dict()

    for k, v in dct.items():
        node = SynSet()
        result_list[k] = node
        # TODO popuni node
        node.bcs = v['bcs'] # Postoje 3 seta rijeci, bcs je njihov identifikator
        node.dfn = v['def'] # definicija rijeci
        node.relations = dict(v['ilrs'].items()) 
        node.id = k

        # print(k)

        if ('notes' in v) and ('usage' in v['notes']):
            node.usage = v['notes']['usage'] # kako se koristi
        for syn_raw in v['synonyms']:
            sense = syn_raw['sense']
            word = syn_raw['word']
            syn = Synonyms(sense, word)
            # print("Dosao")
            node.synonyms.append(syn)

    return result_list

def word_to_synset_map(synsets : dict):
    result = dict()
    for _, synset in synsets.items():
        for synonym in synset.synonyms:
            if not synonym.word in result:
                result[synonym.word] = list()
            result[synonym.word].append(synset)
    return result


def word_to_synset_ids(synsets : dict):
    result = dict()
    for k, synset in synsets.items():
        for synonym in synset.synonyms:
            if not synonym.word in result:
                result[synonym.word] = list()
            result[synonym.word].append(k)
    return result


if __name__ == "__main__":
    import json
    json_path = './crowordnet/cro_wn30_2012-12-13.json'

    with open(json_path) as json_file:
        dct = json.load(json_file)

    data = dict_of_word_nodes(dct)

    print("Successfully extracted {} entities.".format(len(data)))



