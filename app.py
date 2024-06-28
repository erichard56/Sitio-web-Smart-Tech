from flask import Flask     # pip install flask
from flask import render_template, request, redirect, jsonify
import mysql.connector      # pip instal mysql-connector-python

app = Flask(__name__)

conn = mysql.connector.connect(
    # host = 'sql10.freemysqlhosting.net',
    # user = 'sql10715490',
    # password = 'vpy7xcsZkk',
    # database = 'sql10715490'
    host = 'localhost',
    user = 'smart',
    password = 'Smart@Tech22',
    database = 'sql10715490'
)
cursor = conn.cursor()


@app.route('/')
def index():
    q1 = 'SELECT * FROM productos ORDER BY id'
    cursor.execute(q1)
    productos = cursor.fetchall()
    return render_template('index.html', productos = productos)
    # return jsonify(productos)

@app.route('/j')
def indexj():
    q1 = 'SELECT * FROM productos ORDER BY id'
    cursor.execute(q1)
    productos = cursor.fetchall()
    # return render_template('index.html', productos = productos)
    return jsonify(productos)

@app.route('/historia')
def historia():
    return render_template('historia.html')


@app.route('/medios_pago')
def medios_pago():
    q1 = 'SELECT * FROM medios_pago'
    cursor.execute(q1)
    mps = cursor.fetchall()
    return render_template('medios_pago.html', mps = mps) 
    # return jsonify(mps)


@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    if (request.method == 'GET'):
        if (id == 0):
            mps = [0, '', 0, '']
        else:
            q1 = 'SELECT * FROM medios_pago WHERE id = ' + str(id)
            cursor.execute(q1)
            mps = cursor.fetchone()
        return render_template('modificar_medios_pago.html', mps = mps)
    else:
        fi = int(request.form['fi'])
        ft = request.form['ft']
        fd = request.form['fd']
        fc = request.form['fc']

        if (fi == 0):
            q1 = 'INSERT INTO medios_pago (tipo, descuento, clase) VALUES (%s, %s, %s)' 
            cursor.execute(q1, (ft, fd, fc))
        else:
            q1 = 'UPDATE medios_pago SET tipo = %s, descuento = %s, clase = %s WHERE id = %s'
            cursor.execute(q1, (ft, fd, fc, fi))
        conn.commit()
        return redirect('/medios_pago') 


@app.route('/eliminar/<int:id>')
def eliminar(id):
    q1 = 'DELETE from medios_pago WHERE id = ' + str(id)
    cursor.execute(q1)
    return redirect('/medios_pago')


@app.route('/registro_consultas')
def registro_consultas():
    return render_template('registro_consultas.html')


if (__name__ == '__main__'):
    app.run(debug=True)
