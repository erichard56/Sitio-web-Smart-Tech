from flask import Flask     # pip install flask
from flask import render_template, request, redirect, jsonify
from flask_cors import CORS
import mysql.connector      # pip instal mysql-connector-python

app = Flask(__name__)
CORS(app)

class cnx:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host = host,
            user = user,
            password = password, 
            database = database
        )
        self.cursor = self.conn.cursor()

    def get_productos(self):
        q1 = 'SELECT * FROM productos ORDER BY id'
        self.cursor.execute(q1)
        productos = self.cursor.fetchall()
        return (productos)

    def get_medios_pago(self):
        q1 = 'SELECT * FROM medios_pago'
        self.cursor.execute(q1)
        mps = self.cursor.fetchall()
        return(mps)

    def get_medio_pago(self, id):
        q1 = f'SELECT * FROM medios_pago WHERE id = {id}'
        self.cursor.execute(q1)
        mps = self.cursor.fetchone()
        return(mps)

    def agregar_medio_pago(self, tipo, descuento, clase):
        q1 = f'INSERT INTO medios_pago (tipo, descuento, clase) VALUES ("{tipo}", {descuento}, "{clase}")'
        try:
            self.cursor.execute(q1)
            self.conn.commit()
            return(True)
        except:
            return(False)

    def modificar_medio_pago(self, tipo, descuento, clase, id):
        q1 = f'UPDATE medios_pago SET tipo = "{tipo}", descuento = {descuento}, clase = "{clase}" WHERE id = {id}'
        try:
            self.cursor.execute(q1)
            self.conn.commit()
            return(True)
        except:
            return(False)

    def eliminar_medio_pago(self, id):
        q1 = f'DELETE FROM medios_pago WHERE id = {id}'
        try:
            self.cursor.execute(q1)
            self.conn.commit()
            return(True)
        except:
            return(False)



cnx = cnx('localhost', 'smart', 'Smart@Tech22', 'sql10715490')

@app.route('/')
def index():
    productos = cnx.get_productos()
    return render_template('index.html', productos = productos)

@app.route('/productosj')
def indexj():
    productos = cnx.get_productos()
    return jsonify(productos)

@app.route('/historia')
def historia():
    return render_template('historia.html')


@app.route('/medios_pago')
def medios_pago():
    mps = cnx.get_medios_pago()
    return render_template('medios_pago.html', mps = mps) 


@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    if (request.method == 'GET'):
        if (id == 0):
            mps = [0, '', 0, '']
        else:
            mps = cnx.get_medio_pago(id)
        return render_template('modificar_medios_pago.html', mps = mps)
    else:
        fi = int(request.form['fi'])
        ft = request.form['ft']
        fd = request.form['fd']
        fc = request.form['fc']

        if (fi == 0):
            if (not cnx.agregar_medio_pago(ft, fd, fc)):
                return 'Error agregando medio de pago'
        else:
            if (not cnx.modificar_medio_pago(ft, fd, fc, fi)):
                return 'Error modificando medio de pago'
        return redirect('/medios_pago') 


@app.route('/eliminar/<int:id>')
def eliminar(id):
    if (not cnx.eliminar_medio_pago(id)):
        return 'Error eliminando medio de pago'
    return redirect('/medios_pago')



@app.route('/registro_consultas')
def registro_consultas():
    return render_template('registro_consultas.html')


if (__name__ == '__main__'):
    app.run(debug=True)
