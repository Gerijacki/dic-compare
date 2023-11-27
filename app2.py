import os
import requests
import platform
import json
import datetime


VIRUSTOTAL_API_KEY = '964ff6a97060a4512bf3a8047f09964b5a0b6f53055ce5e540e130eb09204b4b'  # api virus total
LOGS_ENABLED = True
LOGS_FOLDER = "logs"

class Colors:
    # Codi d'escape ANSI per colors de text
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

def esborraPantalla():
    if platform.system == 'Linux':
        os.system('clear')
    else:
        os.system('cls')

def cargar_configuracion():
    global VIRUSTOTAL_API_KEY, LOGS_ENABLED, LOGS_FOLDER
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            VIRUSTOTAL_API_KEY = config.get("virustotal_api_key", VIRUSTOTAL_API_KEY)
            LOGS_ENABLED = config.get("logs_enabled", LOGS_ENABLED)
            LOGS_FOLDER = config.get("logs_folder", LOGS_FOLDER)
    except FileNotFoundError:
        # Si no se encuentra el archivo de configuración, se utilizan los valores predeterminados.
        pass

def guardar_configuracion():
    config = {
        "virustotal_api_key": VIRUSTOTAL_API_KEY,
        "logs_enabled": LOGS_ENABLED,
        "logs_folder": LOGS_FOLDER
    }
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=2)

def imprimir_banner():
    banner = f"""
    {Colors.BLUE} _______  __   __  _______  _______  __    _ 
     ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄▄  ▄▄▄▄▄▄▄ ▄     ▄ ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ 
    █       █  █ █  █      █      ██       █ █ ▄ █ █  ▄    █  █ █  █       █       █
    █  ▄▄▄▄▄█  █▄█  █  ▄   █  ▄    █   ▄   █ ██ ██ █ █▄█   █  █▄█  █▄     ▄█    ▄▄▄█
    █ █▄▄▄▄▄█       █ █▄█  █ █ █   █  █ █  █       █       █       █ █   █ █   █▄▄▄ 
    █▄▄▄▄▄  █   ▄   █      █ █▄█   █  █▄█  █       █  ▄   ██▄     ▄█ █   █ █    ▄▄▄█
     ▄▄▄▄▄█ █  █ █  █  ▄   █       █       █   ▄   █ █▄█   █ █   █   █   █ █   █▄▄▄ 
    █▄▄▄▄▄▄▄█▄▄█ █▄▄█▄█ █▄▄█▄▄▄▄▄▄██▄▄▄▄▄▄▄█▄▄█ █▄▄█▄▄▄▄▄▄▄█ █▄▄▄█   █▄▄▄█ █▄▄▄▄▄▄▄█

    """
    print(f"{Colors.RED}{banner}{Colors.RESET}")

def mostra_menu():
    print("\n----- MENU -----")
    print(f"{Colors.RED}1. Mostrar llista de fitxers en directori 1{Colors.RESET}")
    print(f"{Colors.RED}2. Mostrar llista de fitxers en directori 2{Colors.RESET}")
    print(f"{Colors.RED}3. Comparar fitxers en ambdós directoris{Colors.RESET}")
    print(f"{Colors.RED}4. Comparar fitxer específic{Colors.RESET}")
    print(f"{Colors.RED}5. Penjar un fitxer a VirusTotal i verificar malware{Colors.RESET}")
    print(f"{Colors.RED}6. Canviar directoris{Colors.RESET}")
    print(f"{Colors.RED}7. Configuració{Colors.RESET}")
    print(f"{Colors.RED}8. Sortir{Colors.RESET}")

def log_moviment(missatge):
    if LOGS_ENABLED:
        arxiu_log = f"{LOGS_FOLDER}/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log"
        with open(arxiu_log, 'a') as log_file:
            log_file.write(f"{datetime.datetime.now()} - {missatge}\n")

def mostrar_configuracion():
    print(f"\nConfiguració actual:")
    print(f"1. Clau de l'API de VirusTotal: {Colors.MAGENTA}{VIRUSTOTAL_API_KEY}{Colors.RESET}")
    print(f"2. Sistema de logs: {'Activat' if LOGS_ENABLED else 'Desactivat'}")
    print(f"3. Carpeta de logs: {Colors.MAGENTA}{LOGS_FOLDER}{Colors.RESET}")

