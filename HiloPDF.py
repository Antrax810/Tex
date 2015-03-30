import threading
import urllib2

class HiloPDF(threading.Thread):
    
    def __init__(self, url):
        threading.Thread.__init__(self)
        urlDividido = url.split("/")
        self.__nombre = urlDividido[len(urlDividido) - 1]
        self.__url = url
            
    
    def run(self):
        try:
            conexion = urllib2.urlopen(self.__url)
            salida =file(self.__nombre,"w") 
            salida.write(conexion.read()) 
            salida.close() 
            print self.__nombre + " download"        
        except Exception:
            print "Error - " + self.__url