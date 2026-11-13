from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_cors import CORS
import user_management as dbHandler

# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)
# Enable CORS to allow cross-origin requests (needed for CSRF demo in Codespaces)
CORS(app)


def password_meets_rules(password: str) -> bool:
    score = 0
    feedback = []

    if len(password) < 8:
        feedback.append("   Password should be 8 characters.")
    else:
        score += 1

    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("   Password should have lowercase.")

    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("   Password should have uppercase.")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("   Password should have number.")

    special_characters = "!@#$%^&*()-_=+[]{}|;:,.<>/?`~"
    if any(c in special_characters for c in password):
        score += 1
    else:
        feedback.append("   Password should have special character.")

    return feedback, score


@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form["feedback"]
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else:
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")


@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        feedback, score = password_meets_rules(password)

        if score != 5:
            return render_template("/signup.html", feedback=feedback, score=score)

        DoB = request.form["dob"]
        dbHandler.insertUser(username, password, DoB)
        return render_template("/index.html")

    return render_template("/signup.html")


@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@app.route("/", methods=["POST", "GET"])
def home():
    # Simple Dynamic menu
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    # Pass message to front end
    elif request.method == "GET":
        msg = request.args.get("msg", "")
        return render_template("/index.html", msg=msg)
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")


@app.route("/index.html1", methods=["GET"])
def profile():
    return render_template("/index1.html")


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5000)
