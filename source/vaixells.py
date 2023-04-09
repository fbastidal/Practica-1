# -*- coding: utf-8 -*-

from selenium import webdriver # Drivers de Firefox y Chrome
#from selenium.webdriver.common.keys import Keys # Proporciona teclat
from selenium.webdriver.common.by import By # Per a localitzar elements en una pàgina
from selenium.common.exceptions import NoSuchElementException


# Maxim platges
maxVaixells = 100

# Obrim el navegado Chrome
browser = webdriver.Chrome()

# Carregam la pàgina principal de la base de dades de vaixells AIS
browser.get("https://www.vesselfinder.com/es/vessels")

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
    for fila in iteradorFiles:
        try:
            atribut = fila.find_element(By.CLASS_NAME, 'n3').get_attribute('innerText')
            valor = fila.find_element(By.CLASS_NAME, 'v3').get_attribute('innerText')
        except NoSuchElementException:
            continue;
        print("   " + atribut + ": " + valor)
        if atribut == "Nombre del buque":
            nombre = valor
        elif atribut == "Tipo de barco":
            tipo = valor
        elif atribut == "Eslora (m)":
            eslora = valor
        elif atribut == "Manga (m)":
            manga = valor
        elif atribut == "Calado (m)":
            calado = valor
        elif atribut == "Año de construccion":
            año = valor
        elif atribut == "Lugar de construccion":
            origen = valor
        elif atribut == "Bandera":
            bandera = valor
        elif atribut == "Numero IMO":
            imo = valor
    llistaVaixells.append([i,nombre,imo,index[0],tipo,eslora,manga,calado,bandera,año,origen])
    i += 1
    
with open("Vaixells.txt","w") as fitxer:
    fitxer.write("Id, Nombre, IMO, URL, Tipo, Eslora, MAnga, Calado, Bandera, Año, Construccion\n")
    for vaixell in llistaVaixells:
        fitxer.write(str(vaixell[0])+", "+vaixell[1]+", "+vaixell[2]+", "+vaixell[3]+", "+vaixell[4]+", "+vaixell[5]+", "+vaixell[6]+", "+vaixell[7]+", "+vaixell[8]+", "+vaixell[9]+", "+vaixell[10]+"\n")
