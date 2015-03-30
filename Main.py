import WebCrawler
import HiloAnalizar
import HiloLogin
import HiloPDF
import sys
import pycurl
import time
import StringIO

def imprimirCabecera():
    print "  \t\t\t\t _______        "
    print " \t\t\t\t|__   __|     "  
    print "\t\t\t\t   | | _____  __"
    print "\t\t\t\t   | |/ _ \ \/ /"
    print "\t\t\t\t   | |  __/>  < "
    print "\t\t\t\t   |_|\___/_/\\_\\"
    print "\n\t\t\t\t   ShadowHackers"
    print "\n\t\t\t\t     Antrax810"
    print "\nShadowHackers: https://www.facebook.com/pages/ShadowHackers/852985464762163?ref=hl"
    print "\nShadowHackers: http://www.shadowhackers.org/"
    print "\nAntrax810: https://www.facebook.com/Antrax810"
                                  
                                                                                     
                                                                                     
def imprimirAyuda():
    print "\n\n[+]Developer: Antrax810\n"
    print "-d <page>: (Objetivo-Target)"
    print "-t <int>: (Numero de Hilos-Number of Threads) Default 5"
    print "-l <int>: (Limite de paginas a Analizar-Limit pages to Analyze) Default 100000"
    print "-h <int>: (Tiempo en minutos-Time in minutes) Default 5"
    print "-i <int>: (1.- Espanol / 2.- English) Default 1.- Espanol"
    print "-f: (Buscar pagina de Login-Search page Login) Default No"
 


def getPaginaPrincipal(pagina):
    paginaDividida = pagina.split("/")
    paginaVerificar = ""
    
    try:
        salida = StringIO.StringIO()
        paginaVerificar=paginaDividida[0]+"//"+paginaDividida[2]+"/"
        conexion = pycurl.Curl()
        conexion.setopt(pycurl.CONNECTTIMEOUT, 1)
        conexion.setopt(pycurl.URL, paginaVerificar)
        conexion.setopt(pycurl.NOBODY, True)
        conexion.setopt(pycurl.WRITEFUNCTION, salida.write)
        conexion.perform()
        if int(conexion.getinfo(pycurl.RESPONSE_CODE)) != 200 and int(conexion.getinfo(pycurl.RESPONSE_CODE)) != 404 :
            paginaVerificar = conexion.getinfo(pycurl.REDIRECT_URL)
        elif int(conexion.getinfo(pycurl.RESPONSE_CODE)) == 200 and int(conexion.getinfo(pycurl.RESPONSE_CODE)) != 404:
            paginaVerificar = paginaVerificar
    except pycurl.error:
        pass    
    finally:
        return paginaVerificar



#Opciones
if "-d" in sys.argv:
    try:    
        paginaAtacar = sys.argv[sys.argv.index("-d")+1]
        if not paginaAtacar.startswith("http"):
            paginaAtacar = "http://" + paginaAtacar
    except IndexError:
        paginaAtacar = None
else:
    paginaAtacar = None




if "-t" in sys.argv:
    try:
        limiteHilos = int(sys.argv[sys.argv.index("-t")+1])
    except IndexError:
        limiteHilos = 5
else:
    limiteHilos = 5
    
    
    
if "-h" in sys.argv:
    try:
        limiteTiempo = int(sys.argv[sys.argv.index("-h")+1])
        if limiteTiempo > 59:
            limiteTiempo = 59
        if limiteTiempo <= 0:
            limiteTiempo = 5
    except ValueError:
        limiteTiempo = 5
else:
    limiteTiempo = 5
    
    
    
if "-l" in sys.argv:
    try:
        limitePaginas = int(sys.argv[sys.argv.index("-l")+1])
    except ValueError:
        limitePaginas = 100000
else:
    limitePaginas = 100000
        


if "-i" in sys.argv:
    try:
        idioma = int(sys.argv[sys.argv.index("-i") + 1])
    except ValueError:
        idioma = 1
    if idioma != 2 and idioma != 1:
        idioma = 1
else:
    idioma = 1


if "-f" in sys.argv:
    buscarPaginaLogin = True
else:
    buscarPaginaLogin = False
        
