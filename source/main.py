# -*- coding: utf-8 -*-

import time
from datetime import datetime
from scraper import *

# Definim la funciño principal desde la que es treballarà:
def main():
    print("[" + str(datetime.utcfromtimestamp(time.time())) + " UTC] Lectura del fitxer robots.txt")
    oParsedRobots = ParseRobots('https://www.vesselfinder.com/robots.txt')
    
    # Test del retorn del objecte amb les dades parsejades del fitxer "robots.txt"
    print(oParsedRobots.delay)

if __name__ == "__main__":
    main()