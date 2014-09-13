try:
    import networkx as NX
    import pylab as P
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
__DFS                       = 1
__BFS                       = 2
__RANDOM                    = 4

#Parameters
number_of_graphs_in_a_run   = 50
number_of_times_to_run      = 1         
number_of_vertices          = 20        # x \in N  
probability_of_graph_construction = 0  # 0<x<1
generation_mode             = __RANDOM
number_of_figs              = 2


def generate_deck(G):
    L={}
    for d in sorted(G.nodes()):
        L[d] = G.copy()
        L[d].delete_node(d)
    return L

def trivial_reconstruct(G, L):
    deg = sorted(G.degree())
    H = L[0].copy()
    cardDeg = sorted(H.degree())
    H.add_node(0)
    for i in range(H.order()-1):
        if cardDeg[i] < deg[i+1]:
            H.add_edge(0,i+1)
    return H

def find_counter_example(G,L):
    deg = sorted(G.degree())
    H = L[0].copy()
    cardDeg = sorted(H.degree())
    H.add_node(0)
    for i in range(H.order()-1):
        if cardDeg[i] < deg[i+1]:
            H.add_edge(0,i+1)
    return H

def reconstruct():
    G=NX.erdos_renyi_graph(8,0.8)
    #G=NX.complete_graph(5)
    H = NX.convert_node_labels_to_integers(G,ordering="increasing degree")
    L = generate_deck(H)
    k = int(sqrt(H.order()))+2
    pos=NX.spring_layout(H)
    P.subplot(k,k, 1)
    NX.draw_circular(H, node_color='r',node_size=40)
    for i in sorted(H.nodes()):
        pos=NX.spring_layout(L[i])
        P.subplot(k,k, i+2)
        NX.draw_circular(L[i],node_color='g',node_size=30)
    T = trivial_reconstruct(H, L)
    print(NX.is_isomorphic(H,T))
    pos=NX.spring_layout(T)
    P.subplot(k,k, i+3)
    NX.draw_circular(T, node_color='y', node_size=30)
    P.show()

def calculate_average(f):
    ave = 0
    count = size(f)
    for i in range(count):
        ave += f[i]

    ave /= float(count)
    return ave

def calculate_variance(f):
    mu = calculate_average(f)
    var = 0
    count = size(f)
    for i in range(count):
        var += (f[i] - mu)*(f[i] - mu)

    var /= float(count)
    return var

def makeNormalTree(n):
    T = NX.path_graph(2)
    for i in range(n-2):
        T.add_node(i+2)
        j = randint(0, i+2)
        T.add_edge(j, i+2)
        
    return T

def generate_BFS_spanning_tree(G, root):
    for u in G.nodes():
        color[u] = 0
    T = NX.create_empty_copy(G)
    bn = [root]
    while bn:
        core = bn
        bn = []
        for i in core:
            color[i] = 1
            for j in G[i]:
                if color[j] == 0:
                    T.add_edge(i,j)
                    color[j] = 1
                    bn.append(j)
    return T

def generate_BFS_level_function(G, root):
    func = {}
    i = 0
    func[i] = 1
    core = [root]
    bn = G.node_boundary(core)
    while bn:
        i += 1
        func[i] = len(bn)
        core.extend(bn)
        bn = G.node_boundary(core)
    return func

color = {}
def DFS_visit(G, u, T):   #0 not visited, 1 visited, 2 gray
    color[u] = 2
    for v in G[u]:
        if color[v] == 0:
            T.add_edge(u,v) 
            T = DFS_visit(G, v, T)

    color[u] = 1
    return T

def generate_DFS_spanning_tree(G, root):
    for u in G.nodes():
        color[u] = 0
    T = NX.create_empty_copy(G)
    T = DFS_visit(G, root, T)
    for u in G.nodes():
        if color[u] == 0:
            T = DFS_visit(G, u, T)
    return T

def generate_DFS_level_function(G, root):
    T = generate_DFS_spanning_tree(G,root)
    return generate_BFS_level_function(T, root)

