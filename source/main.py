# -*- coding: utf-8 -*-

import time
from datetime import datetime
from scraper import *

class ScraperOptions:
    def __init__(self):
        self.maxVaixells = 0
        self.outputFile = ""
        self.urlLogin = "https://www.vesselfinder.com/es/login"
        self.usuariLogin = "fbastidal@uoc.edu"
        self.passwordLogin = "Pra1_Cicle_de_Vida"
        self.urlRobot = "https://www.vesselfinder.com/robots.txt"
        self.urlScrapper = "https://www.vesselfinder.com/es/vessels"

# Creem una funció per ensenyar el menú inicial i obtenir les opcions a utilitzar
def ShowMenu():
    # Guardarem les opcions en un objecte de la classe "ScraperOptions"
    oScraperOptions = ScraperOptions()
    
    print("===============================================================================")
    print("                                      .                                        ")
    print("                                    .^~:                                       ")
    print("                                   .^~~~^.                                     ")
    print("                                  :^^~^~~~:                                    ")
    print("  ...                           .:^^^~^^~~~^.                                  ")
    print("  .:^^^~~~^^^^::.....          .^^^^^~^^~~~~~:                  .....:^~!7~.   ")
    print("    .::::^^~~!!!!77777!!~~~^^.:^^^^^~~^^~~~~~~^. ..........:::^^~!77??JJ7^     ")
    print("     ..::::::::^^~!!7777777!^^^^^^^^~~^^~~~~~~~~:.......:^^~!7????????7^       ")
    print("       .:::::::::::::^^~!!~^^^^^^^^^~~^^~~~~~~~~~^:^^~!77?????7777777^         ")
    print("         .:::::::::::::::::::^^^^^^^~~^^^~~~~!!!777777777777777777!^           ")
    print("           .::::::::::::::::::::::^^~~~!!77777777777777777!!!!!7!^.            ")
    print("            ..:::::::::::::::::^^^~~!!!!!777777777!!!!!!!!!!!!!^.              ")
    print("              ..::::::::::::^^~~~~~~~~~~~~~~!!!!!!!!!!!!!!!!~^.                ")
    print("                ..:::::^^^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:.                 ")
    print("                  .:^~~!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!~~^::....             ")
    print("                    ..::^^~~~~~~!!!!!!!!!!!!!!!!!!!!!~~~~^^::::....            ")
    print("                           .....::::::::::::^^^^^:::::::::::......             ")
    print("                                   .............................               ")
    print("                                                                               ")
    print("-------------------------------------------------------------------------------")
    print("                                                                               ")
    print("                            VESSEL SCRAPER v1.0                                ")
    print("   Pràctica 1 – Tipologia i cicle de vida de les dades (semestre: 2022/23-2)   ")
    print("                                                                               ")
    print("===============================================================================")
    print("")
    value = input("De quants vaixells vols intentar raspar dades?: ")
    
    if (value.isnumeric()):
        oScraperOptions.maxVaixells = int(value)
        
        # Necessitem recuperar la direcció del fitxer CSV de sortida
        print("")
        value = input("Ruta del fitxer CSV on vols salvar les dades raspades (inclou la ruta i el nom del fitxer):\n")
        oScraperOptions.outputFile = value
    else:
        print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [ERROR] El valor introduït no és de tipus numèric!!")
        oScraperOptions.maxVaixells = 0

    return(oScraperOptions)

# Definim la funció principal desde la que es treballarà
def main():
    # Mostrem el menú inicial per obtenir les opcions del raspat
    oScraperOptions = ShowMenu()
        
    # Iniciem el web scraping
    if (oScraperOptions.maxVaixells > 0):
        # Primer revisem el fitxer "robots.txt" de la web
        oParsedRobots = ParseRobots(oScraperOptions.urlRobot)
        
        # Iniciem el procés de raspat
        oVesselsList = ScrapVessels(oScraperOptions, oParsedRobots )
        ExportVesselsData(oVesselsList, oScraperOptions.outputFile)
    else:
        print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] [INFO] No hi ha vaixells a raspar")

if __name__ == "__main__":
    main()
    