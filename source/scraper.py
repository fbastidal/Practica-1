# -*- coding: utf-8 -*-

import io
import csv
import time
from datetime import datetime
from selenium import webdriver                                     # Drivers de Firefox y Chrome
from selenium.webdriver.common.by import By                        # Per a localitzar elements en una pàgina
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

class RobotsConfig:
  def __init__(self, allowed, disallowed, delay):
    self.allowed = allowed
    self.disallowed = disallowed
    self.delay = delay
    
    
class VesselInfo:
    def __init__(self):
        self.nombre = ""
        self.tipo = ""
        self.eslora = ""
        self.manga = ""
        self.calado = ""
        self.anyo = ""
        self.origen = ""
        self.bandera = ""
        self.imo = ""
        self.puertoDestino = ""
        self.urlPuertoDestino = ""
        self.puertoOrigen = ""
        self.urlPuertoOrigen = ""
        self.ETA = ""
        self.ETAPredecido = ""
        self.distancia = ""
        self.tiempo = ""
        self.rumbo = ""
        self.velocidad = ""
        self.caladoActual = ""
        self.estadoNavegacion = ""
        self.ultimaPosicionRecibida = ""
        self.MMSI = ""
        self.signal = ""
        self.GT = ""
        self.DWT = ""
        self.TEU = ""
        self.crudo = ""
        self.grano = ""
        self.fardo = ""
        self.puerto01_nombre = ""
        self.puerto01_llegada = ""
        self.puerto01_salida = ""
        self.puerto01_tiempo = ""
        self.puerto02_nombre = ""
        self.puerto02_llegada = ""
        self.puerto02_salida = ""
        self.puerto02_tiempo = ""
        self.puerto03_nombre = ""
        self.puerto03_llegada = ""
        self.puerto03_salida = ""
        self.puerto03_tiempo = ""
        self.puerto04_nombre = ""
        self.puerto04_llegada = ""
        self.puerto04_salida = ""
        self.puerto04_tiempo = ""
        self.puerto05_nombre = ""
        self.puerto05_llegada = ""
        self.puerto05_salida = ""
        self.puerto05_tiempo = ""


def ParseRobots(sUrl):
    print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] Lectura del fitxer robots.txt iniciada")
    
    # Preparem les variables amb els valors per defecte
    iDelay = 0
    lAllowed = []
    lDisallowed = []
        
    # Primer llegim i fem un parsing del fitxer robots
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    browser = webdriver.Chrome(options=option)
    browser.get(sUrl)

    # Buscarem el "User-agent: *", ja que és el que ens aplica
    elemRobots = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'pre')))
    bufRobots = io.StringIO(str(elemRobots.text))

    # Només volem revisar la informació referent al user-agent general, ja que utilitzarem un crawler no típic
    print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] Parsing del fitxer robots.txt iniciat")
    sUserAgent = ""    
    for sRobotsLine in bufRobots:
        if "User-agent: *" in sRobotsLine:
            sUserAgent = "*"
        elif "User-agent" in sRobotsLine:
            sUserAgent = ""
        
        # En el cas de trobar-nos dins la descripció del user-agent general, fem un parsing de les dades:
        if sUserAgent == "*":
            if "Allow: *" in sRobotsLine:
                lAllowed.append((sRobotsLine.split(': '))[1])
            elif "Disallow: *" in sRobotsLine:
                lDisallowed.append((sRobotsLine.split(': '))[1])
            elif "Crawl-delay" in sRobotsLine:
                iDelay = int((sRobotsLine.split(': '))[1])

    print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] Parsing del fitxer robots.txt finalitzat")
    print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] Lectura del fitxer robots.txt finalitzada")
    
    # Retornem l'objecte amb la configuració del robot/crawler: 
    return(RobotsConfig(lAllowed, lDisallowed, iDelay))


def CheckUrlIsAllowed(sUrl, vAllowed, vDisallowed):
    # Comprovem si la ruta que es vol raspar està inclosa o no dins el fitxer robots i, per tant, si està permesa o no
    print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] Comprovant si la URL " + sUrl + " està permesa al fitxer robots.txt")
    bAllowed = True
    bFinish = False
    for sAllowed in vAllowed:
        if (bFinish == False) and (sAllowed.replace('*','') in sUrl):
            bFinish == True
    
    for sDisallowed in vDisallowed:
        if (bFinish == False) and (sDisallowed.replace('*','') in sUrl):
            bAllowed == False
            bFinish == True
                
    # Si no es trobava en cap de les llistes de permesos o no, llavors la considerem com a permesa
    return(bAllowed)


