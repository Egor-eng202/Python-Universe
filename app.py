from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "pu-2026-super-secret-key-xyz"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "register"

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")
TOTAL_LESSONS = 25


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS progress (
            user_id INTEGER NOT NULL,
            lesson TEXT NOT NULL,
            PRIMARY KEY (user_id, lesson),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()


init_db()


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return User(row["id"], row["username"]) if row else None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/lessons")
def lessons():
    return render_template("lessons.html", total=TOTAL_LESSONS)


@app.route("/report")
def report():
    return render_template("report.html")


@app.route("/lesson<int:n>")
def lesson(n):
    if n < 1 or n > TOTAL_LESSONS:
        return redirect(url_for("lessons"))
    return render_template(f"lesson{n}.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""
        if not username or not password:
            return jsonify(ok=False, msg="Заполните все поля"), 400
        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            conn.commit()
            row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            login_user(User(row["id"], row["username"]))
            return jsonify(ok=True, msg="Регистрация успешна")
        except sqlite3.IntegrityError:
            return jsonify(ok=False, msg="Пользователь уже существует"), 409
        finally:
            conn.close()
    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if not row or not check_password_hash(row["password_hash"], password):
        return jsonify(ok=False, msg="Неверный логин или пароль"), 401
    login_user(User(row["id"], row["username"]))
    return jsonify(ok=True, msg="Вход выполнен")


@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify(ok=True, msg="Вы вышли")


@app.route("/api/me")
def me():
    if current_user.is_authenticated:
        return jsonify(logged_in=True, username=current_user.username)
    return jsonify(logged_in=False)

@app.route("/api/progress", methods=["GET"])
@login_required
def get_progress():
    conn = get_db()
    rows = conn.execute("SELECT lesson FROM progress WHERE user_id = ?", (current_user.id,)).fetchall()
    conn.close()
    return jsonify([r["lesson"] for r in rows])


@app.route("/api/progress", methods=["POST"])
@login_required
def mark_progress():
    data = request.get_json()
    lesson = data.get("lesson")
    if not lesson:
        return jsonify(ok=False, msg="Не указан урок"), 400
    conn = get_db()
    conn.execute("INSERT OR IGNORE INTO progress (user_id, lesson) VALUES (?, ?)", (current_user.id, lesson))
    conn.commit()
    conn.close()
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(debug=True)
