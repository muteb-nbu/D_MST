#from MST import *
from Ribeiro import *
import random
import time
import sys
from copy import copy
import xlsxwriter
'''
running
        "python3 scriptName File1 File2"
    Where:
    File1 is the file containning the Graph
    File2 is the file containing the operations
            a = add edge
            d = delete edge
'''

sumIncMA= 0
sumDecMA= 0
sumIncRIB= 0
sumDecRIB= 0
sumPrim = 0
workbook = xlsxwriter.Workbook(str(str(sys.argv[4])+".xlsx"))
worksheet = workbook.add_worksheet(str(sys.argv[4]))
worksheet.write(0,0,"round")
worksheet.write(0,1,"RIB_DEC")
worksheet.write(0,2,"MA_DEC")
worksheet.write(0,3,"RIB_INC")
worksheet.write(0,4,"MA_INC")
worksheet.write(0,5,"Prime")
for i in range(0,5):
    print(" Working on Exp. {} , round.# {}".format(str(sys.argv[4]), i))
    source = 2
    G = Graph(source)
    G2 = Graph(source)
    
    # initiate sets of operations
    insertList= set()
    insertList2 = set()


    # reading from file1 to create the graph G (MA) and G2 (RIB)
    file1 = sys.argv[1]
    with open(file1, 'r') as f:
        for v in range(0,int(f.readline())):
            G.addVertex(v)
            G2.addVertex(v)
        for line in f:
            split = line.split()
            x = int(split[0])
            y = int(split[1])
            w = int(split[2])
            G.addEdge(x, y, w)
            G.addEdge(y, x, w)
            G2.addEdge(x, y, w)
            G2.addEdge(y, x, w)
    
    # reading the updates from file2
    # Collect the updated edges
    file2 = sys.argv[2]
    with open(file2, 'r') as f2:
        for line in f2:
            #print(line)
            split = line.split()
            op = split[0]
            x = int(split[1])
            y = int(split[2])
            w = int(split[3])
            if op =='a': 
                insertList.add(Edge(x,y,w))
                insertList2.add(Edge(x,y,w))

           

    # build th MST for MA Alg.
    mst = MST(source)
    mst.init_MST(G.numVertices)
    start = time.time()
    # Builing Prim's Alg.
    mst.primMST(G,source)
    end = time.time()
    prime = end-start
    sumPrim+= prime



    # build the MST for RIB
      
    MST_RIB = RIB(source)
    edges =[]
    for e in G2.edgeList:  ###########3 No need maybe 
        edges.append(((e.sr,e.ds),e.w))
    MST_RIB.init_MST(G2.edgeList, G2.numVertices)
    MST_RIB.primMST(G2,source)
    
    RIB_INC = 0
    RIB_DEC = 0
    MA_INC = 0
    MA_DEC = 0
    numOP = int(sys.argv[3])
    for num in range(0, numOP):
        opINC = insertList.pop()
        opDec = copy(opINC)
        opDec.w = opDec.w*2
        
        
        
        # Testing MA DEC ####################
        start = time.time()
        edge = copy(opDec)
        # Update the graph
        for e in G.vertList[edge.sr].edges:
            if e.ds == edge.ds:
                e.w = edge.w

        for e in G.vertList[edge.ds].edges:
            if e.ds == edge.sr:
                e.w = edge.w
        
        # Update edgeList
        G.updateEdge(edge.sr,edge.ds, edge.w)

        # Update THE EDGE FROM THE TREE
        for e in G.vertList[edge.sr].edges:
            if e.ds == edge.ds:
                e.w = edge.w
                break
        for e in G.vertList[edge.ds].edges:
            if e.ds == edge.sr:
                e.w = edge.w
                break
        if (mst.treeList[edge.sr].parent and mst.treeList[edge.ds].parent):
            if mst.treeList[edge.sr].parent.sr ==edge.ds or mst.treeList[edge.ds].parent.sr ==edge.sr:
                mst.decMST(G, edge.sr, edge.ds, edge.w)
                sumDecMA+= 1
        else:
            mst.decMST(G, edge.sr, edge.ds, edge.w)
            sumDecMA+= 1
        MA_DEC += time.time()-start
        
        
        
        # Testing MA INC  ####################
        start = time.time()
        edge = copy(opINC)
        
        for e in G.vertList[edge.sr].edges:
            if e.ds == edge.ds:
                e.w = edge.w
                #print(sumIncMA, "  d1")
                break
        for e in G.vertList[edge.ds].edges:
            if e.ds == edge.sr:
                e.w = edge.w
                #print(sumIncMA, "  d2")
                break
        # Update edgeList
        G.updateEdge(edge.sr,edge.ds, edge.w)
        
        # Update The Tree
        for e in mst.treeList[edge.sr].getChildren():
            if e.ds == edge.ds:
                e.w = edge.w
                #print(sumIncMA, "  u1")
                break
        for e in mst.treeList[edge.ds].getChildren():
            if e.ds == edge.sr:
                e.w = edge.w
                #print(sumIncMA, "  u2")
                break
        mst.incMST( edge.sr, edge.ds, edge.w)
        sumIncMA+=1
        MA_INC += time.time()-start
        
        
        
        
        ## Testing RIB DEC   #################
        start = time.time()
        edge = copy(opDec)
        index1 = 0
        index2 = 0
        s = 0
        f = 0
        # fix by going directly to the edge through the source pointers
        for e in G2.vertList[edge.sr].edges:
            if e.ds == edge.ds:
                e.w = edge.w
                index1 = e.AIndex 
                if index1:
                    MST_RIB.A[index1].w = edge.w
                    s = index1
                break
        for e in G2.vertList[edge.ds].edges:
            if e.ds == edge.sr:
                e.w = edge.w
                index2 = e.AIndex 
                MST_RIB.A[index2].w = edge.w
                if index2:
                    if index2 < index1:
                        s = index2
                break
              
                
        for e in MST_RIB.treeList[edge.sr].getChildren():
            if e.ds == edge.ds:
                e.w = edge.w
                break
                
        for e in MST_RIB.treeList[edge.ds].getChildren():
            if e.ds == edge.sr:
                e.w = edge.w
                break
                
        MST_RIB.sort_A()
        
        # finding f 
        for e in G2.vertList[edge.sr].edges:
            if e.ds == edge.ds:
                index1 = e.AIndex 
                e.w =  edge.w
                if index1:
                    f = index1
                break
        for e in G2.vertList[edge.ds].edges:
            if e.ds == edge.sr:
                index2 = e.AIndex 
                e.w =  edge.w
                if index2:
                    if index2 > f:
                        f = index2
                break
        if (MST_RIB.treeList[edge.sr].parent and MST_RIB.treeList[edge.ds].parent):
            if MST_RIB.treeList[edge.sr].parent.sr ==edge.ds or MST_RIB.treeList[edge.ds].parent.sr ==edge.sr:
                MST_RIB.RIB_DEC(G2, edge.sr, edge.ds, s, f, edge.w)
                sumDecRIB+=1
        else:
            MST_RIB.RIB_DEC(G2, edge.sr, edge.ds, s, f, edge.w)
            sumDecRIB+=1
        
        RIB_DEC += time.time()-start
                
                
                
                
        # Testing RIB INC
        start = time.time()
        edge = copy(opINC)
        # Update Graph and the List A
        for e in G2.vertList[edge.sr].edges:
            if e.ds == edge.ds:
                e.w = edge.w
                index1 = e.AIndex 
                if index1:
                    MST_RIB.A[index1].w = edge.w
                break
        for e in G2.vertList[edge.ds].edges:
            if e.ds == edge.sr:
                e.w = edge.w
                index2 = e.AIndex 
                if index2:
                    MST_RIB.A[index2].w = edge.w
                break
        # Update The Tree
        for e in MST_RIB.treeList[edge.sr].getChildren():
            if e.ds == edge.ds:
                e.w = edge.w
                break
        for e in MST_RIB.treeList[edge.ds].getChildren():
            if e.ds == edge.sr:
                e.w = edge.w
                break

        MST_RIB.sort_A()
        MST_RIB.RIB_INC(edge.sr, edge.ds, edge.w)
        sumIncRIB+=1
        RIB_INC += time.time()-start
        

    worksheet.write((i+1),1,RIB_DEC)
    worksheet.write((i+1),2,MA_DEC)
    worksheet.write((i+1),3,RIB_INC)
    worksheet.write((i+1),4,MA_INC)
    worksheet.write((i+1),4,MA_INC)
    
    

    mstTest = MST(source)
    mstTest.init_MST(G.numVertices)
    start = time.time()
    # Builing Prim's Alg.
    mstTest.primMST(G,source)
    end = time.time()-start
    worksheet.write((i+1),1,RIB_DEC)
    worksheet.write((i+1),2,MA_DEC)
    worksheet.write((i+1),3,RIB_INC)
    worksheet.write((i+1),4,MA_INC)
    worksheet.write((i+1),4,MA_INC)
    worksheet.write((i+1),5,end)
    
    
    
    '''
    verify correcteness of algorithms after all operations
    '''

    sumW = 0
    workSet = set()
    workSet.add(source)
    while(len(workSet)):
        x = workSet.pop()
        for e in mstTest.treeList[x].getChildren():
            if mstTest.treeList[e.ds].parent:
                if mstTest.treeList[e.ds].parent.sr == x:
                    sumW+=e.w
                    workSet.add(e.ds)
    print(" Sum of Edge's Whights in Prim Alg. =", sumW)


    sumW = 0
    workSet = set()
    workSet.add(source)
    while(len(workSet)):
        x = workSet.pop()
        for e in MST_RIB.treeList[x].getChildren():
            if MST_RIB.treeList[e.ds].parent:
                if MST_RIB.treeList[e.ds].parent.sr == x:
                    sumW+=e.w
                    workSet.add(e.ds)
    print(" Sum of Edge's Whights in MST_RIB =", sumW)


    sumW = 0
    workSet = set()
    workSet.add(source)
    while(len(workSet)):
        x = workSet.pop()
        for e in mst.treeList[x].getChildren():
            if mst.treeList[e.ds].parent:
                if mst.treeList[e.ds].parent.sr == x:
                    sumW+=e.w
                    workSet.add(e.ds)
    print(" Sum of Edge's Whights in MA alg.  =", sumW)
 
        
    del G 
    del G2
    del mst, insertList
    del MST_RIB
    time.sleep(1)
       
workbook.close()


# number of updated edge operations of each
print("Updates for RIB_DEC ", sumDecRIB)
print("Updates for RIB_INC ", sumIncRIB)
print("Updates for MA_DEC ", sumDecMA)
print("Updates for MA_INC ", sumIncMA)
    
    
    
   