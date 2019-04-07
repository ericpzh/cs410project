import math
import sys
import time
import metapy
import pytoml


def load_ranker(cfg_file):
    k1 = 1.5
    b = 0.8
    k3 = 55
    return metapy.index.OkapiBM25(k1, b, k3)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    cfg = sys.argv[1]
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    ranker = load_ranker(cfg)
    ev = metapy.index.IREval(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    # TODO: Implement the algorithm
