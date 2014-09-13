try:
    from networkx import *
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

class Set:
    def __init__(self, value = [ ]): # Constructor
        self.data = [ ] # Manages a list
        if 1J in value:
            self.infty = 1
            value.remove(1J)
        else:
            self.infty = 0
        
        self.concat(value)
        
    def __len__(self): return len(self.data) # len(self)
    
    def __getitem__(self, key): return self.data[key] # self[i]
    
    def __and__(self, other): return self.intersect(other) # self & other
    
    def __or__(self, other): return self.union(other) # self | other

    def __add__(self, other): return self.addition(other) # self + other
    
    def __repr__(self): return 'Set:' + `self.data` + '\t Infty:' + `self.infty` # Print

    def __contains__(self,n): return n in self.data
    
    def intersect(self, other): # other is any sequence.
        res = [ ] # self is the subject.
        for x in self.data:
            if x in other: # Pick common items.
                res.append(x)
        if (self.infty == 1 and other.infty ==1):
            res.append(1J)
        return Set(res) # Return a new data.
    
    def union(self, other): # other is any sequence.
        res = self.data[:] # Copy of my list
        for x in other: # Add items in other.
            if not x in res:
                res.append(x)
        res = sorted(res)
        if (self.infty == 1 or other.infty ==1):
            res.append(1J)
        return Set(res)

    def addition(self, other): # other is any sequence.
        res = [ ] # Copy of my list
        for x in self.data: # Add items in other.
            for y in other.data:
                a = x + y
                if not a in res:
                    res.append(a)
        if (self.infty == 1 or other.infty ==1):
            res.append(1J)
        return Set(res)
    
    def concat(self, value): # value: list, Set...
        for x in value: # Removes duplicates
            if not x in self.data:
                self.data.append(x)

    def add(self, n):
        if n not in self.data:
            self.data.append(n)

    def add_from(self, nlist):
        for n in nlist:
            if n not in self.data:
                self.data.append(n)

    def delete(self,n):
            self.data.remove(n)

    def delete_from(self,nlist):
        for n in nlist:
            self.data.remove(n)

    def members(self):
        res = self.data
        if self.infty==1: res.append(1J)
        return res
    
    def clear(self):
        self.data = []

    def copy(self):
        S=self.__class__()
        S.data = self.data
        S.infty = self.infty
        return S

def degree1(G):
    dic = G.degree(with_labels=True)
    res = []
    for i in dic.keys():
        if dic.get(i) == 1:
            res.append(i)
    return res

def max_node(G):
    dic = G.degree(with_labels=True)
    maxm = 0
    node = 0
    for i in dic.keys():
        if dic.get(i) > maxm:
            node = i
            maxm = dic.get(i)
    return node

def min_node(G):
    dic = G.degree(with_labels=True)
    minm = dic.get(0)
    node = 0
    for i in dic.keys():
        if dic.get(i) < minm:
            node = i
            minm = dic.get(i)
    return node 

def ForceZero(G):
    dg1 = degree1(G)
    while len(dg1) != 0:
        removeNb = True
        i = dg1[0]
        if not i in G.nodes(): continue
        last = i
        nb = G[last][0]
        while (G.degree(nb) == 2):
            G.delete_node(last)
            removeNb = not removeNb
            last = nb
            nb = G[last][0]
        G.delete_node(last)
        if removeNb == True:
            G.delete_node(nb)
        dg1 = degree1(G)
            
    return 0

def forcing_node(G):  #Choose a node
    V = G.nodes()
    minim = 0
    node = V[0]
    for v in V:
        H = G.copy()
        H.delete_node(v)
        ForceZero(H)
        lm = G.order() - H.order()
        if lm >= minim:
            minim = lm
            node = v
    return node

def choose_node(G, candid):
    if not candid in G:
        #root = forcing_node(G)
        root = max_node(G)
        #root = min_node(G)
        #d = randint(0,G.order()-1)
        #root = G.nodes()[d]
    else:
        root = candid

    return root
        


gl = 0
def VSpec(G, node = -1):
    ForceZero(G)
    if (G.order() == 2 and G.size() == 1):
        return Set([0])
    elif (G.order() == 1):
        return Set([1J])
    elif (G.order() == 0):
        return Set([0])
    elif (G.size() == 0):
        return Set([1J])

    # this block adds up the spec of each component
    if (not is_connected(G)):
        res = Set([0])
        subgrps = connected_components(G)
        for subgrp in subgrps:
            res = res + VSpec(subgraph(G, subgrp))
            return res

    root = choose_node(G, node)

    # this block uses the theorem to calc spec recursively
    outer_breaked = 0
    inter_breaked = 0
    Gcopy = G.copy()

    for cnt in G.nodes(): #in the case an infty occured, it will search for a node to prevent infty
        outer_breaked = 0
        nb = G[root]
        res = Set([])
        Gcopy.delete_node(root)
        near = 0
        for d in nb:
            inter_breaked = 0
            H = Gcopy.copy()
            near = Gcopy[d][0]
            H.delete_node(d)
            res = res | VSpec(H, near)
            if res.infty == 1:
                root = cnt
                Gcopy = G.copy()
                inter_breaked = 1
                break
        if inter_breaked == 1:
            continue
        else:
            res = Set([1]) + res
            outer_breaked = 1
            break
    if outer_breaked == 0:
        res = Set([1J])
    return res

def choose_edge(G):
    E = G.edges()
    minim = 0
    edge = E[0]
    for e in E:
        H = G.copy()
        H.delete_edge(e)
        ForceZero(H)
        lm = G.order() - H.order()
        if lm >= minim:
            minim = lm
            edge = e
    return edge

def ESpec(G):
    ForceZero(G)
    if (G.order() == 2 and G.size() == 1):
        return Set([0])
    elif (G.order() == 1):
        return Set([1J])
    elif (G.order() == 0):
        return Set([0])
    elif (G.size() == 0):
        return Set([1J])
    # this block adds up the spec of each component
    if (not is_connected(G)):
        res = Set([0])
        subgrps = connected_components(G)
        for subgrp in subgrps:
            res = res + ESpec(subgraph(G, subgrp))
            return res

    edge = choose_edge(G)
    G.delete_edge(edge)
    res = ESpec(G.copy())
    G.delete_nodes_from(edge)
    res = res | ESpec(G)
    res = Set([1]) + res
    return res

gl = 0
H = grid_2d_graph(4 ,4)
#H = ladder_graph(10)
#H = complete_graph(8)
#H = circular_ladder_graph(6)
H = complete_bipartite_graph(5,5)
#H = cycle_graph(10)
#H = hypercube_graph(4)
#H = petersen_graph()
G = convert_node_labels_to_integers(H,ordering="increasing degree")
#draw(G)
#print ESpec(G.copy())
print VSpec(G)

