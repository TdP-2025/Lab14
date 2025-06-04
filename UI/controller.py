import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDStore(self):
        stores = self._model.getIdStores()

        for s in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(text=s.store_id,
                                                                  data=s))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        store = self._view._ddStore.value
        if not store:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Seleziona un store", color="red"))
            self._view.update_page()
            return

        k = self._view._txtIntK.value
        if not k:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegli un numero di giorni", color="red"))
            self._view.update_page()
            return

        try:
            kInt = int(k)
        except ValueError:
            print("Formato sbagliato")
            return


        self._model.buildGraph(store, kInt)
        self.fillDDNodi()

        nodes, edges = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {edges}"))

        self._view.update_page()


    def fillDDNodi(self):
        store = self._view._ddStore.value
        if not store:
            self._view.txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Seleziona un store", color="red"))
            self._view.update_page()
            return

        self._view._ddNode.options.clear()
        ordini = self._model.getNodi(store)

        for o in ordini:
            self._view._ddNode.options.append(ft.dropdown.Option(text=o.order_id,
                                                                  data=o))
        self._view.update_page()

    def handleCerca(self, e):
        nodoPartenza = self._view._ddNode.value
        if not nodoPartenza:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegli un nodo da cui vuoi partirei", color="red"))
            self._view.update_page()
            return

        cammino = self._model.camminoPiuLungo(int(nodoPartenza)) #meglio fare con try+except

        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {nodoPartenza}"))
        for n in cammino[1:]:
            self._view.txt_result.controls.append(ft.Text(n))

        self._view.update_page()

    def handleRicorsione(self, e):
        nodoPartenza = self._view._ddNode.value
        if not nodoPartenza:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegli un nodo da cui vuoi partirei", color="red"))
            self._view.update_page()
            return

        try:
            nodoId = int(nodoPartenza)
        except ValueError:
            print("Il formato sbagliato")
            return

        percorso, peso = self._model.trovaPercorsoOttimo(nodoId)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Il peso massimo: {peso}"))
        for a in percorso:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]} -> {a[1]}: {a[2]}"))

        self._view.update_page()