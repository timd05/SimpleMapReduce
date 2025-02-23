import re
import rpyc
import argparse
from rpyc.utils.server import ThreadedServer

@rpyc.service
class WordCountService (rpyc.Service):
    @rpyc.exposed
    def count_words (self , lines):
        wordcount = {}
        cleaned_lines = []
        for line in lines:
            # Leerzeichen und Tabs am Anfang und Ende entfernen
            line = line.strip()
            # Nicht-alphanumerische Zeichen entfernen
            line = re.sub(r'[^a-zA-Z0-9\s]', '', line)
            # In Kleinbuchstaben umwandeln
            line = line.lower()
            cleaned_lines.append(line)
        # Zählen der Wörter
        for line in cleaned_lines:
            words = line.split()
            for word in words:
                wordcount[word] = wordcount.get(word, 0) + 1
        return wordcount

if __name__ == "__main__":
    # Erstelle einen Argumentparser
    parser = argparse.ArgumentParser(description='Starte den RPyC-Server.')
    # Füge das Argument --port hinzu
    parser.add_argument('--port', type=int, required=True, help='Der Port, auf dem der Server laufen soll.')
    # Analysiere das Argument
    args = parser.parse_args()

    # Starte den RPyC-Server auf dem angegebenen Port
    print(f"Starting server on port {args.port}...")
    server = ThreadedServer(WordCountService, port=args.port, protocol_config={"allow_pickle": True, "sync_request_timeout": 900000})
    server.start()