try:
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

    def __div__(self, other): return self.subtract(other) # self / other

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

    def subtract(self, other): # other is any sequence.
        res = [ ] # self is the subject.
        for x in self.data:
            if not x in other: # Pick common items.
                res.append(x)
        if (self.infty == 1 and other.infty !=1):
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

    def is_connected(self):
        index = 0
        for i in range(min(self.data)+1, max(self.data)-1):
            index += 1
            if self.data[index] != i:
                return False
        return True

degree1 = []
good_vertices = []
stars = []

def makeNormalTree(n):
    T = NX.path_graph(2)
    for i in range(n-2):
        T.add_node(i+2)
        j = randint(0, i+2)
        T.add_edge(j, i+2)
        
    dg1 = degree_i(T, 1)
    dg2 = degree_i(T, 2)
    i = n - 1
    for v in dg2:
        for u in dg1:
            if u in T[v]:
                i = i + 1
                T.add_node(i)
                T.add_edge(v, i)
                break
    return T

def degree_i(G, deg):
    dic = G.degree(with_labels=True)
    res = []
    for i in dic.keys():
        if dic.get(i) == deg:
            res.append(i)
    return res

def max_node(G):
    nd = G.nodes()
    node = nd[0]
    maxim = G.degree(node)
    for i in nd:
        if G.degree(i) > maxim:
            node = i
    return node 

def min_node(G):
    nd = G.nodes()
    node = nd[0]
    minim = G.degree(node)
    for i in nd:
        if G.degree(i) < minim:
            node = i
    return node 

def infForceZero(G):
    #remove degree 2 vertices
    for v in G.nodes():
        if G.degree(v) == 2:
            neighb = G[v]
            if (G.degree(neighb[0]) == 1):
                G.delete_node(neighb[0])
                continue
            if (G.degree(neighb[1]) == 1):
                G.delete_node(neighb[1])
                continue
            for u in G[neighb[1]]:
                G.add_edge(neighb[0], u)
            G.delete_node(neighb[1])
            G.delete_node(v)

def choose_vertex(G):
    for v in good_vertices:
        if v in G:
            return v
    for v in star:
        if v in G:
            return v
    return G.nodes()[0]

visited = {}
status = {}        # can store status of the child node with respect to it's father
def DFS_visit(G, neigh):
    global visited
    global status
    visited[neigh] = 2
    
    for v in G[neigh]:
        if visited[v] == 0:
            status[v] = not status[neigh]
        else:
            continue
        if (v in good_vertices or v in star):
            if (status[v] == True):
                return True
            else:
                continue
        else:
            good = 0
            for u in G[v]:
                if G.degree(u) == 1:
                    good +=1
                if good >= 1:
                    if (status[v] == True):
                        return True
            return DFS_visit(G, v)

    visited[neigh] = 1
    return False

def checkForces_2ray(G, root, neigh):
    if neigh in good_vertices or neigh in star:
            return True
    good = 0
    for u in G[neigh]:
        if G.degree(u) == 1:
            good +=1
        if good >= 1:
            return True
    global visited
    global status
    for i in G.nodes():
        visited[i] = 0
    status[neigh] = True
    visited[root] = 1
    return DFS_visit(G, neigh)

def subSpec(G):
    # this block adds up the spec of each component
    if (not is_connected(G)):
        res = Set([0])
        subgrps = connected_components(G)
        for subgrp in subgrps:
            res = res + subSpec(subgraph(G, subgrp))
        return res
    print G.nodes()
    infForceZero(G)
    print G.nodes()
    if (G.order() -1 != G.size()):
        print 'Problem', G.edges()
    if (G.order() == 1):
        return Set([0])
    elif (G.order() <= 4):
        return Set([1])
    
    root = choose_vertex(G)
    # this block uses the theorem to calc spec recursively
    nb = G[root]
    res = Set([])
    deg_flag = False
    for d in nb:
        if (deg_flag == True and G.degree(d) == 1):
            continue
        if (G.degree(d) == 1):
            deg_flag = not deg_flag
            forces = True
        else:
            forces = checkForces_2ray(G, root, d)
            
        H = G.copy()
        H.delete_nodes_from([root, d])
        if forces == True:
            resH = Set([1]) + subSpec(H)
        else:
            resH = subSpec(H)
        res = res | resH
    return res

def Spec(G):
    global good_vertices
    global degree1
    global star
    degree1 = degree_i(G, 1)
    good_vertices = []
    star = []
    #find good vertices which are like the center of -<
    tmp = []
    for v in degree1:
        candid = G[v][0]
        if candid in good_vertices or candid in star:
            continue
        d1 = 0
        d2 = 0
        for u in G[candid]:
            if G.degree(u) == 1:
                d1 += 1
            else:
                d2 += 1
                
        if d1>1 and d2<=1:
            good_vertices.append(candid)
        elif d1 >= 1:
            star.append(candid)

    #print star, good_vertices
    return subSpec(G)

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

