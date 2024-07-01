from flask import Flask     # pip install flask
from flask import render_template, request, redirect, jsonify
import mysql.connector      # pip instal mysql-connector-python

app = Flask(__name__)

# conn = mysql.connector.connect(
#     # host = 'sql10.freemysqlhosting.net',
#     # user = 'sql10715490',
#     # password = 'vpy7xcsZkk',
#     # database = 'sql10715490'
#     host = 'localhost',
#     user = 'smart',
#     password = 'Smart@Tech22',
#     database = 'sql10715490'
# )
# cursor = conn.cursor()

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
        q1 = 'SELECT * FROM medios_pago WHERE id = ' + str(id)
        self.cursor.execute(q1)
        mps = self.cursor.fetchone()
        return(mps)

    def agregar_medio_pago(self, tipo, descuento, clase):
        q1 = 'INSERT INTO medios_pago (tipo, descuento, clase) VALUES (%s, %s, %s)'
        try:
            self.cursor.execute(q1, (tipo, descuento, clase))
            self.commit()
            return(True)
        except:
            return(False)

    def modificar_medio_pago(self, tipo, descuento, clase, id):
        q1 = 'UPDATE medios_pago SET tipo = %s, descuento = %s, clase = %s WHERE id = ' + str(id)
        try:
            self.cursor.execute(q1, (tipo, descuento, clase))
            self.conn.commit()
            return(True)
        except:
            return(False)

    def eliminar_medio_pago(self, id):
        q1 = 'DELETE FROM medios_pago WHERE id = ' + str(id)
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
    # return jsonify(productos)

@app.route('/j')
def indexj():
    # q1 = 'SELECT * FROM productos ORDER BY id'
    # cursor.execute(q1)
    # productos = cursor.fetchall()
    # return render_template('index.html', productos = productos)
    productos = cnx.get_productos()
    return jsonify(productos)

@app.route('/historia')
def historia():
    return render_template('historia.html')


@app.route('/medios_pago')
def medios_pago():
    # q1 = 'SELECT * FROM medios_pago'
    # cursor.execute(q1)
    # mps = cursor.fetchall()
    mps = cnx.get_medios_pago()
    return render_template('medios_pago.html', mps = mps) 
    # return jsonify(mps)


@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    if (request.method == 'GET'):
        if (id == 0):
            mps = [0, '', 0, '']
        else:
            # q1 = 'SELECT * FROM medios_pago WHERE id = ' + str(id)
            # cursor.execute(q1)
            mps = cnx.get_medio_pago(id)
        return render_template('modificar_medios_pago.html', mps = mps)
    else:
        fi = int(request.form['fi'])
        ft = request.form['ft']
        fd = request.form['fd']
        fc = request.form['fc']

        if (fi == 0):
            # q1 = 'INSERT INTO medios_pago (tipo, descuento, clase) VALUES (%s, %s, %s)' 
            # cursor.execute(q1, (ft, fd, fc))
            if (not cnx.agregar_medio_pago(ft, fd, fc)):
                print('Error agregando medio de pago')
        else:
            # q1 = 'UPDATE medios_pago SET tipo = %s, descuento = %s, clase = %s WHERE id = %s'
            # cursor.execute(q1, (ft, fd, fc, fi))
            if (not cnx.modificar_medio_pago(ft, fd, fc, fi)):
                print('Error modificando medio de pago')
        # conn.commit()
        return redirect('/medios_pago') 


@app.route('/eliminar/<int:id>')
def eliminar(id):
    # q1 = 'DELETE FROM medios_pago WHERE id = ' + str(id)
    # cursor.execute(q1)
    if (not cnx.eliminar_medio_pago(id)):
        print('Error eliminando medio de pago')
    return redirect('/medios_pago')



@app.route('/registro_consultas')
def registro_consultas():
    return render_template('registro_consultas.html')


if (__name__ == '__main__'):
    app.run(debug=True)
