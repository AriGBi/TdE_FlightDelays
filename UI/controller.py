import flet as ft
from datetime import datetime

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._numCompagnieMin=None
        self.airportPScelto=None
        self.airportDScelto=None
        self._maxTratte=None
        self._grafo=None

    def handleAnalizza(self,e):
        self._numCompagnieMin= self._view._txtInCMin.value
        if self._numCompagnieMin is None or self._numCompagnieMin=="":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, inserire un numero di compagnie minimo", color="red"))
            self._view.update_page()
            return
        try:
            numCompagnieMinINT=int(self._numCompagnieMin)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, inserire un numero intero", color="red"))
            self._view.update_page()
            return

        if numCompagnieMinINT <= 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un intero positivo."))
            self._view.update_page()
            return

        self.nodi,archi, self._grafo=self._model.buildGraph(numCompagnieMinINT)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo costruito correttamente."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha: {len(list(self.nodi))} nodi e {len(list(archi))} archi."))
        self._view._ddAeroportoP.disabled=False
        self._view._btnConnesso.disabled = False
        self._view._ddAereoportoD.disabled = False
        self.fillDDs()
        self._view.update_page()
        return



    def handleConnessi(self,e):
        if  self.airportPScelto is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegliere un aereoporto di partenza"))
            self._view.update_page()
            return
        viciniOrdinati = self._model.getAdiacenti(self.airportPScelto)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Gli aeroporti vicini a {self.airportPScelto.AIRPORT} sono:"))
        for vicino in viciniOrdinati:
            self._view.txt_result.controls.append(
                ft.Text(f"{vicino[0].AIRPORT} - peso: {vicino[1]['weight']}"))
        self._view.update_page()
        return

    def handlePercorso(self,e):
        self._maxTratte=self._view._txtInTratteMax.value
        if self._maxTratte is None or self._maxTratte=="":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, scegliere un numero massimo di tratte", color="red"))
            self._view.update_page()
            return
        try:
            numTratteMaxINT = int(self._maxTratte)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, inserire un numero intero", color="red"))
            self._view.update_page()
            return
        if numTratteMaxINT <= 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un intero positivo."))
            self._view.update_page()
            return
        if self.airportDScelto is None or self.airportPScelto is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegliere un aereoporto di partenza e uno di destinazione"))
            self._view.update_page()
            return
        path, cost=self._model.getBestPath(self.airportPScelto,self.airportDScelto,numTratteMaxINT)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Percorso con numero massimo di voli trovato:"))
        for nodo in path:
            self._view.txt_result.controls.append(ft.Text(f"{nodo.AIRPORT} "))
        self._view.txt_result.controls.append(ft.Text(f"Numero totale di voli: {cost}"))
        self._view.update_page()
        return

    def handleCerca(self,e):
        pass

    def fillDDs(self):
        for nodo in self.nodi:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(data=nodo, key=nodo.AIRPORT, on_click=self.readDDAirportP))
            self._view._ddAereoportoD.options.append( ft.dropdown.Option(data=nodo, key=nodo.AIRPORT, on_click=self.readDDAirportD))

    def readDDAirportP(self,e):
        self.airportPScelto = e.control.data

    def readDDAirportD(self,e):
        self.airportDScelto = e.control.data
