import time
from random import randint
from heapq import heappush, heappop
from copy import copy
import queue

class Vertex:


    def __init__(self, key):
        self.id = key
        self.heapIndex = float('inf')
        self.connectedTo = set()
        self.color = 0
        self.edges = set()

    def addNeighbor(self, nbr,w):
        self.connectedTo.add((nbr,w))
        
    def addEdge(self, edge):
        self.edges.add(edge)
        
    def remNeighbor(self, nbr):
        for v in self.getConnections():
            if v[0].id == nbr:
                self.connectedTo.remove(v)
                return
                
    def remEdge(self,edge):
        for e in self.getEdges():
            if e == edge:
                self.edges.remove(e)
                return
                
    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in
                self.connectedTo])
                
    def getConnections(self):
        return self.connectedTo
        
    def getEdges(self):
        if (len(self.edges)):
            return self.edges
        else:
            return iter(())
        
    def getEdge(self,edge):
        for e in self.getEdges():
            if e == edge:
                return e

    def getId(self):
        return self.id

    def getIndex(self):
        return self.heapIndex

    def getWeight(self, nbr):
        for v in self.getConnections():
            if v[0].id == nbr:
                return v[1]

class Graph:

    def __init__(self,srs):
        self.vertList = {}
        self.numVertices = 0
        self.edgeList=set()
        self.numEdges = 0
        self.s = srs

    def addVertex(self, key):
        if (key<self.numVertices and self.numVertices>0):
            return
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex
    def addEdge(self, f, t, w):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        exist = 0
        if self.vertList[f].edges:
            for edge in self.vertList[f].getEdges(): # does not exist
                if edge.ds == t:
                    exist=1
        if self.vertList[t].edges:
            for edge in self.vertList[t].getEdges():
                if edge.ds == f:
                    exist=1
        if not exist:
            e = Edge(t, f, w)
            self.vertList[t].addEdge(e)
            self.edgeList.add(e)
            e = Edge(f, t, w)
            self.vertList[f].addEdge(e)
            self.edgeList.add(e)
            self.vertList[f].addNeighbor(self.vertList[t], w)
            self.vertList[t].addNeighbor(self.vertList[f], w)

    def rmEdge(self, f, t):
        self.vertList[f].remNeighbor(t)
        for e in self.edgeList:
            if e.sr == f and e.ds == t:
                self.vertList[f].remEdge(e)
                self.vertList[t].remEdge(e)
                self.edgeList.remove(e)
                return
    def updateEdge(self, f, t, w):
        #self.vertList[f].remNeighbor(t)
        for e in self.edgeList:
            if e.sr == f and e.ds == t:
                e.w = w
                return
        
        
    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    
    def __contains__(self, n):
        return n in self.vertList

''' 

      tree class 
' 
'
'
''' 
class treeV:

    def __init__(self, vertex):
        self.id = vertex
        self.wieght = float('inf')
        self.port = None
        self.parent = None
        self.color = 0
        self.children = set()
    def getChildren(self):
        return self.children


# Ribeiro Alg.

