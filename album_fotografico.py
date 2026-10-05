import csv

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    # TODO
    album = []
    try:
        with open(file_path, "r", encoding = "utf-8", newline='') as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for foto in reader:
                foto["mese"] = int(foto["mese"])
                foto["anno"] = int(foto["anno"])

                foto_anno = None    # non ho ancora trovato lista di foto di quell'anno
                # ora cerco lista di foto in quell'anno
                for gruppo in album:
                    if gruppo[0] == foto["anno"]:
                        foto_anno = gruppo[1]
                        break
                # se l'anno non esiste creo il gruppo
                if foto_anno is None:
                    foto_anno = []
                    album.append([foto["anno"], foto_anno])
                foto_anno.append(foto)

    except FileNotFoundError:
        return None
    return album


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # TODO
    # controllo se esiste già una foto con quel codice: in caso interrompo
    if cerca_foto(album, codice) is not None:
        return None
    if mese < 1 or mese > 12:
        return None

    foto = {"codice": codice, "titolo": titolo, "autore": autore, "mese": mese, "anno": anno}

    try:
        with open(file_path, "r", encoding="utf-8"):
            with open(file_path, "a", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([codice, titolo, autore, mese, anno])
    except OSError:
        return None

    # ora faccio stesso passaggio che avevo fatto nella prima funzione
    foto_anno = None
    for gruppo in album:
        if gruppo[0] == anno:
            foto_anno = gruppo[1]
            break
    if foto_anno is None:
        foto_anno = []
        album.append([anno, foto_anno])
    foto_anno.append(foto)
    return foto



def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # TODO
    # scorro sugli elementi gruppo
    for gruppo in album:
        # scorro sui dizionari foto
        for foto in gruppo[1]:
            if foto["codice"] == codice:
                # restituisco come stringa di valori
                return (f"{foto['codice']}, {foto['titolo']}, {foto['autore']}, {foto['mese']}, {foto['anno']}")
    # se non trovo
    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO
    for gruppo in album:
        if gruppo[0] == anno:
            # creo una lista dei titoli delle foto di quell'anno e la ordino
            titoli = []
            for foto in gruppo[1]:
                titoli.append(foto["titolo"])
            titoli.sort()
            return titoli
    return None


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
