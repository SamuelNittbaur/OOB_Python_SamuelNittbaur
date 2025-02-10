import json
from Objects import Studiengang, Semester, Modul, Klausur, Portfolio, Projektbericht

class Datenmanager:
    def __init__(self, dateipfad: str):
        self.dateipfad = dateipfad

    def speichern(self, studiengang):
        try:
            with open(self.dateipfad, "w", encoding="utf-8") as file:
                json.dump(studiengang.__dict__, file, indent=4, default=lambda o: o.__dict__)
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")

    def laden(self):
        try:
            with open(self.dateipfad, "r", encoding="utf-8") as file:
                data = json.load(file)
                if data:
                    studiengang = Studiengang(data["name"], data["benoetigte_ects"])
                    for semester_data in data.get("semester", []):
                        semester = Semester(semester_data["name"])
                        for modul_data in semester_data.get("module", []):
                            modul = Modul(modul_data["name"])
                            modul.add_pruefungsleistung(Klausur(modul_data["note"], modul_data["ects"], 1))
                            semester.add_modul(modul)
                        studiengang.add_semester(semester)
                    return studiengang
        except FileNotFoundError:
            print("⚠️ Datei nicht gefunden: Stelle sicher, dass `studiengang.json` existiert!")
        except json.JSONDecodeError:
            print("⚠️ Fehler beim Laden der JSON-Datei. Ist das JSON-Format korrekt?")
        return None