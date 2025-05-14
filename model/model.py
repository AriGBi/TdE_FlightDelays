import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._idMapAirports={}
        self.airports=DAO.getAllAirports()
        for a in self.airports:
            self._idMapAirports[a.ID]=a


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


