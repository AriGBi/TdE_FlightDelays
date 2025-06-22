import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo=nx.Graph()
        self._nodi=[]
        self.idMap={}
        self._bestPath=[]
        self._maxCost=0


    def getBestPath(self, source, destination, tMax):
        self._bestPath = []
        self._maxCost = 0
        parziale=[source]
        self.ricorsione(parziale,destination,tMax)
        return self._bestPath, self._maxCost

    def ricorsione(self,parziale,destination,tMax):
            if (parziale[-1]==destination and self.calcolaCosto(parziale)>self._maxCost):
                self._bestPath=copy.deepcopy(parziale)
                self._maxCost=self.calcolaCosto(parziale)
            if (len(parziale) == tMax +1):
                return
            for nodo in self._grafo.neighbors(parziale[-1]):
                if nodo not in parziale:
                    parziale.append(nodo)
                    self.ricorsione(parziale,destination,tMax)
                    parziale.pop()

    def calcolaCosto(self, parziale):
        costo=0
        for i in range(0,len(parziale)-1):
            costo+=self._grafo[parziale[i]][parziale[i+1]]["weight"]
        return costo

    def buildGraph(self, minCompagnie):
        self._grafo.clear()
        self._nodi=DAO.getAirposts(minCompagnie)
        self._grafo.add_nodes_from(self._nodi)
        self.fillIdMap()
        archiProvvisori=DAO.getEdges(self.idMap)
        for arco in archiProvvisori:
            if arco.aeroportoP in self._grafo and arco.aeroportoD in self._grafo:
                self.add_or_sum_Edge(arco)
        return self._grafo.nodes, self._grafo.edges, self._grafo


    def fillIdMap(self):
        self.idMap = {}
        for nodo in self._nodi:
            self.idMap[nodo.ID]=nodo


    def add_or_sum_Edge(self,arco): #chiesto a chat
        if self._grafo.has_edge(arco.aeroportoP, arco.aeroportoD) :
            self._grafo[arco.aeroportoP][arco.aeroportoD]["weight"] += arco.peso
        else:
            self._grafo.add_edge(arco.aeroportoP, arco.aeroportoD, weight=arco.peso)


    def getAdiacenti(self, source):
        #vicini=self._grafo.neighbors(source)
        viciniOrdinati=sorted(self._grafo[source].items(), key=lambda edge: edge[1]["weight"], reverse=True) #TROVATO SU INTERNET --> ORDINA I NODI VICINI IN BASE AL PESO
        return viciniOrdinati


    def getPercorso(self,source,destination):
        path=nx.shortest_path(self._grafo,source,destination) #prendo il percorso piu corto (potevo prenderne uno qualunque)
        return path

