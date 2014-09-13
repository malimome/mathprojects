try:
    import infspecMIN as minspec
    import infspecT as tspec
    from networkx import *
    import networkx as NX
    from numpy import *
    import random
    import math
    from matplotlib.pylab import *
    import matplotlib.mlab as mlab
except:
    print
    print "A package not found!"
    print
    raise

def HK(k):
    T = NX.path_graph(k)
    k= k +1
    for i in T.nodes():
        T.add_node(k-1)
        T.add_node(k)
        T.add_edge(i, k-1)
        T.add_edge(i, k)
        k = k+2
    return T

def HTree():
    edges = [(0, 1), (0, 3), (0, 5), (0, 9), (1, 2), (1, 12), (2, 11), (2, 14), (3, 4), (3, 7), (4, 6), (4, 15), (5, 8), (5, 13), (9, 16), (9, 10)]
    edges = [(0, 1), (0, 2), (0, 12), (1, 5), (1, 6), (2, 8), (2, 3), (3, 4), (3, 10), (5, 13), (5, 9), (6, 14), (6, 7), (10, 11), (10, 15)]
    G = Graph()
    G.add_edges_from(edges)
    return G

def main(PROGRAM):
    if (PROGRAM == 1):
        T = HK(8)
        #T = balanced_tree(2, 3)
        T = HTree()
        NX.draw(T, node_color='y', node_size=150)
        #show()
        print Spec(T)
        
    elif (PROGRAM == 2):
        f = open("D:\\Mathematics\\App & Source\\reconstruction\\graphs-compare.txt", "w")
        for i in range(1, 20):
            for j in range(10 + 3*i):
                T = tspec.makeNormalTree(i)
                S = tspec.Spec(T)
                U = minspec.Spec(T)
                if S.members() != U.members():
                    f.write("%s ##\t %s ##\t %s\n" % (S.members(), U.members(), T.edges()))
                    f.flush()
                    #return 0
        f.close()

main(2)
