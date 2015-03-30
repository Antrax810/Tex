import pycurl
import threading
import WebCrawler
import StringIO

class HiloAnalizar(threading.Thread):
    
    def __init__(self, pagina, paginaReal, WebCrawler):
        threading.Thread.__init__(self)
        self.__pagina = pagina
        self.__paginaReal = paginaReal
        self.__webCrawler = WebCrawler
        
            
    def run(self):
        try:
            self.__webCrawler.aumentarHilo()
            salida = StringIO.StringIO()
            conexion = pycurl.Curl()
            conexion.setopt(pycurl.URL, self.__pagina)
            conexion.setopt(pycurl.NOSIGNAL, 1)
            conexion.setopt(pycurl.WRITEFUNCTION, salida.write)
            conexion.perform()
            #Verificar si el enlace conectado es una subpagina
            if int(conexion.getinfo(pycurl.RESPONSE_CODE)) == 301:
                paginaRedireccion = conexion.getinfo(pycurl.REDIRECT_URL)
                self.__webCrawler.agregarEnlace(paginaRedireccion)
            else:
                #Analizar paginas
                lineas = str(salida.getvalue()).split("<")
                for linea in lineas:
                    if "href" in linea and not "<link" in linea:
                        atributos = linea.strip().split(" ")
                        for atributo in atributos:
                            if "href=" in atributo:
                                try:
                                    atributo = atributo.split("\"")[1]
                                    if len(atributo) > 1:
                                        if not atributo.startswith("http"):
                                            atributo = self.__paginaReal + atributo
                                        if not atributo in self.__webCrawler.getEnlaces():
                                            self.__webCrawler.agregarEnlace(atributo)
                                except IndexError:
                                    pass
            self.__webCrawler.quitarHilo()    
            conexion.close()
        except pycurl.error:
              conexion.close()
              self.__webCrawler.quitarHilo()
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    