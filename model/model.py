import copy

import networkx as nx
import database.DAO as DAO

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._dao = DAO.DAO()
        self._idMap = {}
        self._best = None
        self._costo_best = 0


    def getStores(self):
        return self._dao.getStores()


    def create_graph(self, id_store, num_giorni):
        self._graph.clear()
        nodi = self._dao.getNodes(id_store)
        self._graph.add_nodes_from(nodi)

        for sale in nodi:
            self._idMap[sale.order_id] = sale

        archi = self._dao.getEdges(num_giorni, id_store)

        if self._graph is None:
            return False, 0, 0

        for arco in archi:
            if (arco.u in self._idMap.keys()):
                if (arco.v in self._idMap.keys()):
                    self._graph.add_edge(self._idMap[arco.u], self._idMap[arco.v], weight=arco.weight)


        return True, self._graph.nodes(), self._graph.edges()


    def cercaPercorso(self, partenza):
        p = self._idMap[(int(partenza))]
        tree = nx.dfs_tree(self._graph, p)
        nodes = list(tree.nodes())
        sol = []

        for node in nodes:
            temp = [node]

            while (temp[0] != p):
                pred = nx.predecessor(tree, p, temp[0])
                temp.insert(0, pred[0])

            if len(temp) > len(sol):
                sol = copy.deepcopy(temp)

        return sol

    def cercaPercorsoMax(self, sorgente):
        parziale = [self._idMap[sorgente]]
        costo_attuale = -float('inf')

        for nodo in self._graph.neighbors(self._idMap[sorgente]):
            parziale.append(nodo)
            costo_attuale = self.calcola_costo(parziale)
            self._ricorsione(parziale, costo_attuale)
            parziale.pop()

        return self._costo_best, self._best


    def calcola_costo(self, parziale):
        costo = 0
        for i in range(len(parziale)-1):
            costo += self._graph[parziale[i]][parziale[i+1]]['weight']

        return costo


    def viciniAmmissibili(self, nodo, parziale):
        candidati = []
        for candidato in self._graph.neighbors(nodo):
            if (candidato not in parziale and self._graph[parziale[-2]][parziale[-1]]['weight'] > self._graph[parziale[-1]][candidato]['weight']):
                candidati.append(candidato)
        return candidati


    def _ricorsione(self, parziale, costo_attuale):
        if (len(self.viciniAmmissibili(parziale[-1], parziale)) == 0):
            if(self.calcola_costo(parziale) > self._costo_best):
                self._costo_best = self.calcola_costo(parziale)
                self._best = copy.deepcopy(parziale)


        vicini_amm = self.viciniAmmissibili(parziale[-1], parziale)
        for nodo in vicini_amm:
            parziale.append(nodo)
            costo_attuale = self.calcola_costo(parziale)
            self._ricorsione(parziale, costo_attuale)
            parziale.pop()










