from flask import Flask, render_template, request, jsonify, redirect, url_for
import pyodbc

app = Flask(__name__)


def get_db():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-N6SHLQ1;'
        'DATABASE=ArenaMatch;'
        'Trusted_Connection=yes;'
    )
    return conn



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/usuarios')
def usuarios():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Usuario')
    datos = cursor.fetchall()
    conn.close()
    return render_template('usuarios.html', usuarios=datos)

@app.route('/usuarios/crear', methods=['POST'])
def crear_usuario():
    data = request.form
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Usuario (Nombre, Email, Password_Hash, Rol) VALUES (?, ?, ?, ?)',
        data['nombre'], data['email'], data['password'], data['rol']
    )
    conn.commit()
    conn.close()
    return redirect(url_for('usuarios'))

@app.route('/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Usuario WHERE ID_Usuario = ?', id)
    conn.commit()
    conn.close()
    return redirect(url_for('usuarios'))



@app.route('/equipos')
def equipos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Equipo')
    datos = cursor.fetchall()
    conn.close()
    return render_template('equipos.html', equipos=datos)

@app.route('/equipos/crear', methods=['POST'])
def crear_equipo():
    data = request.form
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Equipo (Nombre, Logo_URL) VALUES (?, ?)',
        data['nombre'], data['logo']
    )
    conn.commit()
    conn.close()
    return redirect(url_for('equipos'))

@app.route('/equipos/eliminar/<int:id>')
def eliminar_equipo(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Equipo WHERE ID_Equipo = ?', id)
    conn.commit()
    conn.close()
    return redirect(url_for('equipos'))



@app.route('/torneos')
def torneos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Torneo')
    datos = cursor.fetchall()
    conn.close()
    return render_template('torneos.html', torneos=datos)

@app.route('/torneos/crear', methods=['POST'])
def crear_torneo():
    data = request.form
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Torneo (Nombre, Videojuego, Fecha_Inicio, Fecha_Fin, Prize_Pool, Costo_Inscripcion, Estado) VALUES (?, ?, ?, ?, ?, ?, ?)',
        data['nombre'], data['videojuego'], data['fecha_inicio'], data['fecha_fin'], data['prize_pool'], data['costo'], data['estado']
    )
    conn.commit()
    conn.close()
    return redirect(url_for('torneos'))

@app.route('/torneos/eliminar/<int:id>')
def eliminar_torneo(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Torneo WHERE ID_Torneo = ?', id)
    conn.commit()
    conn.close()
    return redirect(url_for('torneos'))



@app.route('/inscripciones')
def inscripciones():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT i.ID_Inscripcion, t.Nombre, e.Nombre, i.Fecha_Inscripcion, i.Monto_Pagado, i.Estado
        FROM Inscripcion i
        JOIN Torneo t ON i.ID_Torneo = t.ID_Torneo
        JOIN Equipo e ON i.ID_Equipo = e.ID_Equipo
    ''')
    datos = cursor.fetchall()
    cursor.execute('SELECT ID_Torneo, Nombre FROM Torneo')
    torneos = cursor.fetchall()
    cursor.execute('SELECT ID_Equipo, Nombre FROM Equipo')
    equipos = cursor.fetchall()
    conn.close()
    return render_template('inscripciones.html', inscripciones=datos, torneos=torneos, equipos=equipos)

@app.route('/inscripciones/crear', methods=['POST'])
def crear_inscripcion():
    data = request.form
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Inscripcion (ID_Torneo, ID_Equipo, Monto_Pagado, Estado) VALUES (?, ?, ?, ?)',
        data['torneo'], data['equipo'], data['monto'], data['estado']
    )
    conn.commit()
    conn.close()
    return redirect(url_for('inscripciones'))

if __name__ == '__main__':
    app.run(debug=True)