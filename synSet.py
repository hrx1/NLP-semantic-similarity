class SynSet:
    def __init__(self):
        self.bcs = None
        self.bcs = None
        self.dfn = None
        self.relations = dict()
        self.usage = None
        self.synonyms = list()
        self.id = None

    def __str__(self):
        res = "{syns:"
        
        res += ",".join([syn.word for syn in self.synonyms])

        if len(self.synonyms) == 0:
            res += 'None'
        
        res += '|hyper:{}'.format(self.relations.get(Relation.HYPERNYM))
        res += "}"
        return res
    def __repr__(self):
        return str(self)

class Synonyms:
    def __init__(self, sense, word):
        self.sense = sense
        self.word = word

class Relation:
    HYPERNYM = 'hypernym'