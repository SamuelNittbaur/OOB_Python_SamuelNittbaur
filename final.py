from flask import Flask, render_template
import pandas as pd
from DatenManager import Datenmanager
from Objects import Studiengang, Semester, Modul, Klausur, Portfolio, Projektbericht

app = Flask(__name__)

datenmanager = Datenmanager("studiengang.json")
studiengang = datenmanager.laden()

if not studiengang:
    studiengang = Studiengang("B.Sc. Software Entwicklung", 180)

@app.route('/')
def dashboard():
    earned_ects = studiengang.get_earned_ects()
    total_ects = studiengang.benoetigte_ects
    progress_percentage = (earned_ects / total_ects) * 100
    average_gpa = studiengang.get_average_grade()
    output_text = "Du bist auf dem richtigen Weg dein Ziel von 2,5 zu erreichen"
    output_text_color = "green"
    if average_gpa >= 2.5:
        output_text = "Du bist nicht auf dem Weg, dein Notenziel zu erreichen"
        output_text_color = "red"
    print("Semester-Daten:")
    for semester in studiengang.semester:
        print(f"📌 {semester.name}")
        for modul in semester.module:
            print(f"  ➜ Modul: {modul.name}, Note: {modul.get_grades()}, ECTS: {modul.get_earned_ects()}")

    return render_template("dashboard.html", 
                           progress_percentage=progress_percentage, 
                           earned_ects=earned_ects, 
                           total_ects=total_ects, 
                           average_gpa=average_gpa,
                           output_text = output_text,
                           output_text_color = output_text_color,
                           studiengang=studiengang)

if __name__ == "__main__":
    app.run(debug=True)
