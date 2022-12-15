from flask import Flask, render_template, app
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("///UI/templates/home.html")


# if __name__ == "__main__":
#     app.run(debug=True)