#Variables
obtenerEnlaces = "\n\n[+]Obteniendo enlaces...\n\n"
subdominioTexto = "\n\n[+]Subdominio: "
enlaceExterno = "\n\n[+]Enlace externo: "
buscarLogin = "\n\n[+]Buscando pagina de Login...\n"
pdf = "\n\n[+]Archivos PDF"
totales = "Totales: "
indice = "\n[+]Indice: "
ayudaPdf = "\nEscriba <int-int>: Para descargar un rango\nEscriba <int,int,*>: Para descargar los Archivos seleccionados\nNumero negativo para salir\n"
descargarPdf = "\n\n[+]Descargar PDF...\n"

if idioma == 2:
    obtenerEnlaces = "\n\n[+]Getting links...\n\n"
    subdominioTexto = "\n\n[+]Subdomain: "
    enlaceExterno = "\n\n[+]External link: " 
    buscarLogin = "\n\n[+]Seeking page Login...\n"
    pdf = "\n\n[+]PDF files"
    totales = "Totals: "
    indice = "\n[+]Index: "
    ayudaPdf = "\nType <int-int>: To download a range \nType <int,int,*>: To download the selected files\nNumber negative to exit\n"
    descargarPdf = "\n\n[+]Download PDF...\n"


imprimirCabecera()
#Ejecucion del Codigo
if paginaAtacar == None:
    imprimirAyuda()
