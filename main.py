import json
from semantic_analysis import SynsetSemanticAnalyser
from prettytable import PrettyTable
import sys

json_path = './crowordnet/cro_wn30_2012-12-13.json'

EXAMPLES = "pas,mačka,ovca,miš,televizor,računalo"

print("Enter the list of words you wish to compare. Separate words by comma, do not use trailing whitespace and finish by pressing Enter.")
print("Words have to be in nominative.")
print("Example: ")
print(EXAMPLES)
print("Press enter if you wish to use example stated above.")

if len(sys.argv) == 2 and sys.argv[1] != 'time_test':
    words = input()
else:
    words = []
    print("Time testing... Using words from example.")

if len(words) == 0:
    words = EXAMPLES
words = words.split(",")
# print(words)


with open(json_path) as json_file:
    dct = json.load(json_file)

analizator = SynsetSemanticAnalyser.from_crown(dct)

X = PrettyTable()
X.field_names = ["First word", "Second word", "Similarity"]


analizator.leacock_chodorov_sim(
    words, 
    lambda w1, w2, r : X.add_row([w1,w2,"{:.3f}".format(r)]), 
    lambda w : print("Nemam {} u korpusu! Izbacujem.".format(w))
)

print(X)

print("End of program.")