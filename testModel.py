from model.model import Model
import  networkx as nx
from datetime import datetime

myModel = Model()
nodi=myModel.buildGraph(5)
source=myModel.idMap[2]
destination=myModel.idMap[14]
listaPercorsi=myModel.getPercorso(source, destination)
for nodo in (list(listaPercorsi)):
    print(nodo.AIRPORT)

