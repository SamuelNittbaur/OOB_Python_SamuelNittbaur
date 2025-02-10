from flask import Flask, render_template
import pandas as pd
import plotly.express as px


# Das Interface stimmt nicht mit dem Mockup überein

app = Flask(__name__)

data = {
    "Semester": ["1. Semester", "2. Semester", "3. Semester", "4. Semester"],
    "Noten": [[2.3, 2.7, 2.0, 2.5], [2.5, 2.8, 2.4, 2.3], [2.2, 2.1, 2.4, 2.0], [2.1, 2.3, 2.0, 2.2]]
}

# Berechnungen
def calculate_credits(data):
    credits_per_course = 5
    total_courses = sum(len(semester) for semester in data["Noten"])
    completed_courses = sum(len(semester) for semester in data["Noten"])
    total_credits = total_courses * credits_per_course
    earned_credits = completed_courses * credits_per_course
    progress_percentage = (earned_credits / total_credits) * 100
    
    return earned_credits, total_credits, progress_percentage

def calculate_gpa(data):
    all_grades = [grade for semester in data["Noten"] for grade in semester]
    return round(sum(all_grades) / len(all_grades), 2)

# Berechnete Werte
earned_credits, total_credits, progress_percentage = calculate_credits(data)
average_gpa = calculate_gpa(data)

@app.route("/")
def dashboard():
    df = pd.DataFrame({
        "Semester": data["Semester"],
        "Durchschnittsnote": [round(sum(semester) / len(semester), 2) for semester in data["Noten"]]
    })

    # Fortschrittsdiagramm
    fig_credits = px.bar(df, x="Semester", y="Durchschnittsnote", title="Notenentwicklung")
    
    return f"""
    <html>
        <head>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <h1>Studienfortschritt Dashboard</h1>
            <h2>Übersicht der Semester</h2>
            {df.to_html()}
            <h2>Fortschritt</h2>
            <p>Erworbene Credits: {earned_credits} / {total_credits} ({progress_percentage:.2f}%)</p>
            <p>Gesamter Notendurchschnitt: {average_gpa}</p>
            <h2>Notenentwicklung</h2>
            <div>{fig_credits.to_html(full_html=False)}</div>
        </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