def is_node_connected(G, v1, v2):
    core = [v1]
    boundry = G.node_boundary(core)
    while boundry:
        if v2 in boundry:
            return 1
        else:
            core.extend(boundry)
            boundry = G.node_boundary(core)

    return 0

def generate_random_graph():
    if probability_of_graph_construction==0:
        k = rand()
    else:
        k = probability_of_graph_construction
    G=NX.gnp_random_graph(number_of_vertices, k) 
    while not(NX.is_connected(G)):
        G=NX.gnp_random_graph(number_of_vertices, k)
        k += 0.1
    return G

def generate_random_regular():
    d = randint(2,number_of_vertices-1)
    G = NX.random_regular_graph(d, number_of_vertices)
    while not (G and NX.is_connected(G)):
        d = randint(2, number_of_vertices-1)
        G = NX.random_regular_graph(d, number_of_vertices)

    return G

def make_random_spanning_tree(G):
    T = NX.create_empty_copy(G)
    edge_list = G.edges()
    edge_count = 0
    while edge_count+1 != G.order():
        chosen = randint(0, len(edge_list))
        edge = edge_list[chosen]
        if is_node_connected(T, edge[0], edge[1])==0:
            T.add_edge(edge)
            edge_count += 1
        del edge_list[chosen]

    return T

def generate_random_level_function(G):
    T = make_random_spanning_tree(G)
    root = G.nodes()[randint(0, len(G.nodes()))]
    return generate_BFS_level_function(T, root)

def generateGraphFunction(H):
    G = NX.convert_node_labels_to_integers(H)
    func = [0 for i in G.nodes()]
    which_used = 0
    if (generation_mode & __DFS == __DFS):
        which_used += 1
        for i in G.nodes():
            lf = generate_DFS_level_function(G, i)
            for j in range(len(lf)):
                func[j] += lf[j]
                
    if (generation_mode & __BFS == __BFS):
        which_used += 1
        for i in G.nodes():
            lf = generate_BFS_level_function(G, i)
            for j in range(len(lf)):
                func[j] += lf[j]

    if (generation_mode & __RANDOM == __RANDOM):
        which_used += 1
        for i in G.nodes():
            lf = generate_random_level_function(G)
            for j in range(len(lf)):
                func[j] += lf[j]

    if generation_mode == 0:
        ordr = float(which_used*G.order())
    else:
        ordr = float(G.order())
        
    for i in G.nodes():
        func[i] /= ordr

    return func

def draw_plot_diffs( generation_type):  # random = 0, normalTree = 1, random spanning tree =2, random regular=3
    temp = [0 for i in range(number_of_vertices)]
    total = []
    functions = []
    diffs = [0 for i in range(number_of_graphs_in_a_run)]

    for i in range(number_of_graphs_in_a_run):
        if (generation_type == 0):
            G = generate_random_graph()
        elif (generation_type == 1):
            G = makeNormalTree(number_of_vertices)
        elif (generation_type == 2):
            C = NX.complete_graph(number_of_vertices)
            G = make_random_spanning_tree(C)
        elif (generation_type == 3):
            G = generate_random_regular()
        
        func = generateGraphFunction(G)
        functions.append(func)
        for i in range(number_of_vertices):
            temp[i] += func[i]

    for i in range(number_of_vertices):
        if temp[i]:
            temp[i] /= number_of_graphs_in_a_run
            total.append(temp[i])
        else:
            break
    total.append(0)
    for i in range(number_of_graphs_in_a_run):
        for j in range(number_of_vertices):
            diffs[i] += (functions[i][j] - temp[j])**2
        diffs[i] = sqrt(diffs[i])

    figure(1)
    plot(diffs)
    
    text(0, diffs[1], "diffs graph")
    xlabel('Index')
    ylabel('Value')
    title('Graph function')
    grid(True)
    global number_of_figs

    figure(number_of_figs)
    number_of_figs = number_of_figs + 1
    hist(diffs)
    
    return total