else:
    print obtenerEnlaces
    paginaReal = getPaginaPrincipal(paginaAtacar)
    webCrawler = WebCrawler.WebCrawler(paginaReal, limiteHilos, limiteTiempo)
    webCrawler.agregarEnlace(paginaAtacar)
    paginasAnalizadas = 0
    #Calcular Dominio principal
    enlaceDividido = paginaReal.split("/")[2]
    dominioDividido = enlaceDividido.split(".")
    objetivo = dominioDividido[len(dominioDividido) - 2]
    while paginasAnalizadas <= limitePaginas:
        try:
            if webCrawler.getNumeroHilos() < webCrawler.getLimiteHilos():
                pagina = webCrawler.getEnlaces()[paginasAnalizadas]
                hilo = HiloAnalizar.HiloAnalizar(pagina, paginaReal, webCrawler)
                hilo.start()
                tiempoEjecucion = webCrawler.getHoraActual() - webCrawler.getHoraInicio()
                paginasAnalizadas = paginasAnalizadas + 1
                if tiempoEjecucion >= limiteTiempo:
                    break
            else:
                time.sleep(2)
        except IndexError:
            tiempoEjecucion = webCrawler.getHoraActual() - webCrawler.getHoraInicio()
            if tiempoEjecucion >= limiteTiempo:
                break
            continue
    
    
    
    #Encontrar subdominios
    listaSubdominios = list()
    listaExternos = list()
    listaPdf = list()
    contadorGeneral = 0
    for enlace in webCrawler.getEnlaces():
        try:
            enlaceDividido = enlace.split("/")
            if not enlaceDividido[2] in listaSubdominios and objetivo in enlaceDividido[2]:
                listaSubdominios.append(enlaceDividido[2])
            #Buscar enlaces externos
            if not enlaceDividido[2] in listaExternos and len(enlaceDividido[2]) > 0 and not objetivo in enlaceDividido[2]:
                listaExternos.append(enlaceDividido[2])
            #Buscar Archivos PDF
            if enlace.endswith(".pdf"):
                listaPdf.append(enlace)
        except IndexError:
            pass
    
    #Mostrar por subdominios
    for subdominio in listaSubdominios:
        print subdominioTexto + subdominio 
        for enlace in webCrawler.getEnlaces():
            try:
                enlaceDividido = enlace.split("/")
                if subdominio.startswith(enlaceDividido[2]) and enlace.startswith("http") and len(enlace) > 9:
                    print  "\t" + enlace
                    contadorGeneral +=1
                
            except IndexError:
                pass
            
        print "\n"
    
    
    #Mostrar enlaces externos
    for externo in listaExternos:
        print enlaceExterno + externo 
        for enlace in webCrawler.getEnlaces():
            try:
                enlaceDividido = enlace.split("/")
                if externo.startswith(enlaceDividido[2]) and enlace.startswith("http") and len(enlace) > 9:
                    print "\t" + enlace
                    contadorGeneral +=1
            except IndexError:
                pass
    
    #Mostrar PDF
    print pdf
    for contador in range(len(listaPdf)):
        print "\t" + str(contador) +" = " + listaPdf[contador]
        
    print "\n" + totales + str(contadorGeneral)
    
    
    #Buscar pagina de Login
    if buscarPaginaLogin == True:
        print "\n\n" + buscarLogin
        posiblesLogin= ['admin.php','admin/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/',
                    'admin_area/','panel-administracion/','instadmin/','memberadmin/', 'administratorlogin/','adm/',
                    'admin/account.php','admin/index.php','admin/login.php','admin/admin.php','admin/account.php',
                    'joomla/administrator','login.php', 'admin_area/admin.php','admin_area/login.php','siteadmin/login.php'
                    ,'siteadmin/index.php','siteadmin/login.html','admin/account.html','admin/index.html','admin/login.html'
                    , 'admin/admin.html','admin_area/index.php','bb-admin/index.php','bb-admin/login.php','bb-admin/admin.php'
                    ,'admin/home.php','admin_area/login.html','admin_area/index.html', 'admin/controlpanel.php','admincp/index.asp'
                    ,'admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html','webadmin/index.html'
                    ,'webadmin/admin.html', 'webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html'
                    ,'admin/cp.php','cp.php','administrator/index.php','administrator/login.php', 'nsw/admin/login.php','webadmin/login.php'
                    ,'admin/admin_login.php','admin_login.php','administrator/account.php','administrator.php','admin_area/admin.html'
                    ,'pages/admin/admin-login.php', 'admin/admin-login.php','admin-login.php','bb-admin/index.html','bb-admin/login.html'
                    ,'bb-admin/admin.html','admin/home.html','modelsearch/login.php','moderator.php','moderator/login.php', 'moderator/admin.php'
                    ,'account.php','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.php'
                    ,'admincontrol.php', 'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.php'
                    ,'adminarea/index.html','adminarea/admin.html','webadmin.php', 'webadmin/index.php','webadmin/admin.php','admin/controlpanel.html'
                    ,'admin.html','admin/cp.html','cp.html','adminpanel.php','moderator.html','administrator/index.html','administrator/login.html'
                    , 'user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html','moderator/login.html'
                    ,'adminarea/login.html','panel-administracion/index.html', 'panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html'
                    ,'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.php','account.html', 'controlpanel.html'
                    ,'admincontrol.html','panel-administracion/login.php','wp-login.php','adminLogin.php','admin/adminLogin.php','home.php','adminarea/index.php'
                    ,'adminarea/admin.php','adminarea/login.php', 'panel-administracion/index.php','panel-administracion/admin.php','modelsearch/index.php'
                    ,'modelsearch/admin.php','admincontrol/login.php','adm/admloginuser.php','admloginuser.php','admin2.php', 'admin2/login.php','admin2/index.php'
                    ,'adm/index.php','adm.php','affiliate.php','adm_auth.php','memberadmin.php','administratorlogin.php','administrador/']
    
        for pagina in posiblesLogin:
            if webCrawler.getNumeroHilos() <= webCrawler.getLimiteHilos():
                pagina = paginaReal + "/" + pagina
                hilo = HiloLogin.HiloLogin(pagina, webCrawler)
                hilo.start()
                hilo.join()
            else:
                time.sleep(1)
        
        #Imprimit los Login
        for login in webCrawler.getLogin():
            print "\t" + login
    
    
    #Buscar y descargar los pdf
    print descargarPdf
    quitar = False
    while quitar == False:
        numero = raw_input(indice)
        listaIndice = numero.split(",")
        listaLimite = numero.split("-")
        #Descargar seleccionados
        for posicion in listaIndice:
            try:
                posicion = int(posicion)
                if posicion < 0:
                    quitar = True
                else:
                    pagina = listaPdf[posicion]
                    hiloPdf = HiloPDF.HiloPDF(pagina)
                    hiloPdf.start()
                    hiloPdf.join()                   
            except Exception:
                ayudaPdf
            
        #Descargar limites
        try:
            limiteUno = int(listaLimite[0])
            limiteDos = int(listaLimite[1])
            for posicion in range(limiteUno, limiteDos):
                posicion = int(posicion)
                if posicion < 0:
                    quitar = True
                pagina = listaPdf[posicion]
                hiloPdf = HiloPDF.HiloPDF(pagina)
                hiloPdf.start()
                hiloPdf.join()
        except Exception:
            ayudaPdf
        
        #Selecciona un solo archivo
        if len(listaIndice) == 1 and len(listaLimite) == 1:
            try:
                posicion = int(posicion)
                if posicion < 0:
                    quitar = True
                else:
                    pagina = listaPdf[posicion]
                    hiloPdf = HiloPDF.HiloPDF(pagina)
                    hiloPdf.start()
            except Exception:
                print ayudaPdf   
                
sys.exit(0)
            
        
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    