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


def ScrapVessels(sUrl, maxVaixells, allowed, disallowed, delay):
    # Obrim el navegado Chrome
    browser = webdriver.Chrome()
    
    # Carregam la pàgina principal de la base de dades de vaixells AIS
    browser.get(sUrl)
    
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
            browser.get(botoNext.get_attribute("href"))
    
    
    # Una vegada que tenim l'índex de tots els Vaixells recollim les seves dades
    llistaVaixells = []
    i = 1
    for index in indexVaixells:
        print(str(i) + ". " + index[0])
        
        # Carregam la pàgina del baixell
        browser.get(index[0])
    
        #----------------------------------------------------------------------
        # DATOS MAESTROS
        #----------------------------------------------------------------------
        
        # Identificam la taula dades
        try:
            taula = browser.find_element(By.XPATH, '//table[@class="aparams"]')
        except NoSuchElementException:
            print("  Sense taula de paràmetres")
            llistaVaixells.append([i,"","",index[0],"","","","","","",""])
            i += 1
            continue
        iteradorFiles = taula.find_elements(By.XPATH, '//tr')
        
        # Netejam les variables a llegir
        nombre = ""
        tipo = ""
        eslora = ""
        manga = ""
        calado = ""
        año = ""
        origen = ""
        bandera = ""
        imo = ""
        sPuertoDestino = ""
        sUrlPuertoDestino = ""
        sPuertoOrigen = ""
        sUrlPuertoOrigen = ""
        sETA = ""
        sETAPredecido = ""
        sDistancia = ""
        sTiempo = ""
        sRumbo = ""
        sVelocidad = ""
        sCaladoActual = ""
        sEstadoNavegacion = ""
        sUltimaPosicionRecibida = ""
        sMMSI = ""
        sSignal = "" 
        sGT = "" 
        sDWT = "" 
        sTEU = "" 
        sCrudo = "" 
        sGrano = "" 
        sFardo = "" 
        
        for fila in iteradorFiles:
            try:
                atribut = fila.find_element(By.CLASS_NAME, 'n3').get_attribute('innerText')
                valor = fila.find_element(By.CLASS_NAME, 'v3').get_attribute('innerText')
            except NoSuchElementException:
                continue;
            print("   " + atribut + ": " + valor)
            match atribut:
                case "Nombre del buque":
                    nombre = valor
                case "Tipo de barco":
                    tipo = valor
                case "Eslora (m)":
                    eslora = valor
                case "Manga (m)":
                    manga = valor
                case "Calado (m)":
                    calado = valor
                case "Año de construccion":
                    año = valor
                case "Lugar de construccion":
                    origen = valor
                case "Bandera":
                    bandera = valor
                case "Numero IMO":
                    imo = valor
                case "Predicted ETA":
                    sETAPredecido = valor
                case "Distance / Time":
                    if ('/' in valor):
                        sTemp = valor.split(' / ')
                        sDistancia = sTemp[0]
                        sTiempo = sTemp[1]
                    else:
                        sDistancia = ""
                        sTiempo = ""
                case "Rumbo / Velocidad":
                    if ('/' in valor):
                        sTemp = valor.split(' / ')
                        sRumbo = sTemp[0]
                        sVelocidad = sTemp[1]
                    else:
                        sRumbo = ""
                        sVelocidad = ""
                case "Calado actual":
                    sCaladoActual = valor
                case "Navigation Status":
                    sEstadoNavegacion = valor
                case "IMO / MMSI":
                    if ('/' in valor):
                        sTemp = valor.split(' / ')
                        sMMSI = sTemp[1]
                    else:
                        sMMSI = ""
                case "Señal de llamada":
                    sSignal = valor
                case "GT":
                    sGT = valor
                case "DWT (t)":
                    sDWT = valor
                case "TEU":
                    sTEU = valor
                case "Crudo (bbl)":
                    sCrudo = valor
                case "Grano":
                    sGrano = valor
                case "Fardo":
                    sFardo = valor
            
        # Finalment fem scraping d'altres valors interessants
        elemShipSection = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'ship-section')))
        sUltimaPosicionRecibida        
        
        # Es guarden les dades obtingudes (falten les dades AIS)
        llistaVaixells.append([i,nombre,imo,index[0],tipo,eslora,manga,calado,bandera,año,origen])
        i += 1
        
    with open("Vaixells.txt","w") as fitxer:
        fitxer.write("Id, Nombre, IMO, URL, Tipo, Eslora, MAnga, Calado, Bandera, Año, Construccion\n")
        for vaixell in llistaVaixells:
            fitxer.write(str(vaixell[0])+", "+vaixell[1]+", "+vaixell[2]+", "+vaixell[3]+", "+vaixell[4]+", "+vaixell[5]+", "+vaixell[6]+", "+vaixell[7]+", "+vaixell[8]+", "+vaixell[9]+", "+vaixell[10]+"\n")