def draw_plot( generation_type):  # random = 0, normalTree = 1, random spanning tree =2, random regular=3
    temp = [0 for i in range(number_of_vertices)]
    total = []
    functions = []
    diffs = [0 for i in range(number_of_graphs_in_a_run)]

    for i in range(number_of_graphs_in_a_run):
        if (generation_type == 0):
            G = generate_random_graph()
        elif (generation_type == 1):
            G = makeNormalTree(number_of_vertices)
        elif (generation_type == 2):
            C = NX.complete_graph(number_of_vertices)
            G = make_random_spanning_tree(C)
        elif (generation_type == 3):
            G = generate_random_regular()
        
        func = generateGraphFunction(G)
        functions.append(func)
        for i in range(number_of_vertices):
            temp[i] += func[i]

    for i in range(number_of_vertices):
        if temp[i]:
            temp[i] /= number_of_graphs_in_a_run
            total.append(temp[i])
        else:
            break
    total.append(0)
        
    print total
    print calculate_variance(total)

    plot(total)
    if generation_type==0:
        label = "Random graph function: %f "% (calculate_variance(total))
    elif generation_type == 1:
        label = "Normal Tree function: %f "% (calculate_variance(total))
    elif generation_type == 2:
        label = "Random Tree function: %f "% (calculate_variance(total))
    elif generation_type == 3:
        label = "Random regular function: %f "% (calculate_variance(total))
    text(generation_type+1, total[generation_type+1], label)
    xlabel('Index')
    ylabel('Value')
    title('Graph function')
    grid(True)
    
    return total

def draw_tree(H):  # plots a graph H with it's different spanning trees
    G=NX.convert_node_labels_to_integers(H)
    T1=generate_BFS_spanning_tree(G, 0)
    T2=generate_DFS_spanning_tree(G, 0)
    T3=make_random_spanning_tree(G)
    T4=makeNormalTree(G.size())
    
    global number_of_figs
    figure(number_of_figs)
    number_of_figs += 1
    
    P.subplot(2,3, 1)
    title("The graph")
    NX.draw(G, node_color='y', node_size=100)
    P.subplot(2,3, 2)
    title("BFS")
    NX.draw(T1, node_color='g', node_size=100)
    P.subplot(2,3, 3)
    title("DFS")
    NX.draw(T2, node_color='m', node_size=100)
    P.subplot(2,3, 4)
    title("Random")
    NX.draw(T3, node_color='m', node_size=100)
    P.subplot(2,3, 5)
    title("Normal")
    NX.draw(T4, node_color='y', node_size=150)

def draw_graph_function(G, name, stat = 4):
    total = generateGraphFunction(G)
    print total
    plot(total)
    text(stat, total[stat], name)
##    xlabel('Index')
##    ylabel('Value')
##    title('Graph function')
##    grid(True)
    return total

def main():
    for i in range(number_of_times_to_run):
        figure(0)
        draw_plot(1)    #normalTree
        draw_plot(3)    #random spanning tree
        draw_plot(0)    #random
        #draw_plot_diffs(0) #distribution of diffs of functions
    title('Graph function - finished')

def tests():
    H=NX.complete_graph(8)
    generate_random_level_function(H)
    #NX.draw_circular(H, node_color='y', node_size=150)

##
##exit
main()
#show()
#samples
#draw_graph_function(NX.ladder_graph(number_of_vertices), "ladder", 4)
#draw_graph_function(NX.cycle_graph(number_of_vertices), "cycle",5)
#draw_graph_function(NX.wheel_graph(number_of_vertices), "wheel",6)
#draw_graph_function(NX.complete_graph(number_of_vertices), "complete",1)
#draw_graph_function(NX.complete_bipartite_graph(number_of_vertices/2, number_of_vertices/2), "comp bipartite",1)
#draw_graph_function(NX.circular_ladder_graph(number_of_vertices), "circ ladder",6)
#draw_graph_function(NX.grid_2d_graph(sqrt(number_of_vertices), sqrt(number_of_vertices)), "grid",6)
#draw_graph_function(NX.hypercube_graph(log(number_of_vertices)/log(2)), "hypercube",6)
#draw_graph_function(NX.lollipop_graph(number_of_vertices/2, number_of_vertices/2), "lollipop",6)
#G = NX.random_regular_graph(5, number_of_vertices)
#if G:
#    draw_graph_function(G, "random regular",6)
#draw_tree( G)
