import pycurl
import threading
import WebCrawler

class HiloLogin(threading.Thread):
    
    def __init__(self, paginaAnalizar, webCrawler):
        threading.Thread.__init__(self)
        self.__paginaAnalizar = paginaAnalizar
        self.__webCrawler = webCrawler
    
    def run(self):
        try:
            conexion = pycurl.Curl()
            conexion.setopt(pycurl.URL, self.__paginaAnalizar)
            conexion.setopt(pycurl.NOBODY, True)
            conexion.perform()
            if conexion.getinfo(pycurl.RESPONSE_CODE) == 200:
                self.__webCrawler.agregarLogin(self.__paginaAnalizar)     
            conexion.close() 
        except pycurl.error:
            conexion.close()
        