def configurar_programa():
    global VIRUSTOTAL_API_KEY, LOGS_ENABLED, LOGS_FOLDER
    op_config = input(f"\nSelecciona una opció de configuració ({Colors.RED}1-3{Colors.RESET}, o 'T' per tornar): ")
    
    if op_config == "1":
        VIRUSTOTAL_API_KEY = input(f"{Colors.RED}Introdueix la nova clau de l'API de VirusTotal: {Colors.RESET}")
        log_moviment("S'ha canviat la clau de l'API de VirusTotal.")
    elif op_config == "2":
        LOGS_ENABLED = not LOGS_ENABLED  # Invertir el estado actual
        print(f"Sistema de logs {'activat' if LOGS_ENABLED else 'desactivat'}.")
        log_moviment(f"S'ha {'activat' if LOGS_ENABLED else 'desactivat'} el sistema de logs.")
    elif op_config == "3":
        LOGS_FOLDER = input(f"{Colors.RED}Introdueix la nova carpeta de logs: {Colors.RESET}")
        log_moviment(f"S'ha canviat la carpeta de logs a: {LOGS_FOLDER}")
    elif op_config.lower() == "t":
        return
    else:
        print(f"{Colors.YELLOW}Opció no vàlida.{Colors.RESET}")

    guardar_configuracion()
    print(f"\n{Colors.GREEN}Configuració actualitzada amb èxit.{Colors.RESET}")
    log_moviment("S'ha guardat la configuració del programa.")

def llista_fitxers_directori(directori):
    if os.path.exists(directori):
        try:
            llista_fitxers = os.listdir(directori)
            print(f"\nFitxers en {Colors.RED}{directori}{Colors.RESET}:")
            for fitxer in llista_fitxers:
                ruta_fitxer = os.path.join(directori, fitxer)
                tamany_mb = os.path.getsize(ruta_fitxer) / (1024 * 1024)  # Tamany en megabytes
                tipus_fitxer = "Fitxer" if os.path.isfile(ruta_fitxer) else "Directori"
                print(f"- {Colors.MAGENTA}{fitxer}{Colors.RESET} ({tamany_mb:.2f} MB, {Colors.CYAN}{tipus_fitxer}{Colors.RESET})")
        except FileNotFoundError:
            print(f"\n{Colors.YELLOW}Error: El directori {directori} no existeix.{Colors.RESET}")
    else:
        print(f"\n{Colors.YELLOW}Error: El directori {directori} no existeix.{Colors.RESET}")

def compara_fitxers(directori1, directori2):
    if os.path.exists(directori1) and os.path.exists(directori2):
        llista1 = set(os.listdir(directori1))
        llista2 = set(os.listdir(directori2))

        fitxers_comuns = llista1.intersection(llista2)

        print(f"\nFitxers comuns en ambdós directoris:")
        for fitxer in fitxers_comuns:
            print(f"- {Colors.MAGENTA}{fitxer}{Colors.RESET}")
    else:
        print(f"\n{Colors.YELLOW}Error: Un dels directoris no existeix.{Colors.RESET}")

def compara_fitxer(directori1, directori2, nom_fitxer):
    path1 = os.path.join(directori1, nom_fitxer)
    path2 = os.path.join(directori2, nom_fitxer)

    if os.path.exists(path1) and os.path.exists(path2):
        print(f"\nComparant contingut del fitxer {Colors.MAGENTA}{nom_fitxer}{Colors.RESET} en ambdós directoris:")
        with open(path1, 'rb') as file1, open(path2, 'rb') as file2:
            content1 = file1.read()
            content2 = file2.read()

            if content1 == content2:
                print(f'El contingut del {Colors.GREEN}fitxer és idèntic{Colors.RESET} en ambdós directoris.')
            else:
                print(f'El contingut del {Colors.YELLOW}fitxer és diferent{Colors.RESET} en ambdós directoris.')
    else:
        print(f"\n{Colors.YELLOW}Error: Fitxer {nom_fitxer} no trobat en un dels directoris.{Colors.RESET}")