class RIB:

    def __init__(self,srs):
        self.treeList = {} 
        self.A=[]
        self.s = srs
        
    def init_MST(self, edgeList, n):
        #fix list index to insure adding to len. INDEX
        for e in edgeList: 
            e.AIndex = len(self.A)
            self.A.append(e)
            
            
        self.A.sort(key=lambda x: x.w)
        for i in range(n):
            self.treeList[i] = treeV(i)
            
    '''
    def insert_A(self, item, w):
        # fixing
        for e in self.treeList[item.sr].getChildren():
            if e.ds == item.ds:
                index = self.A.index(e)
        self.A.append(item)
        return self.A.index(
        index = self.A.index(item)
        self.A.[index]= ((item.sr, item.ds),w)
    ''' 
        
    def sort_A(self):
        self.A.sort(key=lambda x: x.w)
        for i in range(len(self.A)):
            self.A[i].AIndex=i


    def primMST(self, G, source):
        
        for v in self.treeList:
            self.treeList[v].color = 1
        self.treeList[source].color = 0
        heap = Heap()
        for e in G.vertList[source].getEdges():
            if e.heapIndex == float('inf'):
                heap.push(e, e.w)
            else:
                heap.update(e.w, e.heapIndex)
        while heap.heap():
            popped = heap.pop() # pop an edge with the min. wieght
            popped.heapIndex = float('inf')
            if self.treeList[popped.ds].color ==1:  # if the neighbur is not yet considered (new) 
                                                    #> and since we scaning the min edge then we need this edge for this vertex
               self.treeList[popped.ds].color = 0
               e = Edge(popped.sr, popped.ds, popped.w)
               self.treeList[popped.sr].children.add(e)
               e = Edge(popped.ds,popped.sr, popped.w)
               e.AIndex = popped.AIndex
               self.treeList[popped.ds].children.add(e)

                
               for e in G.vertList[popped.ds].getEdges():
                if self.treeList[e.ds].color == 1:
                    index = e.heapIndex
                    if index == float('inf'):
                        heap.push(e, e.w)
                    else:
                        heap.update(e.w, index)
        self.treeList[source].parent = 1
        q1 = queue.Queue()
        q1.put(self.treeList[source].id)
        while not q1.empty():
            node = q1.get()
            for e in self.treeList[node].getChildren():
                if self.treeList[e.ds].parent == None:
                    self.treeList[e.ds].parent = e
                    q1.put(e.ds)
        self.treeList[source].parent = None

        for v in self.treeList:
            self.treeList[v].color = 0
        

    def Find_Max(self, i, j, w):
        path = []
        path2 = []

        isParent = 0
        self.ParentColorRed(self.s, i)

        isParent, rootSubTree = self.findRootCycle(path, j, i)
        if isParent == 2:
            path.clear()
        # connecting a dissconnected suptree
        if isParent == 1:
            maxEdge = Edge(0,rootSubTree,float('inf'))
            self.ParentColorWth(self.s, i)
            return maxEdge, j
        if self.treeList[i].color<2:
            isParent, rootSubTree = self.findRootCycle(path2, i, j)
            if isParent == 1:
                maxEdge = Edge(0,rootSubTree,float('inf'))
                self.ParentColorWth(self.s, i)
                return maxEdge, i
            if isParent == 2:
                path2.clear()
            
        self.ParentColorWth(self.s, i)
        maxW = w
        maxEdge = Edge(i, j, w)

        Node = j
        for p in path:
            if maxW<p.w:
                maxW = p.w
                maxEdge = p
        
        for p in path2:
            if maxW<p.w:
                maxW = p.w
                maxEdge = p
                Node = i

        return maxEdge, Node

    # #
    def ParentColorRed(self, s, y):
        if y==s:
            self.treeList[y].color = 1
            return 
        else:
            if self.treeList[y].color == 0:
                self.treeList[y].color = 1
                if self.treeList[y].parent:
                    self.ParentColorRed(s, self.treeList[y].parent.sr)
            return
    
    def findRootCycle(self,found, u, x):
        if u == self.s:
            return 2, 0
        if self.treeList[u].parent:
            if ((self.treeList[u].color != self.treeList[self.treeList[u].parent.sr].color) or (self.treeList[u].parent.sr ==x)):
                found.append(copy(self.treeList[u].parent))
                self.treeList[self.treeList[u].parent.sr].color = self.treeList[u].color +3
                return 0, 0
            else:
                found.append(copy(self.treeList[u].parent))
                return self.findRootCycle(found, self.treeList[u].parent.sr, x)
        else:
            return 1, u

    def ParentColorWth(self, s, y):
        if y==s:
            self.treeList[y].color = 0
            return 
        else:
            if self.treeList[y].color > 0:
                self.treeList[y].color = 0
                if self.treeList[y].parent:
                    self.ParentColorWth(s, self.treeList[y].parent.sr)
        return
        
    '''
 
                        INC
 
    '''
             
    def RIB_INC(self, i, j, w):
        # the lines 1-3 are ebmedded in Find_Path
        # node is the node with maxEdge in its path to root and need to be fixed
        
        maxEdge, Node = self.Find_Max(i, j, w) # line 4
        # determine i and j 
        if Node ==i:
            i, j = j, i
        if maxEdge.w > w:   # lines 5-8
            for e in self.treeList[maxEdge.sr].getChildren():
                if e.ds == maxEdge.ds:
                    self.treeList[maxEdge.sr].children.remove(e)
                    break
            for e in self.treeList[maxEdge.ds].getChildren():
                if e.ds == maxEdge.sr:
                    self.treeList[maxEdge.ds].children.remove(e)
                    break 
            
            #link the rest of path to maxEdge
            u = copy(self.treeList[j].parent)
            if u:
                while(u.sr!=maxEdge.sr):
                    #time.sleep(.5)
                    if (self.treeList[u.sr].parent):
                        e = copy(u)
                        u = copy(self.treeList[u.sr].parent)
                        e.sr, e.ds = e.ds, e.sr
                        self.treeList[e.ds].parent = e
                        
                        if u == None:
                            break

                    else:
                        break
            # link (line 7)
            # link j to i
            e = Edge(j,i,w)
            self.treeList[j].children.add(e)
            e=Edge(i,j,w)
            self.treeList[i].children.add(e)
            self.treeList[j].parent = e
        
        return

    def FixParent(self, path, u, dst):
        if u==self.s:
            return 0
        if u==dst:
            return 1
        found = self.FixParent(path,self.treeList[u].parent.sr, dst)
        if found:
            return path.append(u)
        return 0


    def RIB_DEC(self,G, i, j, s, f, w):
        
        cut_x = set()
        workSet = set()
        
        # labeling subTree j with color 1 (Line 1)
        if self.treeList[i].parent:
            if self.treeList[i].parent.sr == j: #Making sure that i is the parent of j
                i, j = j, i
        workSet.add(self.treeList[j].id)
        while (len(workSet)):
            x = workSet.pop()
            cut_x.add(x)
            self.treeList[x].color = 1
            for e in self.treeList[x].getChildren():
                if self.treeList[e.ds].color ==0:
                    workSet.add(e.ds)

        k = s 
        flag = 0
        while k < f:
            edge = self.A[k]
            if self.treeList[edge.sr].color != self.treeList[edge.ds].color:
                flag = 1
                for e in self.treeList[i].getChildren(): #cut (line 6)
                    if e.ds == j:
                        self.treeList[i].children.remove(e)
                        break
                for e in self.treeList[j].getChildren():
                    if e.ds == i:
                        self.treeList[j].children.remove(e)
                        break 
                # fixing the parent pointer for the alg
                # edge.sr.color = 1 then , j
                
                if self.treeList[edge.sr].color == 1: # insuring the edge is u->v
                    edge.sr, edge.ds = edge.ds, edge.sr
                v = edge.ds
                
                # fixing the parrent pointer from v (the nodes connects the 2 subtrees) to the affected j
                upperParent = copy(self.treeList[v].parent)
                while(upperParent.ds != j):
                    if (self.treeList[upperParent.sr].parent):
                        e = copy(self.treeList[upperParent.sr].parent)
                        upperParent.sr, upperParent.ds = upperParent.ds, upperParent.sr
                        self.treeList[upperParent.ds].parent = copy(upperParent)
                        upperParent = e                
                    else:
                        break
                    
                e2 = Edge(edge.sr, edge.ds,edge.w)

                self.treeList[edge.sr].children.add(e2)
                self.treeList[edge.ds].parent = e2
                e2 = Edge(edge.ds,edge.sr,edge.w)
                self.treeList[edge.ds].children.add(e2)
                
                
                
                for u in self.treeList:
                    for e in self.treeList[u].getChildren():
                        if e.ds == u:
                            time.sleep(5)
               
                # reset the labeling of subTree j
                while (len(cut_x)):
                    x = cut_x.pop()
                    self.treeList[x].color = 0
  

                return
            k=k+1
        while (len(cut_x)):
                    x = cut_x.pop()
                    self.treeList[x].color = 0

            
    



