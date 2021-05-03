from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#Inicializacion de la app
app = Flask(__name__)

#settings
app.secret_key = 'miclavesecreta'


#Conexion a bbdd
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)


#Rutas
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos')
    data = cur.fetchall()
    return render_template('index.html', contactos = data)


@app.route('/agregar', methods=['POST'])    
def AgregarContactos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contactos (nombre, telefono, email) VALUES (%s, %s, %s)', (nombre, telefono, email))
        mysql.connection.commit()
        flash('Contacto agregado!')
        return redirect(url_for('Index'))

@app.route('/editar/<id>')
def obtenerContacto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('editar_contacto.html', contacto = data[0]) 


@app.route('/actualiza/<id>', methods=['POST'])
def actualizaContacto(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contactos
            SET nombre = %s,
                email = %s,
                telefono = %s
            WHERE id = %s
        """, (nombre, email, telefono, id))    
        mysql.connection.commit()
        flash('El contacto se ha actualizado exitosamente!')
        return redirect(url_for('Index'))



@app.route('/eliminar/<string:id>')
def EliminarContacto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    flash('Contacto Removido Exitosamente!')
    mysql.connection.commit()

    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port = 3000, debug=True)