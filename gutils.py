import networkx as nx
#import matplotlib.pyplot as plt

def save_graph(G, filename):
    '''Writes networkx graph to file using custom format'''
    f = open(filename, 'w')
    nodes = G.nodes(data=True)
    # write vertices coordinates
    for node in nodes:
        print("writing node:", node)
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

    for ind, edge in enumerate(edges.split('\n')):
        if (edge == ''):
            continue
        data = edge.split(' ')
        new_graph.add_edge(int(data[0]), int(data[1]))

    f.close()
    return new_graph

#def visualize(G):
#    '''visualize using matplotlib'''
#    fig = plt.figure()
#    ax = fig.gca()
#    for edge in G.edges():
#        side = (G.node[edge[0]]['coord'],G.node[edge[1]]['coord'])
#        x, y = zip(*side)
#        ax.plot(x, y, color = 'r')
#    plt.axis('off')
#    plt.show()
#
#if __name__ == '__main__':
#    graph = nx.Graph()
#    graph.add_node(1, coord=(-2,1))
#    graph.add_node(2, coord=(-1,1))
#    graph.add_node(3, coord=(0,0))
#    graph.add_node(4, coord=(-1,-1))
#    graph.add_node(5, coord=(-2,-1))
#    graph.add_node(6, coord=(1,0))
#    graph.add_node(7, coord=(1,-1))
#    graph.add_node(8, coord=(2,-1))
#    graph.add_node(9, coord=(1,1))
#    graph.add_node(10,coord=(2,1))
#
#    graph.add_edges_from([(1,2), (2,3), (3,4), (4,5), (3,6), (6,7), (7,8),
#                            (6,9), (9,10)])
#
#    visualize(graph)
#
#    new_graph = nx.Graph()
#    #add vertices:
#    for n in graph.nodes(data=True):
#        print("node:", n)
#        num = n[0]
#        coords = n[-1]['coord']
#        new_graph.add_node(num, coord=coords)
#    for edge in nx.max_weight_matching(graph):
#        print("edge:", edge)
#        new_graph.add_edge(edge[0], edge[1])
#
#    visualize(new_graph)
