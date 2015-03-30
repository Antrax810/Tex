import datetime

class WebCrawler():
    
    def __init__(self, paginaReal, limiteHilos, limiteTiempo):
        self.__paginaReal = paginaReal
        self.__limiteHilos = limiteHilos
        self.__tiempo = limiteTiempo
        
        self.__enlaces = list()
        self.__enlacesLogin = list()
        self.__numeroHilos = 0
        self.__horaInicio = int(datetime.datetime.now().minute)


    def aumentarHilo(self):
        self.__numeroHilos = self.__numeroHilos + 1
        
        
    def quitarHilo(self):
        self.__numeroHilos = self.__numeroHilos - 1
    
    
    def agregarEnlace(self, pagina):
        self.__enlaces.append(pagina)
    
    
    def agregarLogin(self, pagina):
        self.__enlacesLogin.append(pagina)
    
    
    def getHoraInicio(self):
        return self.__horaInicio
    
    
    def getHoraActual(self):
        return int(datetime.datetime.now().minute)
    
    
    def getNumeroHilos(self):
        return self.__numeroHilos
    
    
    def getLimiteHilos(self):
        return self.__limiteHilos
    
    
    def getEnlaces(self):
        return self.__enlaces


    def getLogin(self):
        return self.__enlacesLogin
    
    
        





























