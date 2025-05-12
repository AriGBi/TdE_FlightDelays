import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph
        self._idMapAirports={}
        self.airports=DAO.getAllAirports()
        for a in self.airports:
            self._idMapAirports[a.ID]=a


    def buildGraph(self,nMin):
        nodes=DAO.getAllNodes(nMin,self._idMapAirports)
        self._graph.add_node(nodes)
