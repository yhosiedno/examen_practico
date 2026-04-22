import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def crear_bd():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            categoria TEXT,
            precio REAL,
            stock INTEGER
        )
    """)

    conn.commit()
    conn.close()

crear_bd()

@app.route('/')
def index():
    conn = sqlite3.connect("inventario.db")
    conn.row_factory = sqlite3.Row

    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()

    return render_template("index.html", productos=productos)

if __name__ == '__main__':
    app.run(debug=True)