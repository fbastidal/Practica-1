# -*- coding: utf-8 -*-

import time
from datetime import datetime
from scraper import *

# Definim la funciño principal desde la que es treballarà:
def main():
    print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] Lectura del fitxer robots.txt")
    oParsedRobots = ParseRobots('https://www.vesselfinder.com/robots.txt')
    
    # Iniciem el web scraping
    maxVaixells = 5
    sOutputFilePath = "vessels_test.csv"
    oVesselsList = ScrapVessels('https://www.vesselfinder.com/es/vessels', maxVaixells, oParsedRobots.allowed, oParsedRobots.disallowed, oParsedRobots.delay)
    ExportVesselsData(oVesselsList, sOutputFilePath)

if __name__ == "__main__":
    main()