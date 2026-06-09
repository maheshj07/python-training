from flask import Flask, render_template

app = Flask(__name__)

students = [
    {
        "name": "Rahul Sharma",
        "roll": 101,
        "attendance": "92%",
        "marks": 85
    },
    {
        "name": "Priya Patil",
        "roll": 102,
        "attendance": "95%",
        "marks": 90
    },
    {
        "name": "Amit Verma",
        "roll": 103,
        "attendance": "88%",
        "marks": 78
    },
    {
        "name": "Sneha Joshi",
        "roll": 104,
        "attendance": "97%",
        "marks": 94
    },
    {
        "name": "Rohan Gupta",
        "roll": 105,
        "attendance": "90%",
        "marks": 82
    }
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/records")
def records():
    return render_template("records.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)