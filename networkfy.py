__author__ = 'Matias Estrada'
__version__ = '0.1.0'


import networkx as nx
import matplotlib.pyplot as plt

from collections import Counter

GRAPH_TYPE = {
    "undirected": nx.Graph,
    "directed": nx.MultiDiGraph
}


DATASET_PATH = '/home/matias/devel/inf414/datasets/aan/aan/release/2012/'
PAPER_AUTHOR_FILE = 'paper_author_affiliations.txt'


def get_distribution(paper_author):
    paper_author_dist = Counter(map(lambda x: x[0], paper_author))
    author_paper_dist = Counter(map(lambda x: x[1], paper_author))

    return paper_author_dist, author_paper_dist

def get_paper_author(
    dataset_location=DATASET_PATH,
    paper_author_file=PAPER_AUTHOR_FILE):

    paper_author = []
    with open(dataset_location + paper_author_file, 'r') as acl_file:
        # A00-1002    13467;3431;13692
        separator = '\t'
        for line in acl_file.readlines():
            pid, aids = line.strip().split(separator)
            aids = aids.split(';')

            for aid in aids:
                paper_author.append((pid, aid))

    return paper_author


def get_network(dataset_location=DATASET_PATH, filename='acl.txt', graph_type='undirected'):
    edges = []
    with open(dataset_location + filename, 'r') as acl_file:
        #  C08-3004 ==> A00-1002
        separator = ' ==> '
        for line in acl_file.readlines():
            edges.append(line.strip().split(separator))

    graph = GRAPH_TYPE[graph_type]()
    for edge in edges:
        graph.add_edge(*edge, etype='cite')

    return graph


def filter_by_venue(venue):
    return map(lambda x: x[0], filter(lambda x: x[1]['venue'] == venue, acl.node.items()))


def reverse_lookup(dd, value):
    return (k for k,v in dd.items() if v==value).next()


def get_venue(paper_id):
    value = map(
            lambda x: x[2],
            filter(
                   lambda x: x[0] == paper_id,
                   papers_meta)
            )
    return value[0] if value != [] else None


def cluster_by_venue(dataset_location=DATASET_PATH, filename='paper_ids_meta.txt'):

    papers_meta = []
    with open(dataset_location + filename, 'r') as paper_meta_file:
        #C10-2037   Monolingual ... COLING - POSTERS    2010
        separator = '\t'
        for line in paper_meta_file.readlines():
            papers_meta.append(line.strip().split(separator))

    venues = set(map(lambda x: x[2], papers_meta))

    venues_mapping = {}
    for idx, venue in enumerate(venues):
        venues_mapping["V-{0}".format(idx)] = venue
    venues_mapping['V-null'] = None

    try:
        for node in acl.node:
            acl.node[node]['venue'] = reverse_lookup(venues_mapping, get_venue(node))
    except IndexError, StopIteration:
        print node
        raise

    clusters_by_venue = {}
    for vid in venues_mapping.keys():
        clusters_by_venue[vid] = acl.subgraph(filter_by_venue(vid))

    return clusters_by_venue
