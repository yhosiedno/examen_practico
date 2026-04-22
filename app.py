import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("inventario.db")
    conn.row_factory = sqlite3.Row
    return conn

def crear_bd():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

crear_bd()

# LISTAR
@app.route('/')
def listar():
    conn = get_db()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()
    return render_template("index.html", productos=productos)

# REGISTRAR
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        conn = get_db()
        conn.execute(
            "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
            (
                request.form['nombre'],
                request.form['categoria'],
                request.form['precio'],
                request.form['stock']
            )
        )
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template("registrar.html")

# EDITAR
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = get_db()

    if request.method == 'POST':
        conn.execute("""
            UPDATE productos
            SET nombre=?, categoria=?, precio=?, stock=?
            WHERE id=?
        """, (
            request.form['nombre'],
            request.form['categoria'],
            request.form['precio'],
            request.form['stock'],
            id
        ))
        conn.commit()
        conn.close()
        return redirect('/')

    producto = conn.execute("SELECT * FROM productos WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("editar.html", producto=producto)

# ELIMINAR
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = get_db()
    conn.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)