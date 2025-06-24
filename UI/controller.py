import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._store = None


    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        try:
            num_giorni = int(self._view._txtIntK.value)

        except:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("ERRORE: INTERISCI UN NUMERO INTERO NEL CAMPO 'NUMERO GIORNI'"))
            self._view.update_page()
            return

        if  self._store is None:
            self._view.txt_result.controls.append(ft.Text("ERRORE: INTERISCI UNO STORE.'"))
            self._view.update_page()
            return

        ok, nodes, edges = self._model.create_graph(self._store.store_id, num_giorni)


        if(ok):
            self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
            self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {len(nodes)}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero archi: {len(edges)}"))

            self._view._btnCerca.disabled = False
            self._view._btnRicorsione.disabled = False
            self._view._ddNode.options = []

            for node in nodes:
                self._view._ddNode.options.append(ft.dropdown.Option(text = node.order_id,
                                                                     data = node,
                                                                     on_click = self.readDDNode))

        else:
            self._view.txt_result.append(ft.Text("Errore nella creazione del grafo."))

        self._view.update_page()
        return



    def handleCerca(self, e):
        if self._view._ddNode.value == None or self._view._ddNode.value=="" :
            self._view.txt_result.controls.append(ft.Text("Inserisci un nodo"))
            self._view.update_page()
            return

        percorso = self._model.cercaPercorso(self._view._ddNode.value)

        for node in percorso:
            self._view.txt_result.controls.append(ft.Text(node))

        self._view.update_page()
        return


    def handleRicorsione(self, e):
        self._model.cercaPercorsoMax(self._iniziale.order_id)
        return


    def _fillddStore(self):
        elementi = self._model.getStores()

        self._view._ddStore.options = []
        for el in elementi:

            self._view._ddStore.options.append(ft.dropdown.Option(text = el.store_id,
                                                                  data =  el,
                                                                  on_click = self.readDDStore))

    def readDDStore(self, e):
        self._store = e.control.data

    def readDDNode(self,e):
        self._iniziale = e.control.data