def ScrapVesselData(sUrl, browser, delay):
    # Carregam la pàgina del baixell
    browser.get(sUrl)
    time.sleep(delay)
   
    # Identificam la taula dades
    print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] Raspant dades del vaixell amb URL " + sUrl)
    try:
        taula = browser.find_element(By.XPATH, '//table[@class="aparams"]')
    except NoSuchElementException:
        print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [WARN] Sense dades a la URL " + sUrl)
        return(None)   
    
    # Creem el nou objecte que contindrà la informació del vaixell i iniciem el raspat de les dades
    oVessel = VesselInfo()
    iteradorFiles = taula.find_elements(By.XPATH, '//tr')
    for fila in iteradorFiles:
        atribut = ""
        try:
            atribut = fila.find_element(By.CLASS_NAME, 'n3').get_attribute('innerText')
            valor = fila.find_element(By.CLASS_NAME, 'v3').get_attribute('innerText')
        except NoSuchElementException:
            print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [WARN] Sense dades a la URL " + sUrl + " per la fila actual")
            continue
        
        if (atribut == "Nombre del buque"):
            oVessel.nombre = valor
        elif (atribut == "Tipo de barco"):
            oVessel.tipo = valor
        elif (atribut == "Eslora (m)"):
            oVessel.eslora = valor
        elif (atribut == "Manga (m)"):
            oVessel.manga = valor
        elif (atribut == "Calado (m)"):
            oVessel.calado = valor
        elif (atribut == "Año de construccion"):
            oVessel.anyo = valor
        elif (atribut == "Lugar de construccion"):
            oVessel.origen = valor
        elif (atribut == "Bandera"):
            oVessel.bandera = valor
        elif (atribut == "Numero IMO"):
            oVessel.imo = valor
        elif (atribut == "Predicted ETA"):
            oVessel.ETAPredecido = valor
        elif (atribut == "Distance / Time"):
            if ('/' in valor):
                sTemp = valor.split(' / ')
                oVessel.distancia = sTemp[0]
                oVessel.tiempo = sTemp[1]
            else:
                oVessel.distancia = ""
                oVessel.tiempo = ""
        elif (atribut == "Rumbo / Velocidad"):
            if ('/' in valor):
                sTemp = valor.split(' / ')
                oVessel.rumbo = sTemp[0]
                oVessel.velocidad = sTemp[1]
            else:
                oVessel.rumbo = ""
                oVessel.velocidad = ""
        elif (atribut == "Calado actual"):
            oVessel.caladoActual = valor
        elif (atribut == "Navigation Status"):
            oVessel.estadoNavegacion = valor
        elif (atribut == "IMO / MMSI"):
            if ('/' in valor):
                sTemp = valor.split(' / ')
                oVessel.MMSI = sTemp[1]
            else:
                oVessel.MMSI = ""
        elif (atribut == "Señal de llamada"):
            oVessel.signal = valor
        elif (atribut == "GT"):
            oVessel.GT = valor
        elif (atribut == "DWT (t)"):
            oVessel.DWT = valor
        elif (atribut == "TEU"):
            oVessel.TEU = valor
        elif (atribut == "Crudo (bbl)"):
            oVessel.crudo = valor
        elif (atribut == "Grano"):
            oVessel.grano = valor
        elif (atribut == "Fardo"):
            oVessel.fardo = valor
        elif (atribut == "Position received"):
            oVessel.ultimaPosicionRecibida = fila.find_element(By.CLASS_NAME, 'v3').get_attribute('data-title')
    
    # Recuperem els detalls dels últims ports que ha visitat el vaixell, en cas d'existir:
    oPortCalls = browser.find_elements(By.XPATH, '/html/body/div[1]/div/main/div/section[3]/div/div[2]/div[1]/div')
    
    if (len(oPortCalls) > 0):
        i = 1
        for portCall in oPortCalls:
            # Hi ha un màxim de 5 entrades corresponents als ports, així que controlem a quin port corresponen les dades
            if (i == 1):
                portTimes = portCall.find_elements(By.CLASS_NAME, '_1GQkK')
                portCallPortName = portCall.find_elements(By.TAG_NAME, 'a')
                if (len(portCallPortName) > 0):
                    oVessel.puerto01_nombre = (portCall.find_element(By.TAG_NAME, 'a')).get_attribute('text')
                else:
                    oVessel.puerto01_nombre = portCall.find_element(By.CLASS_NAME, 'flx').text
                oVessel.puerto01_llegada = portTimes[0].text
                oVessel.puerto01_salida = portTimes[1].text
                oVessel.puerto01_tiempo = portTimes[2].text
            elif (i == 2):
                portTimes = portCall.find_elements(By.CLASS_NAME, '_1GQkK')
                portCallPortName = portCall.find_elements(By.TAG_NAME, 'a')
                if (len(portCallPortName) > 0):
                    oVessel.puerto02_nombre = (portCall.find_element(By.TAG_NAME, 'a')).get_attribute('text')
                else:
                    oVessel.puerto02_nombre = portCall.find_element(By.CLASS_NAME, 'flx').text
                oVessel.puerto02_llegada = portTimes[0].text
                oVessel.puerto02_salida = portTimes[1].text
                oVessel.puerto02_tiempo = portTimes[2].text
            elif (i == 3):
                portTimes = portCall.find_elements(By.CLASS_NAME, '_1GQkK')
                portCallPortName = portCall.find_elements(By.TAG_NAME, 'a')
                if (len(portCallPortName) > 0):
                    oVessel.puerto03_nombre = (portCall.find_element(By.TAG_NAME, 'a')).get_attribute('text')
                else:
                    oVessel.puerto03_nombre = portCall.find_element(By.CLASS_NAME, 'flx').text
                oVessel.puerto03_llegada = portTimes[0].text
                oVessel.puerto03_salida = portTimes[1].text
                oVessel.puerto03_tiempo = portTimes[2].text
            elif (i == 4):
                portTimes = portCall.find_elements(By.CLASS_NAME, '_1GQkK')
                portCallPortName = portCall.find_elements(By.TAG_NAME, 'a')
                if (len(portCallPortName) > 0):
                    oVessel.puerto04_nombre = (portCall.find_element(By.TAG_NAME, 'a')).get_attribute('text')
                else:
                    oVessel.puerto04_nombre = portCall.find_element(By.CLASS_NAME, 'flx').text
                oVessel.puerto04_llegada = portTimes[0].text
                oVessel.puerto04_salida = portTimes[1].text
                oVessel.puerto04_tiempo = portTimes[2].text
            elif (i == 5):
                portTimes = portCall.find_elements(By.CLASS_NAME, '_1GQkK')
                portCallPortName = portCall.find_elements(By.TAG_NAME, 'a')
                if (len(portCallPortName) > 0):
                    oVessel.puerto05_nombre = (portCall.find_element(By.TAG_NAME, 'a')).get_attribute('text')
                else:
                    oVessel.puerto05_nombre = portCall.find_element(By.CLASS_NAME, 'flx').text
                oVessel.puerto05_llegada = portTimes[0].text
                oVessel.puerto05_salida = portTimes[1].text
                oVessel.puerto05_tiempo = portTimes[2].text
            
            # Passem al següent element de la llista de ports
            i += 1
    
    print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] Dades del vaixell amb URL " + sUrl + " raspades")
    
    # Retornem l'objecte que conté tota la informació del vaixell actual
    return(oVessel)