def penja_a_virustotal(nom_fitxer):
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': VIRUSTOTAL_API_KEY}

    with open(nom_fitxer, 'rb') as file:
        files = {'file': (nom_fitxer, file)}
        response = requests.post(url, files=files, params=params)

    result = response.json()
    print(f"\nResultats de VirusTotal:")
    print(f"SHA-256: {result.get('sha256')}")
    print(f"Permalink: {result.get('permalink')}")
    print("Resultat de l'anàlisi:", result.get('verbose_msg'))

def canviar_directoris():
    global directori1, directori2
    nou_directori1 = input(f"{Colors.RED}Introdueix el nou camí del directori 1: {Colors.RESET}")
    nou_directori2 = input(f"{Colors.RED}Introdueix el nou camí del directori 2: {Colors.RESET}")

    if not os.path.exists(nou_directori1):
        print(f"\n{Colors.YELLOW}Error: El directori {nou_directori1} no existeix.{Colors.RESET}")
    else:
        directori1 = nou_directori1

    if not os.path.exists(nou_directori2):
        print(f"\n{Colors.YELLOW}Error: El directori {nou_directori2} no existeix.{Colors.RESET}")
    else:
        directori2 = nou_directori2

    print(f"\n{Colors.GREEN}Directoris canviats amb èxit.{Colors.RESET}")

def main():
    cargar_configuracion()
    imprimir_banner()
    log_moviment("S'ha iniciat l'aplicació.")

    directori1 = input(f"{Colors.RED}Introdueix el camí del directori 1: {Colors.RESET}")
    directori2 = input(f"{Colors.RED}Introdueix el camí del directori 2: {Colors.RESET}")

    if not os.path.exists(directori1):
        print(f"\n{Colors.YELLOW}Error: El directori {directori1} no existeix.{Colors.RESET}")
        log_moviment(f"S'ha intentat accedir a un directori inexistent: {directori1}")

    if not os.path.exists(directori2):
        print(f"\n{Colors.YELLOW}Error: El directori {directori2} no existeix.{Colors.RESET}")
        log_moviment(f"S'ha intentat accedir a un directori inexistent: {directori2}")

    while True:
        mostra_menu()

        opcio = input(f"\nSelecciona una opció ({Colors.RED}1-8{Colors.RESET}): ")

        if opcio == "1":
            llista_fitxers_directori(directori1)
            log_moviment(f"S'ha mostrat la llista de fitxers del directori: {directori1}")
        elif opcio == "2":
            llista_fitxers_directori(directori2)
            log_moviment(f"S'ha mostrat la llista de fitxers del directori: {directori2}")
        elif opcio == "3":
            compara_fitxers(directori1, directori2)
            log_moviment("S'ha comparat la llista de fitxers en ambdós directoris.")
        elif opcio == "4":
            nom_fitxer = input(f"{Colors.RED}Introdueix el nom del fitxer a comparar: {Colors.RESET}")
            compara_fitxer(directori1, directori2, nom_fitxer)
            log_moviment(f"S'ha comparat el fitxer: {nom_fitxer}")
        elif opcio == "5":
            nom_fitxer = input(f"{Colors.RED}Introdueix el nom del fitxer a penjar a VirusTotal: {Colors.RESET}")
            penja_a_virustotal(nom_fitxer)
            log_moviment(f"S'ha penjat el fitxer a VirusTotal: {nom_fitxer}")
        elif opcio == "6":
            canviar_directoris()
            log_moviment("S'han canviat els directoris.")
        elif opcio == "7":
            mostrar_configuracion()
            configurar_programa()
        elif opcio == "8":
            print("Sortint de l'aplicació. Bye :)")
            log_moviment("S'ha tancat l'aplicació.")
            break
        else:
            print(f"Opció no vàlida. Si us plau, selecciona una opció correcta.")
            log_moviment(f"S'ha introduït una opció no vàlida: {opcio}")

if __name__ == "__main__":
    esborraPantalla()
    main()