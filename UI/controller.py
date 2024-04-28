import copy

import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0
        self._giorni=14
        self._sequenzaOttima=[]

    def handle_umidita_media(self, e):
        dict_umidita=self._model.getUmidita(self._mese)
        self._view.lst_result.controls.append(ft.Text(f"L'umidità nel mese selezionato è:"))
        for citta in dict_umidita:
            tot=0
            for situazione in dict_umidita[citta]:
               tot+=situazione.umidita
            media=tot/len(dict_umidita[citta])
            self._view.lst_result.controls.append(ft.Text(f"{citta}: {round(media,4)}"))
        self._view.update_page()



    def handle_sequenza(self, e):
        dict_umidita=self._model.getUmiditaGiorni(self._mese)
        giorni=0
        list_umidita=[]
        for giorno in dict_umidita:
            list_umidita.append(dict_umidita[giorno])
        print("Inizio ricorsione")
        self._ricorsione(list_umidita,giorni,[],[],0)
        self._sequenzaOttima.sort(key=lambda x: x[1])
        sol=self._sequenzaOttima[0]
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {sol[1]} ed è"))
        for situazione in sol[0]:
            self._view.lst_result.controls.append(ft.Text(f"[{situazione.localita} - {situazione.data}] Umidità={situazione.umidita}"))
        self._view.update_page()
    def read_mese(self, e):
        self._mese = int(e.control.value)

    def _ricorsione(self, list_situazioni,giorno,parziale,req,costo):
        if giorno==self._giorni:
            self._sequenzaOttima.append((copy.deepcopy(parziale),costo))
        else:
            for situazione in list_situazioni[giorno]:
                parziale.append(situazione)
                req.append(situazione.localita)
                if self._situazione_ammissibile(parziale,req,situazione):
                    #if giorno >= 1:
                        #if req[giorno] == req[giorno - 1]:
                            costo += situazione.umidita
                            self._ricorsione(list_situazioni, giorno + 1, parziale, req, costo)
                        #else:
                         #   costo += (100 + situazione.umidita)
                          #  self._ricorsione(list_situazioni, giorno + 1, parziale, req, costo)
                    #else:
                    #    costo += situazione.umidita
                     #   self._ricorsione(list_situazioni, giorno + 1, parziale, req, costo)
                req.pop()
                parziale.pop()

    def _situazione_ammissibile(self, parziale, req, situazione):
        if len(parziale)>3:
            if req[-1]==req[-2]==req[-3]==req[-4]:
                return False
            if req.count(situazione.localita)>6:
                return False
        return True
