import networkx
import math

def leakcock_chodorow(path_len, depth):
    return -math.log(path_len/(2*depth))