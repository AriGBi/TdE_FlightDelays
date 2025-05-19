import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._idMapAirports={}
        self.airports=DAO.getAllAirports()
        for a in self.airports:
            self._idMapAirports[a.ID]=a
        self._bestPath = []
        self._bestObjFun = 0

    def getCamminoOttimo(self, v0,v1,t): #prende in input l'aereoporto di partenza, quello di arrivo e il numero massimo di tratte che si vuole percorrere
        self._bestPath=[] #carichiamo alla fine il percorso migliore
        self._bestObjFun=0 #costo max

        parziale=[v0] #lista di aeroporti che visitiamo, il primo lo sappiamo già perche è quello di partenza
        self._ricorsione(parziale,v1,t)
        return self._bestPath,self._bestObjFun

    def _ricorsione(self, parziale, v1, t): # devo passare aereoporto di arrivo e numero massimo di aereoporti da visitare per vedere se sono arrivata alla fine
        #condizione terminale
        if parziale[-1]==v1: #l'ultimo nodo visitato deve essere l'aeroporto di destinazione
            #verificare se parziale è l'ottimo (se è meglio del best corrente)
            if self._getObjFun(parziale)>self._bestObjFun: #se il costo della parziale è migliore del costo migliore trovato finora
                self._bestObjFun=self._getObjFun(parziale)
                self._bestPath=copy.deepcopy(parziale)
        if len(parziale)==t+1: #se ho superato il massimo di tratte che posso fare, esco
            return

        #se non sono alla condizione terminale, posso ancora aggiungere nodi
        #partendo dall'ultimo nodo che ho aggiunto, prendo i vicini e aggiungo e poi faccio ripartire la ricorsione
        for n in self._graph.neighbors(parziale[-1]): #per ogni
            if n not in parziale: #devo controllare che il nodo che sto visitando non l'ho già visitato prima
                parziale.append(n)
                self._ricorsione(parziale, v1, t)
                parziale.pop()


    def _getObjFun(self, listOfNodes):
        """prende in ingresso la lista di nodi parziale e calcola il costo"""
        #costo= somma dei pesi di tutti gli archi attraversati
        #dovrò fare un ciclo su tutti i valori di parziale
        objval=0
        for i in range(0,len(listOfNodes)-1): #ciclo sui nodi
            objval+=self._graph[listOfNodes[i]][listOfNodes[i+1]]["weight"] #prendo il PESO dell'arco tra un nodo della lista e il suo successivo
        return objval

    def buildGraph(self,nMin):
        nodes=DAO.getAllNodes(nMin,self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        self._graph.clear_edges()
        self.addAllArchiV1()
        print("N nodi: ", len(self._graph.nodes), "archi: ", len(self._graph.edges))


    def addAllArchiV1(self):
        allEdges=DAO.getAllEdgesV1(self._idMapAirports)
        for edge in allEdges: #edge è un oggetto Arco quindi posso accedere ai suoi attributi
            if edge.aeroportoP in self._graph and edge.aeroportoD in self._graph: #controllo se i nodi ci sono già
                if self._graph.has_edge(edge.aeroportoP, edge.aeroportoD): #se l'arco c'è già, incremento il peso
                    self._graph[edge.aeroportoP][edge.aeroportoD]["weight"]+=edge.peso
                else:
                    self._graph.add_edge(edge.aeroportoP, edge.aeroportoD,weight=edge.peso)


    def addAllArchiv2(self):
        allEdges=DAO.getAllEdgesV2(self._idMapAirports)
        for edge in allEdges:
            if edge.aeroportoP in self._graph and edge.aeroportoD in self._graph:
                self._graph.add_edge(edge.aeroportoP, edge.aeroportoD, weight=edge.peso)

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllNodes(self):
        nodes=list(self._graph.nodes())
        nodes.sort(key=lambda x:x.IATA_CODE)
        return nodes

    def getSortedNeighbors(self,node):
        neighbors= self._graph.neighbors(node)
        neighbTuples=[]
        for n in neighbors:
            neighbTuples.append((n, self._graph[node][n]["weight"])) #lista di tuple con (nodoVicino,pesoPerRaggiungerlo) rispetto al nodo source passato come parametro
        neighbTuples.sort(key=lambda x:x[1], reverse=True) #sorto in base al secondo elemento della tupla --> i pesi
        return neighbTuples

    def getPath(self,v0,v1):
        path=nx.dijkstra_path(self._graph,v0,v1, weight=None)
        #path=nx.shortest_path(self._graph,v0,v1)

        return path


