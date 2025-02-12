from flask import Flask, render_template  # Importiert Flask und die Funktion zum Rendern von HTML-Templates
import pandas as pd  # Importiert Pandas (wird aber im aktuellen Code nicht genutzt)
from DatenManager import Datenmanager  # Importiert die Klasse zum Laden und Verwalten der Studiengang-Daten
from Objects import Studiengang, Semester, Modul, Klausur, Portfolio, Projektbericht  # Importiert die relevanten Objekte für den Studiengang

app = Flask(__name__)  # Erstellt eine Flask-Anwendung

datenmanager = Datenmanager("studiengang.json")  # Initialisiert den Datenmanager mit einer JSON-Datei
studiengang = datenmanager.laden()  # Lädt die gespeicherten Daten des Studiengangs

# Falls keine Daten geladen wurden, wird ein neuer Studiengang mit 180 ECTS angelegt
if not studiengang:
    studiengang = Studiengang("B.Sc. Software Entwicklung", 180)

@app.route('/')  # Definiert die Route für das Dashboard
def dashboard():
    earned_ects = studiengang.get_earned_ects()  # Berechnet die bisher erworbenen ECTS-Punkte
    total_ects = studiengang.benoetigte_ects  # Gesamte benötigte ECTS-Punkte für den Abschluss
    progress_percentage = (earned_ects / total_ects) * 100  # Berechnet den Fortschritt in Prozent
    average_gpa = studiengang.get_average_grade()  # Berechnet die Durchschnittsnote
    
    # Standardtext zur Motivation basierend auf der Durchschnittsnote
    output_text = "Du bist auf dem richtigen Weg dein Ziel von 2,5 zu erreichen"
    output_text_color = "green"
    if average_gpa >= 2.5:  # Falls die Note schlechter als 2,5 ist, wird eine Warnung ausgegeben
        output_text = "Du bist nicht auf dem Weg, dein Notenziel zu erreichen"
        output_text_color = "red"
    
    # Debug-Ausgabe der Semester- und Moduldaten
    print("Semester-Daten:")
    for semester in studiengang.semester:
        print(f"📌 {semester.name}")
        for modul in semester.module:
            print(f"  ➜ Modul: {modul.name}, Note: {modul.get_grades()}, ECTS: {modul.get_earned_ects()}")
    
    # Übergibt die berechneten Werte an das HTML-Template
    return render_template("dashboard.html", 
                           progress_percentage=progress_percentage, 
                           earned_ects=earned_ects, 
                           total_ects=total_ects, 
                           average_gpa=average_gpa,
                           output_text=output_text,
                           output_text_color=output_text_color,
                           studiengang=studiengang)

if __name__ == "__main__":  # Startet die Flask-Anwendung im Debug-Modus
    app.run(debug=True)
