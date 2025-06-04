import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()

    #ES 1
    def getIdStores(self):
        return DAO.getStores()

    def buildGraph(self, store, k):
        ordini = DAO.getOrdiniStore(store)
        self._idMap = {}
        for o in ordini:
            self._idMap[o.order_id] = o

        self._graph.clear()
        self._graph.add_nodes_from(ordini)

        archi = DAO.getArchi(store, k, self._idMap)
        for a in archi:
            if a.ordine1 in self._graph and a.ordine2 in self._graph:
                self._graph.add_edge(a.ordine1, a.ordine2, weight=a.peso) #riga cambiata

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getNodi(self, store):
        return DAO.getOrdiniStore(store)

    def camminoPiuLungo(self, start):
        nodoPartenza = self._idMap[start]
        cammino = list(nx.dfs_preorder_nodes(self._graph, nodoPartenza)) #perchè non posso fare nx.dfs_tree
        return cammino

    #ES 2
    def trovaPercorsoOttimo(self, source):
        self._percorsoOttimo = []
        self._pesoOttimo = 0

        sourceObj = self._idMap[source]
        parziale =[sourceObj]
        parziale_edges = []

        self._ricorsione(parziale, parziale_edges)

        return self._percorsoOttimo, self._pesoOttimo

    def _ricorsione(self, parziale, parziale_edges):
        ultimo_nodo = parziale[-1]
        nodi_da_esplorare = list(self._graph.successors(ultimo_nodo))

        if not nodi_da_esplorare:
            peso = self._getPesoPercorso(parziale_edges)
            if peso > self._pesoOttimo:
                self._pesoOttimo = peso
                self._percorsoOttimo = copy.deepcopy(parziale_edges)
            return

        for n in nodi_da_esplorare:
            if n not in parziale:
                peso_arco = self._graph[ultimo_nodo][n]["weight"]
                nuovo_arco = (ultimo_nodo, n, peso_arco)

                parziale_edges.append(nuovo_arco)

                if self._ammissibilitaArco(parziale_edges):
                    parziale.append(n)
                    self._ricorsione(parziale, parziale_edges)
                    parziale.pop()

                parziale_edges.pop()

    def _ammissibilitaArco(self, parziale_edges):
        if len(parziale_edges) < 2:
            return True
        return parziale_edges[-2][2] < parziale_edges[-1][2]

    def _getPesoPercorso(self, parziale_edges):
        pesoTot = 0
        for a in parziale_edges:
            pesoTot += a[2]
        return pesoTot