def ScrapVessels(sUrl, maxVaixells, vAllowed, vDisallowed, iDelay):
    print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] Raspat del llistat de vaixells iniciat")
    
    # Obrim el navegador Chrome
    browser = webdriver.Chrome()
    time.sleep(iDelay)
        
    # Carregam la pàgina principal de la base de dades de vaixells AIS
    if CheckUrlIsAllowed(sUrl, vAllowed, vDisallowed):
        print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] URL " + sUrl + " permesa al fitxer robots.txt")
        browser.get(sUrl)
        time.sleep(iDelay)
        
        # Cream un índex dels vaixells que anam a registrar
        indexVaixells = []
        numVaixells = 0 # Inicialment cap vaixell
        
        while numVaixells < maxVaixells:
            # Validam que el títol de la pàgina correspon amb el que esperam
            assert "Barcos base de datos - VesselFinder" in browser.title
        
            # Cream un iterador tots els enllaços a fitxes de vaixells
            iteradorVaixells = browser.find_elements(By.XPATH, '//a[@class="ship-link"]')
        
            # Recorrem l'iterador
            for vaixell in iteradorVaixells:
                numVaixells += 1
                indexVaixells.append([vaixell.get_attribute("href")])
                if numVaixells >= maxVaixells:
                    break;
        
            if numVaixells < maxVaixells:
                # Com que no tenim prou vaixells avançam a la següent pàgina
                botoNext = browser.find_element(By.XPATH, '//link[@rel="next"]')
                sUrl = botoNext.get_attribute("href")
                if CheckUrlIsAllowed(sUrl, vAllowed, vDisallowed):
                    print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] URL " + sUrl + " permesa al fitxer robots.txt")
                    browser.get(sUrl)
                    time.sleep(iDelay)
                else:
                    print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [WARN] URL " + sUrl + " NO permesa al fitxer robots.txt")
        
        # Una vegada que tenim l'índex de tots els Vaixells recollim les seves dades
        llistaVaixells = []
        for index in indexVaixells:
            sUrl = index[0]            
            if CheckUrlIsAllowed(sUrl, vAllowed, vDisallowed):
                print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] URL " + sUrl + " permesa al fitxer robots.txt")
                
                # Fem el raspat del vaixell en curs
                oVessel = ScrapVesselData(sUrl, browser, iDelay)
                                
                # Es guarden les dades obtingudes (falten les dades AIS)
                if oVessel != None:
                    llistaVaixells.append(oVessel)
            else:
                print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] URL " + sUrl + " NO permesa al fitxer robots.txt")
                
        # Retornem el llistat de vaixells que s'han pogut raspar
        print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] Raspat del llistat de vaixells finalitzat")
        return(llistaVaixells)           
    else:
        print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] Raspat del llistat de vaixells finalitzat")
        print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [WARN] URL " + sUrl + " NO permesa al fitxer robots.txt")
        return(None)
        
        
