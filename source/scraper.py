# -*- coding: utf-8 -*-

import io
import time
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


def ParseRobots(sUrl):
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

    # Retornem l'objecte amb la configuració del robot/crawler: 
    return(RobotsConfig(lAllowed, lDisallowed, iDelay))


def CheckUrlIsAllowed(sUrl, vAllowed, vDisallowed):
    # Comprovem si la ruta que es vol raspar està inclosa o no dins el fitxer robots i, per tant, si està permesa o no
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
    try:
        taula = browser.find_element(By.XPATH, '//table[@class="aparams"]')
    except NoSuchElementException:
        return(None)
    
    iteradorFiles = taula.find_elements(By.XPATH, '//tr')
    
    # Creem el nou objecte que contindrà la informació del vaixell
    oVessel = VesselInfo()
    
    for fila in iteradorFiles:
        atribut = ""
        try:
            atribut = fila.find_element(By.CLASS_NAME, 'n3').get_attribute('innerText')
            valor = fila.find_element(By.CLASS_NAME, 'v3').get_attribute('innerText')
        except NoSuchElementException:
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
            
            print(oVessel.MMSI)
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
    
    # Retornem l'objecte que conté tota la informació del vaixell actual
    return(oVessel)


def ScrapVessels(sUrl, maxVaixells, vAllowed, vDisallowed, iDelay):
    # Obrim el navegado Chrome
    browser = webdriver.Chrome()
    time.sleep(iDelay)
        
    # Carregam la pàgina principal de la base de dades de vaixells AIS
    if CheckUrlIsAllowed(sUrl, vAllowed, vDisallowed):
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
                    browser.get(sUrl)
                    time.sleep(iDelay)
        
        
        # Una vegada que tenim l'índex de tots els Vaixells recollim les seves dades
        llistaVaixells = []
        for index in indexVaixells:
            sUrl = index[0]            
            if CheckUrlIsAllowed(sUrl, vAllowed, vDisallowed):
                # Fem el raspat del vaixell en curs
                oVessel = ScrapVesselData(sUrl, browser, iDelay)
                                
                # Es guarden les dades obtingudes (falten les dades AIS)
                llistaVaixells.append(oVessel)
                
        # Retornem el llistat de vaixells que s'han pogut raspar
        
            
#        with open("Vaixells.txt","w") as fitxer:
#            fitxer.write("Id, Nombre, IMO, URL, Tipo, Eslora, MAnga, Calado, Bandera, Año, Construccion\n")
#            for vaixell in llistaVaixells:
#                fitxer.write(str(vaixell[0])+", "+vaixell[1]+", "+vaixell[2]+", "+vaixell[3]+", "+vaixell[4]+", "+vaixell[5]+", "+vaixell[6]+", "+vaixell[7]+", "+vaixell[8]+", "+vaixell[9]+", "+vaixell[10]+"\n")
    else:
        print("URL no permesa al fitxer robots.txt!!!")
        return(None)
        
        
#def ExportVesselsData(vesselsList, output):