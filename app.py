from flask import Flask, render_template
import pymysql

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/db")
def database_test():
    try:
        connection = pymysql.connect(
            host="db",
            user="valarie",
            password="valarie-password",
            database="valarie_db",
            port=3306
        )

        connection.close()

        return "Database connection: SUCCESS"

    except Exception as e:
        return f"Database connection: FAILED - {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