def ExportVesselsData(vesselsList, output):
    # Exportem el contingut del llistat de vaixells, format per objectes de la classe "VesselInfo"
    if (vesselsList != None) and (output != None):
        # Obrim la ruta especificada i procedim a generar el fitxer amb les dades raspades
        with open(output,"w", newline='') as fitxer:
            writer = csv.writer(fitxer)
            
            # Afegim la capçalera del fitxer csv
            writer.writerow(["nombre", "tipo", "eslora", "manga", "calado", "año", "origen", "bandera", "imo", "puertoDestino", "urlPuertoDestino", "puertoOrigen", "urlPuertoOrigen", "ETA", "ETAPredecido", "distancia", "tiempo", "rumbo", "velocidad", "caladoActual", "estadoNavegacion", "ultimaPosicionRecibida", "MMSI", "signal", "GT", "DWT", "TEU", "crudo", "grano", "fardo", "puerto01_nombre", "puerto01_llegada", "puerto01_salida", "puerto01_tiempo", "puerto02_nombre", "puerto02_llegada", "puerto02_salida", "puerto02_tiempo", "puerto03_nombre", "puerto03_llegada", "puerto03_salida", "puerto03_tiempo", "puerto04_nombre", "puerto04_llegada", "puerto04_salida", "puerto04_tiempo", "puerto05_nombre", "puerto05_llegada", "puerto05_salida", "puerto05_tiempo"])
            
            # Afegim les dades de tots els vaixells que s'han raspat
            for vessel in vesselsList:
                writer.writerow([vessel.nombre, vessel.tipo, vessel.eslora, vessel.manga, vessel.calado, vessel.anyo, vessel.origen, vessel.bandera, vessel.imo, vessel.puertoDestino, vessel.urlPuertoDestino, vessel.puertoOrigen, vessel.urlPuertoOrigen, vessel.ETA, vessel.ETAPredecido, vessel.distancia, vessel.tiempo, vessel.rumbo, vessel.velocidad, vessel.caladoActual, vessel.estadoNavegacion, vessel.ultimaPosicionRecibida, vessel.MMSI, vessel.signal, vessel.GT, vessel.DWT, vessel.TEU, vessel.crudo, vessel.grano, vessel.fardo, vessel.puerto01_nombre, vessel.puerto01_llegada, vessel.puerto01_salida, vessel.puerto01_tiempo, vessel.puerto02_nombre, vessel.puerto02_llegada, vessel.puerto02_salida, vessel.puerto02_tiempo, vessel.puerto03_nombre, vessel.puerto03_llegada, vessel.puerto03_salida, vessel.puerto03_tiempo, vessel.puerto04_nombre, vessel.puerto04_llegada, vessel.puerto04_salida, vessel.puerto04_tiempo, vessel.puerto05_nombre, vessel.puerto05_llegada, vessel.puerto05_salida, vessel.puerto05_tiempo])