#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

from flask import Flask, redirect, render_template, request, session, g
import sqlite3
import time
import hashlib
import random
import os
import subprocess

app = Flask(__name__)
os.environ['WERKZEUG_DEBUG_PIN'] = '160-820-010'
app.secret_key = "U2VjdXJlVG9t"  # Clé pour gérer les sessions Flask
DATABASE = "database.db"
app.debug = True
app.lastSTC = "STC{d3bugg3RGoCr4zy2niGHT}"


# Gestion des blocages (ex: après 3 tentatives échouées)
blocked_users = {}
# Variable pour vérifier si une fonction est appelée
function_called = False

def set_function_called(value):
    global function_called
    function_called = value

def is_function_called():
    return function_called

# Gestion des privilèges des utilisateurs
def check_admin():
    if "user_id" in session:
        db = get_db()
        cursor = db.execute("SELECT is_admin FROM users WHERE id = ?", (session["user_id"],))
        user = cursor.fetchone()
        if user and user["is_admin"]:
            return True
    return False

def check_god():
    if "user_id" in session:
        db = get_db()
        cursor = db.execute("SELECT is_god FROM users WHERE id = ?", (session["user_id"],))
        user = cursor.fetchone()
        if user and user["is_god"]:
            return True
    return False

@app.route("/final", methods=["GET"])
def final():
    """Page finale"""
    if check_admin():
        return render_template("final.html") #Debugger code pin : 160-820-010
    else:
        return render_template("erreur.html", message="Vous n'êtes pas autorisé à accéder à cette page.")

@app.route("/notes", methods=["GET"])
def notes():
    """Page de notes"""
    if "user_id" in session:
        return render_template("notes.html")
    else:
        return render_template("erreur.html", message="Vous n'êtes pas autorisé à accéder à cette page.")

@app.route("/admin", methods=["GET"])
def admin():
    """Page d'administration"""
    if check_admin():
        return render_template("admin.html")
    else:
        return render_template("erreur.html", message="Vous n'êtes pas autorisé à accéder à cette page.")

@app.route("/home", methods=["GET"])
def home():
    """Page d'accueil"""
    if "user_id" in session:
        role = "Administrateur" if session["is_admin"] else "Utilisateur"
        return render_template("home.html", username=session["username"], role=role)
    else:
        return render_template("erreur.html", message="Vous n'êtes pas autorisé à accéder à cette page.")

@app.route("/config", methods=["GET"])
def config():
    """Page de configuration"""
    if "user_id" in session:
        return render_template("config.html")
    else:
        return render_template("erreur.html", message="Vous n'êtes pas autorisé à accéder à cette page.")

@app.route("/config", methods=["POST"])
def save_config():
    """Sauvegarde de la configuration"""
    if "user_id" in session:
        random_sleep = random.uniform(1, 10)
        time.sleep(random_sleep)
        db = get_db()
        role_id = int(request.form["role"])
        if not isinstance(role_id, int) or role_id < 0 or role_id > 10000:
            return render_template("erreur.html", message="Utiliser un nombre entre 0 et 10 000 pour définir le rôle")
        if role_id == 2001:
            db.execute("UPDATE users SET is_admin = 1 WHERE id = ?", (session["user_id"],))
            message = "Configuration sauvegardée. Vous êtes désormais Administrateur."
            session["is_admin"] = True
        else:
            db.execute("UPDATE users SET is_admin = 0 WHERE id = ?", (session["user_id"],))
            message = "Configuration sauvegardée. Vous êtes désormais Utilisateur."
            session["is_admin"] = False

        db.commit()
        return render_template("config.html", message=message)
    else:
        return redirect("/home")

@app.route("/robots.txt", methods=["GET"])
def robots():
    """Page robots.txt"""
    return "Beep boop ! 🤖"

@app.route("/dev", methods=["GET"])
def dev():
    """Page de développement"""
    return render_template("dev.html")

@app.errorhandler(404)
def page_not_found(e):
    """Page d'erreur 404"""
    return render_template("erreur.html", message="Cette page n'existe pas.")

def get_db():
    """Connexion à la base SQLite"""
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Fermeture de la connexion"""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/", methods=["GET", "POST"])
def login():
    """Page de connexion"""
    error = None
    db = get_db()

    if "user_id" in session:
        return redirect("/home")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Vérifier si l'utilisateur est bloqué
        if username in blocked_users:
            last_attempt_time = blocked_users[username]
            time_since_last_attempt = time.time() - last_attempt_time
            if time_since_last_attempt < 180:
                remaining_time = 180 - time_since_last_attempt
                error = f"⏳ Tu vas vite en besogne ! Attends {int(remaining_time)} secondes avant de réessayer."
                return render_template("login.html", error=error)

        # Vérifier les caractères interdits
        forbidden_characters = ["'", "|", "\"", ";", "--"]
        if any(char in username for char in forbidden_characters) or any(char in password for char in forbidden_characters):
            error = "😡 STOP ! Pas de triche."
            return render_template("login.html", error=error)

        # Vérifier si l'utilisateur existe
        cursor = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["is_admin"] = user["is_admin"]
            session["is_god"] = user["is_god"]
            return redirect("/home")
        else:
            error = "❌ Identifiants incorrects."
            # Bloquer l'utilisateur après 3 tentatives échouées
            if username in blocked_users:
                blocked_users[username] = time.time()
            else:
                blocked_users[username] = time.time()

    return render_template("login.html", error=error)


@app.route("/logout", methods=["GET"])
def logout():
    """Déconnexion"""
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("is_admin", None)
    session.clear()
    return redirect("/")

@app.route("/reset", methods=["GET", "POST"])
def reset():
    """Page de réinitialisation vulnérable"""
    message = None
    password_comment = ""

    if request.method == "POST":
        time.sleep(3)
        username = request.form["username"]
        db = get_db()

        start_time = time.time()
        cursor = db.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        end_time = time.time()

        if user:
            password_md5 = hashlib.md5(user['password'].encode()).hexdigest()
            password_comment = f"<!-- Password (MD5): {password_md5} -->"
            message = "✔ Si ce compte existe, un email a été envoyé."
        else:
            password_comment = "<!-- Password (MD5): Not available, please try later. -->"
            message = "✔ Si ce compte existe, un email a été envoyé."

        # Différence de temps perceptible
        time.sleep(0.1 if user else 0.9)

    return render_template("reset.html", message=message, password_comment=password_comment)


def init_db():
    """Initialisation de la base SQLite"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, is_admin INTEGER DEFAULT 0, is_god INTEGER DEFAULT 0)")

        def get_random_line(filename):
            with open(filename, 'r') as file:
                lines = file.readlines()
                return random.choice(lines).strip()

        username = get_random_line('Username')
        password = get_random_line('Password')

        cursor.execute("INSERT OR IGNORE INTO users (username, password, is_admin, is_god) VALUES (?, ?, 0, 0)", (username, password))
        conn.commit()


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
