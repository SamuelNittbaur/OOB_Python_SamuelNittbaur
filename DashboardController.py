from flask import Flask, render_template

class DashboardController:
    def __init__(self):
        self.app = Flask(__name__)

    def start(self):
        self.app.run(debug=True)