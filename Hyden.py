import requests
import os
import time
from bs4 import BeautifulSoup

# Colores para resaltar mensajes
GREEN = "\033[92m"
RED = "\033[91m"
ORANGE = "\033[93m"
RESET = "\033[0m"
BLUE = "\033[94m"

# Banner animado
def banner():
    os.system("clear")
    banner_text = """
  
██╗  ██╗██╗   ██╗██████╗ ███████╗███╗   ██╗
██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝████╗  ██║
███████║ ╚████╔╝ ██║  ██║█████╗  ██╔██╗ ██║
██╔══██║  ╚██╔╝  ██║  ██║██╔══╝  ██║╚██╗██║
██║  ██║   ██║   ██████╔╝███████╗██║ ╚████║
╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═══╝
                                           

           443 HTTP por Rovanof - GitHub

 《 ¡echo con fines educativos no me hago responsable del mal uso! 》
"""
    for line in banner_text.splitlines():
        print(f"{ORANGE}{line}{RESET}")
        time.sleep(0.1)

# Verificar conexión
def check_connection(site):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(site, headers=headers, timeout=5)
        latency = response.elapsed.total_seconds()
        if response.status_code == 200:
            print(f"{GREEN}[✓] Conexión estable. Latencia: {latency:.2f}s{RESET}")
            return True
        else:
            print(f"{RED}[✗] Error en la conexión. Código: {response.status_code}{RESET}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"{RED}[✗] Error: {e}{RESET}")
        return False

# Listar contenido
def list_directories(base_url, current_path):
    url = f"{base_url}{current_path}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            print(f"{GREEN}[✓] Contenido de {url}:{RESET}")
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a"):
                href = link.get("href")
                if href:
                    print(f" - {href}")
        else:
            print(f"{ORANGE}[!] No se puede listar el contenido en {url} (código {response.status_code}){RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{RED}[✗] Error: {e}{RESET}")

# Crear carpeta
def create_directory(base_url, current_path):
    dir_name = input("Nombre de la carpeta a crear: ").strip()
    url = f"{base_url}{current_path}/{dir_name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.put(url, headers=headers)
        if response.status_code in [200, 201]:
            print(f"{GREEN}[✓] Carpeta creada: {url}{RESET}")
        else:
            print(f"{RED}[✗] Error al crear carpeta. Código: {response.status_code}{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{RED}[✗] Error: {e}{RESET}")

# Eliminar carpeta
def remove_directory(base_url, current_path):
    dir_name = input("Nombre de la carpeta a eliminar: ").strip()
    url = f"{base_url}{current_path}/{dir_name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.delete(url, headers=headers)
        if response.status_code in [200, 204]:
            print(f"{GREEN}[✓] Carpeta eliminada: {url}{RESET}")
        else:
            print(f"{RED}[✗] Error al eliminar carpeta. Código: {response.status_code}{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{RED}[✗] Error: {e}{RESET}")

# Descargar archivo
def download_file(base_url, current_path):
    file_name = input("Nombre del archivo a descargar: ").strip()
    url = f"{base_url}{current_path}/{file_name}"
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_name, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"{GREEN}[✓] Archivo descargado: {file_name}{RESET}")
        else:
            print(f"{RED}[✗] Error al descargar archivo. Código: {response.status_code}{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{RED}[✗] Error: {e}{RESET}")

# Crear archivo editable
def create_file():
    file_name = input("Nombre del archivo a crear: ").strip()
    os.system(f"nano {file_name}")

# Menú principal
def main():
    banner()
    target_site = input("Ingresa el sitio web (sin 'https://'): ").strip()
    if not target_site.startswith("https://"):
        target_site = f"https://{target_site}"
    current_path = "/"
    if not check_connection(target_site):
        print(f"{RED}[✗] No se pudo conectar al sitio. Saliendo...{RESET}")
        return

    while True:
        print("\nComandos disponibles:")
        print(f"  - {GREEN}LS{RESET}: Listar contenido del directorio actual.")
        print(f"  - {GREEN}CD [carpeta]{RESET}: Cambiar al directorio especificado.")
        print(f"  - {GREEN}MKDIR{RESET}: Crear una nueva carpeta.")
        print(f"  - {GREEN}RMDIR{RESET}: Eliminar una carpeta.")
        print(f"  - {GREEN}FILEDOWN{RESET}: Descargar un archivo.")
        print(f"  - {GREEN}FILEMAKER{RESET}: Crear un archivo editable.")
        print(f"  - {RED}SD{RESET}: Salir del programa.")

        command = input("> ").strip().upper()
        if command == "LS":
            list_directories(target_site, current_path)
        elif command.startswith("CD "):
            folder = command[3:].strip()
            if folder == "..":
                current_path = "/".join(current_path.rstrip("/").split("/")[:-1]) or "/"
            else:
                current_path += folder if folder.endswith("/") else f"/{folder}/"
            print(f"{GREEN}[✓] Directorio actual: {current_path}{RESET}")
        elif command == "MKDIR":
            create_directory(target_site, current_path)
        elif command == "RMDIR":
            remove_directory(target_site, current_path)
        elif command == "FILEDOWN":
            download_file(target_site, current_path)
        elif command == "FILEMAKER":
            create_file()
        elif command == "SD":
            print(f"{RED}[✗] Finalizando conexión...{RESET}")
            break
        else:
            print(f"{ORANGE}[!] Comando no reconocido: {command}{RESET}")

if __name__ == "__main__":
    main()