def HTree(i):
    edges = {}
    res = {}
    edges[0] = [(0,1), (1,2)]
    res[0]   = [1]
    edges[1] = [(0,1), (1,2), (1,3)]
    res[1]   = [1]
    edges[2] = [(0,1), (1,2), (1,3), (3,4), (3,5)]
    res[2]   = [1,2]
    edges[3] = [(0,1), (1,2), (1,6), (3,4), (3,5), (3,6)]
    res[3]   = [1]
    edges[4] = [(0,1), (1,2), (1,6), (3,4), (3,5), (3,6)] 
    res[4]   = [1]
    edges[5] = [(0,1), (1,2), (1,6), (3,4), (3,5), (3,6), (6,7)] 
    res[5]   = [2]
    edges[6] = [(0,1), (1,2), (1,6), (3,4), (3,5), (3,6), (6,7), (6,8), (8,9), (8,10)]
    res[6]   = [3]
    edges[7] = [(0,1), (1,2), (1,8), (3,4), (3,5), (3,6), (6,7), (6,8), (8,9)]
    res[7]   = [2,3]
    edges[8] = [(0,1), (1,2), (1,8), (3,4), (3,5), (3,6), (6,7), (6,8), (6,10), (8,9)] 
    res[8]   = [2,3]
    edges[9] = [(0,1), (1,2), (1,8), (3,4), (3,5), (3,6), (6,7), (6,8), (8,9), (9,10), (9,11)]
    res[9]   = [2,3]
    edges[10] = [(0,1), (1,2), (1,3), (3,4), (3,9), (4,5), (4,6), (6,7), (6,8), (9,10), (9,11), (10,12), (10,13), (11,14), (14,15), (14,16)]
    res[10] = [2,3,4]
    edges[11] = [(0,1), (1,2), (1,6), (3,4), (4,5), (4,6), (6,7), (7,8), (7,9), (8,10), (8,11), (9,12), (9,13)]
    res[11] = [3,4]
    edges[12] = [(0,1), (1,2), (1,3), (3,4), (3,6), (4,5), (4,7), (5,8), (5,9), (6,14), (6,15), (7,16), (7,17), (8,12), (8,13), (9,10), (9,11)]
    res  [12] = [3,4]
    
    edges[50] = [(0,1), (1,2), (1,3), (3,4), (3,6), (4,5), (4,7), (5,8), (5,9), (6,14), (6,15), (7,16), (7,17), (8,12), (8,13), (9,10), (9,11)]
    res  [50] = [3, 4]
    #edges[51] = [(0, 1), (0, 15), (0, 13), (0, 9), (1, 2), (1, 3), (1, 4), (2, 11), (2, 7), (3, 16), (3, 6), (4, 5), (4, 17), (7, 8), (7, 12), (8, 10), (8, 18), (12, 19), (12, 14)]
    #edges[52] = [(0, 7), (0, 9), (0, 11),(7, 8), (7, 12), (8, 10), (8, 18), (12, 19), (12, 14)]
    G = Graph()
    G.add_edges_from(edges[i])
    return G, res[i]

def main(PROGRAM):
    if (PROGRAM == 1):
        T = HK(8)
        #T = balanced_tree(2, 7)
        T, sp = HTree(50)
        NX.draw(T, node_color='y', node_size=150)
        #show()
        print Spec(T)
        #print adjacency_spectrum(T)
        #print laplacian_spectrum(T)
        
    elif (PROGRAM == 2):
        f = open("D:\\Mathematics\\App & Source\\reconstruction\\graphs-dis.txt", "w")
        for i in range(1, 20):
            for j in range(10 + 3*i):
                T = makeNormalTree(i)
                S = Spec(T)
                if S.is_connected() == False:
                    f.write("%s ##\t %s\n" % (S.members(), T.edges()))
                    f.flush()
                    #return 0
        f.close()
    elif (PROGRAM == 3):
        f = open("D:\\Mathematics\\App & Source\\reconstruction\\graphs.txt", "w")
        for i in range(1, 20):
            for j in range(10 + 3*i):
                T = makeNormalTree(i)
                S = Spec(T)
                ls = S.members()
                if min(ls)*2+1 < max(ls) and len(ls)>3:
                    f.write("%s ##\t %s\n" % (S.members(), T.edges()))
                    f.flush()
        f.close()
    elif (PROGRAM == 4):
        f = open("D:\\Mathematics\\App & Source\\reconstruction\\graphs-test.txt", "w")
        for i in range(1, 10):
            T = HK(i)
            S= Spec(T)
            if ((S / Set(range(i/2, i))).members() == []):
                f.write("%s ##\t %s\n" % (S.members(), T.edges()))
                f.flush()
        for i in range(9):
            T, SP = HTree(i)
            S = Spec(T)
            if S.members() != SP:
                f.write("%s != main: %s \t %s\n" % (S.members(), SP, T.edges()))
                f.flush()  
            
        f.close()

main(1)
