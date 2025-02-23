import rpyc
import argparse
import asyncio
from concurrent.futures import ThreadPoolExecutor
from rpyc.utils.classic import obtain

# Funktion um in das File "reduced.txt" zu schreiben
def write(solution):
    with open("reduced.txt", 'w') as file:
        file.write(f"{solution}")

# Stellt eine Verbindung zu einem Server her
def connect_to_server(port):
    print(f"Connecting to server at localhost:{port}...")
    conn = rpyc.connect("localhost", port)
    print(f"Connection to server at localhost:{port} done")
    return conn

async def main():
    # Erstellen der Argumentparser
    parser = argparse.ArgumentParser(description='Starte den RPyC-Server.')
    parser.add_argument('--file')
    parser.add_argument("--ports", type=int, nargs="+")
    args = parser.parse_args()

    file = args.file

    # Öffnen des Files
    try:
        with open(file, 'r', encoding='utf-8') as datei:
            inhalt = datei.read()
    except FileNotFoundError:
        print(f"Die Datei '{file}' wurde nicht gefunden.")
        return
    except Exception as e:
        print(f"Es ist ein Fehler aufgetreten: {e}")
        return

    # Einteilen des Inhalts in Zeilen
    inhaltzeilen = inhalt.split('\n')
    # Entfernene der Leerzeilen
    inhaltszeilen = [line for line in inhaltzeilen if line and not line.isspace()]
    # Aufteilen der Zeilen in Gruppen (teilgrößen)
    teilgroesse = int(len(inhaltszeilen) / len(args.ports))
    rest = len(inhaltszeilen) % len(args.ports)
    ergebnis = []
    start = 0
    for i in range(len(args.ports)):
        ende = start + teilgroesse + (1 if i < rest else 0)
        ergebnis.append(inhaltszeilen[start:ende])
        start = ende

    # ThreadPoolExecutor erstellen, um blockierende Operationen in Threads auszulagern
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()

        # Verbindungen zu den Servern herstellen
        connections = await loop.run_in_executor(
            executor, 
            lambda: [connect_to_server(port) for port in args.ports]
        )

        # Aufruf der Services auf den Servern
        answers = await loop.run_in_executor(
            executor, 
            lambda: [(connections[i].root.count_words(ergebnis[i])) for i in range(len(connections))]
        )

        # Zusammenführen der Ergebnisse
        final_dict = {}
        for local_dict in answers:
            local_dict = obtain(local_dict)
            for key, value in local_dict.items():
                if key in final_dict:
                    final_dict[key] += value
                else:
                    final_dict[key] = value

        # Schließen der Serververbindungen
        for conn in connections:
            conn.close()

        # Schreiben des finalen Ergebnisses in die Datei
        write(final_dict)

if __name__ == "__main__":
    asyncio.run(main())
