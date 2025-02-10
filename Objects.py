class Studiengang:
    def __init__(self, name, benoetigte_ects):
        self.name = name
        self.benoetigte_ects = benoetigte_ects
        self.semester = []

    def add_semester(self, semester):
        self.semester.append(semester)

    def get_earned_ects(self):
        return sum(semester.get_earned_ects() for semester in self.semester)

    def get_average_grade(self):
        grades = [grade for semester in self.semester for grade in semester.get_grades() if isinstance(grade, (int, float))]
        return round(sum(grades) / len(grades), 2) if grades else 0



class Semester:
    def __init__(self, name):
        self.name = name
        self.module = []

    def add_modul(self, modul):
        self.module.append(modul)

    def get_earned_ects(self):
        return sum(modul.get_earned_ects() for modul in self.module)

    def get_grades(self):
        return [grade for modul in self.module for grade in modul.get_grades()]


class Modul:
    def __init__(self, name, abhaengig_von=None):
        self.name = name
        self.abhaengig_von = abhaengig_von
        self.pruefungsleistungen = []

    def add_pruefungsleistung(self, pruefungsleistung):
        self.pruefungsleistungen.append(pruefungsleistung)

    def get_earned_ects(self):
        return sum(pl.ects for pl in self.pruefungsleistungen if pl.note != 0)

    def get_grades(self):
        return [pl.note for pl in self.pruefungsleistungen if pl.note is not None and pl.note != 0]


class Pruefungsleistung:
    def __init__(self, note: float, ects: int):
        self._note = note  # „protected“ Attribut
        self.ects = ects
    @property
    def note(self):
        return self._note
    
    @note.setter
    def note(self, value):
        if 1.0 <= value <= 5.0:  # Notenbereich validieren
            self._note = value
        else:
            raise ValueError("Ungültige Note")


class Klausur(Pruefungsleistung):
    def __init__(self, note: float, ects: int, dauer: int):
        super().__init__(note, ects)
        self.dauer = dauer


class Portfolio(Pruefungsleistung):
    pass


class Projektbericht(Pruefungsleistung):
    pass


class Fachpraesentation(Pruefungsleistung):
    pass


# Beispielhafte Nutzung:
studiengang = Studiengang("Informatik", 180)

semester1 = Semester("1. Semester")
modul1 = Modul("Mathematik")
modul2 = Modul("Programmierung")

modul1.add_pruefungsleistung(Klausur(2.3, 5, 1))
modul1.add_pruefungsleistung(Projektbericht(2.0, 5))
modul2.add_pruefungsleistung(Portfolio(1.7, 5))

semester1.add_modul(modul1)
semester1.add_modul(modul2)

studiengang.add_semester(semester1)