class MST:

    def __init__(self,srs):
        self.treeList = {}
        self.s = srs
    def init_MST(self, n):
        for i in range(n):
            self.treeList[i] = treeV(i)
                 
    def build_ports(self, s):
      
      for i in self.treeList[s].children:
        port = self.treeList[s].children[i]
        l = list() 
        l.append(i)
        while l:
          u = l.pop()
          self.treeList[u].port = port
          for child in self.treeList[u].children:
            l.append(child)
    def primMST(self, G, source):
        
        for v in self.treeList:
            self.treeList[v].color = 1
        self.treeList[source].color = 0
        heap = Heap()
        for e in G.vertList[source].getEdges():
            if e.heapIndex == float('inf'):
                heap.push(e, e.w)
            else:
                heap.update(e.w, e.heapIndex)
        while heap.heap():
            popped = heap.pop() # pop an edge with the min. wieght
            popped.heapIndex = float('inf')
            if self.treeList[popped.ds].color ==1:  # if the neighbur is not yet considered (new) 
                                                    #> and since we scaning the min edge then we need this edge for this vertex
               self.treeList[popped.ds].color = 0
               e = Edge(popped.sr, popped.ds, popped.w)
               self.treeList[popped.sr].children.add(e)
               e = Edge(popped.ds,popped.sr, popped.w)
               e.AIndex = popped.AIndex
               self.treeList[popped.ds].children.add(e)

                
               for e in G.vertList[popped.ds].getEdges():
                if self.treeList[e.ds].color == 1:
                    index = e.heapIndex
                    if index == float('inf'):
                        heap.push(e, e.w)
                    else:
                        heap.update(e.w, index)
        self.treeList[source].parent = 1
        q1 = queue.Queue()
        q1.put(self.treeList[source].id)
        while not q1.empty():
            node = q1.get()
            for e in self.treeList[node].getChildren():
                if self.treeList[e.ds].parent == None:
                    self.treeList[e.ds].parent = e
                    q1.put(e.ds)
        self.treeList[source].parent = None

        for v in self.treeList:
            self.treeList[v].color = 0
        

    def Find_Max(self, i, j, w):
        path = []
        path2 = []

        isParent = 0
        self.ParentColorRed(self.s, i)

        isParent, rootSubTree = self.findRootCycle(path, j, i)
        if isParent == 2:
            path.clear()
        # connecting a dissconnected suptree
        if isParent == 1:
            maxEdge = Edge(0,rootSubTree,float('inf'))
            self.ParentColorWth(self.s, i)
            return maxEdge, j
        if self.treeList[i].color<2:
            isParent, rootSubTree = self.findRootCycle(path2, i, j)
            if isParent == 1:
                maxEdge = Edge(0,rootSubTree,float('inf'))
                self.ParentColorWth(self.s, i)
                return maxEdge, i
            if isParent == 2:
                path2.clear()
            
        self.ParentColorWth(self.s, i)
        maxW = w
        maxEdge = Edge(i, j, w)

        Node = j
        for p in path:
            if maxW<p.w:
                maxW = p.w
                maxEdge = p
        
        for p in path2:
            if maxW<p.w:
                maxW = p.w
                maxEdge = p
                Node = i
        return maxEdge, Node

    # #
    def ParentColorRed(self, s, y):
        if y==s:
            self.treeList[y].color = 1
            return 
        else:
            if self.treeList[y].color == 0:
                self.treeList[y].color = 1
                if self.treeList[y].parent:
                    self.ParentColorRed(s, self.treeList[y].parent.sr)
            return
    
    def findRootCycle(self,found, u, x):
        if u == self.s:
            return 2, 0
        if self.treeList[u].parent:
            if ((self.treeList[u].color != self.treeList[self.treeList[u].parent.sr].color) or (self.treeList[u].parent.sr ==x)):
                found.append(copy(self.treeList[u].parent))
                self.treeList[self.treeList[u].parent.sr].color = self.treeList[u].color +3
                return 0, 0
            else:
                found.append(copy(self.treeList[u].parent))
                return self.findRootCycle(found, self.treeList[u].parent.sr, x)
        else:
            return 1, u

    def ParentColorWth(self, s, y):
        if y==s:
            self.treeList[y].color = 0
            return 
        else:
            if self.treeList[y].color > 0:
                self.treeList[y].color = 0
                if self.treeList[y].parent:
                    self.ParentColorWth(s, self.treeList[y].parent.sr)
        return
        
    '''
 
                        INC
 
    '''
             
    def incMST(self, i, j, w):
        maxEdge, Node = self.Find_Max(i, j, w) # line 4
        
        # setUp i and j 
        if Node ==i:
            i, j = j, i
        if maxEdge.w > w:   
            for e in self.treeList[maxEdge.sr].getChildren():
                if e.ds == maxEdge.ds:
                    self.treeList[maxEdge.sr].children.remove(e)
                    break
            for e in self.treeList[maxEdge.ds].getChildren():
                if e.ds == maxEdge.sr:
                    self.treeList[maxEdge.ds].children.remove(e)
                    break 
            
            #link the rest of the path
            u = copy(self.treeList[j].parent)
            if u:
                while(u.sr!=maxEdge.sr):
                    if (self.treeList[u.sr].parent):
                        e = copy(u)
                        u = copy(self.treeList[u.sr].parent)
                        e.sr, e.ds = e.ds, e.sr
                        self.treeList[e.ds].parent = e
                        if u == None:
                            break
                    else:
                        
                        break
            # link using the new inserted edge
            e = Edge(j,i,w)
            self.treeList[j].children.add(e)
            e=Edge(i,j,w)
            self.treeList[i].children.add(e)
            self.treeList[j].parent = e
        
        return
    
    
    
 
    
    def decMST(self, G, x, y, w):
        #Removing edge from Tree
        if self.treeList[x].parent:
            if self.treeList[x].parent.sr == y: #Making sure that x is the parent of y
                x, y = y, x
            
            
        for e in self.treeList[x].getChildren():
            if e.ds == y:
                self.treeList[x].children.remove(e)
                break
        
        # delete the revirse edge (line.4)
        for e in self.treeList[y].getChildren():
            if e.ds == x:
                self.treeList[y].children.remove(e)
                break
        
        cut_x = set()
        cut_y = set()
        min_w = float('inf')  
        min_e = 0#Edge(1,1,10) # making suuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuure
        workSet = set()
        
        workSet.add(self.treeList[y].id)
        while (len(workSet)):
            node = workSet.pop()
            cut_x.add(node)
            self.treeList[node].color = 1
            for e in self.treeList[node].getChildren():
                if self.treeList[e.ds].color ==0:
                    workSet.add(e.ds)
                #if (e.ds == self.s):
                    
        workSet = copy(cut_x)
        while (len(cut_x)):
            node = cut_x.pop()
            if G.vertList[node].getEdges():
                for e in G.vertList[node].getEdges():
                    if self.treeList[e.sr].color != self.treeList[e.ds].color and e.w < min_w:
                        min_w = e.w
                        min_e = e
        if min_e:
            upperParent = copy(self.treeList[min_e.sr].parent)
            while (upperParent.ds != y):
                if (self.treeList[upperParent.sr].parent):
                    e = copy(self.treeList[upperParent.sr].parent)
                    upperParent.sr, upperParent.ds = upperParent.ds, upperParent.sr
                    self.treeList[upperParent.ds].parent = copy(upperParent)
                    upperParent = e
            self.treeList[min_e.sr].children.add(min_e)
            min_e2 = Edge(min_e.ds,min_e.sr,min_e.w)
            self.treeList[min_e2.sr].children.add(copy(min_e2))
            self.treeList[min_e.sr].parent = copy(min_e2)
        while (len(workSet)):
            x = workSet.pop()
            self.treeList[x].color = 0
        
        

