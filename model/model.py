from database.meteo_dao import MeteoDao
class Model:
    def __init__(self):
        self._meteo_dao=MeteoDao()

    def getUmidita(self,mese):
        self.list_situazioni=self._meteo_dao.get_all_situazioni()
        result={}
        for situazione in self.list_situazioni:
            if situazione.data.month==mese:
                if situazione.localita in result:
                    result[situazione.localita].append(situazione)
                else:
                    result[situazione.localita]=[situazione]
        return result
    def getUmiditaGiorni(self,mese):
        self.list_situazioni=self._meteo_dao.get_all_situazioni()
        result={}
        for situazione in self.list_situazioni:
            if situazione.data.month==mese:
                if situazione.data.day in result:
                    result[situazione.data.day].append(situazione)
                else:
                    result[situazione.data.day]=[situazione]
        return result