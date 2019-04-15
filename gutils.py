import networkx as nx
#import matplotlib.pyplot as plt

def save_graph(G, filename):
    '''Writes networkx graph to file using custom format'''
    f = open(filename, 'w')
    nodes = G.nodes(data=True)
    # write vertices coordinates
    for node in nodes:
        coords = node[-1]['coord']
        c_str = ''
        for c in coords[:-1]:
            c_str += str(c) + ' ' 
        c_str += str(coords[-1]) + '\n'
        f.write(c_str)
    f.write('\n')
    # write edge vertices and type
    edges = G.edges(data=True)
    for edge in edges:
        v1 = edge[0]
        v2 = edge[1]
        f.write('%d %d\n'%(v1, v2))
        #type = edge
    f.close()


def load_graph(filename):
    '''Read graph data from a file.
    Returns a networkx graph'''
    new_graph = nx.Graph()
    f = open(filename, 'r')
    lines = f.read().split('\n\n')
    nodes = lines[0]
    edges = lines[1]

    for ind, node in enumerate(nodes.split('\n')):
        vals = [float(coord) for coord in node.split(' ')]
        new_graph.add_node(ind, coord=vals)

    for edge in edges.split('\n'):
        if (edge == ''):
            continue
        data = edge.split(' ')
        new_graph.add_edge(int(data[0]), int(data[1]))

    f.close()
    return new_graph
