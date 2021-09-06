from typing import Callable
from synSet import Synonyms, SynSet, Relation
import networkx as nx
import itertools
import semanticsims

class SynsetSemanticAnalyser():
    
    def __init__(self, synsets : dict) -> None:
        self._synsets = synsets
        self._word_to_synsets = SynsetSemanticAnalyser._create_word_to_synsets_dict(synsets)
        
        # Preparing for semantic field analysis
        # Creating graph in which words are connected from hypo to hypernymy
        G = nx.DiGraph()

        for word, word_synsets in self._synsets.items():
            if Relation.HYPERNYM in word_synsets.relations:
                for rel in word_synsets.relations[Relation.HYPERNYM]:
                    G.add_edge(word, rel)

        self._G = G.reverse()
        self._G_max_path = nx.dag_longest_path_length(G)


    def leacock_chodorov_sim(self, words : list, result_strat : Callable, fail_strat : Callable):

        clean_words = list()
        for w in words:
            if w not in self._word_to_synsets:
                fail_strat(w)
            else:
                clean_words.append(w)
        words = clean_words
        print(words)

        for w1, w2 in itertools.combinations(words, 2):
            sinsets1 = self._word_to_synsets[w1]
            sinsets2 = self._word_to_synsets[w2]
            
            lowest = None
            for s1, s2 in itertools.product(sinsets1, sinsets2):
                ancestor = nx.lowest_common_ancestor(self._G, s1, s2)
                if ancestor is None:
                    continue
                # print(nx.shortest_path_length(G, source=s1, target=ancestor))
                # print("ANC: ", ancestor)
                # TODO this is bottleneck and can be improved
                path_len = nx.shortest_path_length(self._G, source=ancestor, target=s1) + nx.shortest_path_length(self._G, source=ancestor, target=s2)
                if lowest == None or lowest > path_len:
                    lowest = path_len
            if lowest != None:
                sim = semanticsims.leakcock_chodorow(lowest, self._G_max_path)
            else:
                sim = 0
            result_strat(w1, w2, sim)


    @staticmethod
    def from_crown(dct):
        synsets = SynsetSemanticAnalyser._parse_crown_in_synsets_dict(dct)
        return SynsetSemanticAnalyser(synsets)

    @staticmethod
    def _parse_crown_in_synsets_dict(dct):
        synsets = dict()
        for synset_id, synset_data in dct.items():
            node = SynSet()
            synsets[synset_id] = node
            # Filling basic synset data
            node.bcs = synset_data['bcs'] # ID of set in which word is pulled into CROWN
            node.dfn = synset_data['def'] # word definition
            node.relations = dict(synset_data['ilrs'].items()) 
            node.id = synset_id

            # Parsing usage
            if ('notes' in synset_data) and ('usage' in synset_data['notes']):
                node.usage = synset_data['notes']['usage']

            # Parsing synonyms
            for syn_raw in synset_data['synonyms']:
                sense = syn_raw['sense']
                word = syn_raw['word']
                syn = Synonyms(sense, word)
                # print("Dosao")
                node.synonyms.append(syn)

        return synsets

    @staticmethod
    def _create_word_to_synsets_dict(synsets : dict):
        result = dict()
        for synset_id, synset in synsets.items():
            for synonym in synset.synonyms:
                if not synonym.word in result:
                    result[synonym.word] = list()
                result[synonym.word].append(synset_id)
        return result