class Edge:

    def __init__(self, s1,s2, key):
        self.sr = s1
        self.ds = s2
        self.w = key
        self.color = 0
        self.heapIndex = float('inf')
        self.AIndex = float('inf')
    def getSR(self):
        return self.sr



class Heap:

    def __init__(self):
        self.heapList = {}
        self.len = 0

    def shiftUp(self, length):
        child = length
        while child > 0:
            parent=int((child - 1)/ 2)
            if self.heapList[child].w < self.heapList[parent].w:
                flip = self.heapList[child]
                self.heapList[child] = self.heapList[parent]
                self.heapList[parent] = flip

           # update indexes
                self.heapList[child].heapIndex = child
                self.heapList[parent].heapIndex = parent

           # move pointer ups
                child = parent
            else:
                return self

    def shiftDown(self, newV):
        length = self.len - 1

        child = newV * 2 + 1
        while newV * 2 + 1 <= length:
            try:
                child = newV * 2 + 1
                if child + 1 <= length and self.heapList[child].w > self.heapList[child + 1].w:
                    child += 1
                if child <= length and self.heapList[newV].w > self.heapList[child].w:
                    flip = self.heapList[child]
                    self.heapList[child] = self.heapList[newV]
                    self.heapList[newV] = flip

               # update indexes
                    self.heapList[child].heapIndex = child
                    self.heapList[newV].heapIndex = newV
                    newV = child
                else:
                    return self
            except:
                pass

    def push(self, edge, key):
        self.len += 1
        edge = Edge(edge.sr, edge.ds, key)  # new Edge
        edge.heapIndex = self.len - 1
        self.heapList[self.len - 1] = edge
        return self.shiftUp(self.len - 1)

    def update(self, key, index):
        if self.heapList[index].w > key:
            self.heapList[index].w = key
            return self.shiftUp(index)
        else:
            self.heapList[index].w = key
            return self.shiftDown(index)
        return self

    def heap(self):
        return self.len

    def pop(self):
        self.len -= 1
        popped = self.heapList[0]
        popped.heapIndex = float('inf')

        self.heapList[0] = self.heapList[self.len]
        self.shiftDown(0)

        return popped




