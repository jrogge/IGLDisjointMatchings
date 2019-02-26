import networkx as nx
import matplotlib.pyplot as plt

def max_matching(G):
    return networkx.max_weight_matching(G)

def visualize(G):
    '''visualize using matplotlib'''
    fig = plt.figure()
    ax = fig.gca()
    for edge in G.edges():
        side = (G.node[edge[0]]['coord'],G.node[edge[1]]['coord'])
        x, y = zip(*side)
        ax.plot(x, y, color = 'r')
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    graph = nx.Graph()
    graph.add_node(1, coord=(-2,1))
    graph.add_node(2, coord=(-1,1))
    graph.add_node(3, coord=(0,0))
    graph.add_node(4, coord=(-1,-1))
    graph.add_node(5, coord=(-2,-1))
    graph.add_node(6, coord=(1,0))
    graph.add_node(7, coord=(1,-1))
    graph.add_node(8, coord=(2,-1))
    graph.add_node(9, coord=(1,1))
    graph.add_node(10,coord=(2,1))

    graph.add_edges_from([(1,2), (2,3), (3,4), (4,5), (3,6), (6,7), (7,8),
                            (6,9), (9,10)])

    visualize(graph)

    new_graph = nx.Graph()
    #add vertices:
    for n in graph.nodes(data=True):
        print("node:", n)
        num = n[0]
        coords = n[-1]['coord']
        new_graph.add_node(num, coord=coords)
    for edge in nx.max_weight_matching(graph):
        print("edge:", edge)
        new_graph.add_edge(edge[0], edge[1])

    visualize(new_graph)
