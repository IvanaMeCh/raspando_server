from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

# aca instanciamos la base de datos con la configuracion de la app
db = SQLAlchemy(app)

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100))
    movimientos = db.relationship('Movimiento', backref='categoria', lazy='dynamic')

class Movimiento(db.Model):
    __tablename__ = 'movimientos'
    id = db.Column(db.Integer, primary_key = True)
    descripcion = db.Column(db.String(50))
    monto = db.Column(db.Integer)
    es_ingreso = db.Column(db.Boolean)
    creado_en = db.Column(db.DateTime, default = datetime.now)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))


@app.route('/')
def index():


    todos_los_movimientos = Movimiento.query.all()
    print(todos_los_movimientos)

    dinero_disponible = 0
    for movimiento in todos_los_movimientos:
        if movimiento.es_ingreso == True:
            dinero_disponible += movimiento.monto
        else:
            dinero_disponible -= movimiento.monto
    print(dinero_disponible)

    return render_template('index.html',dinero_disponible=dinero_disponible)

with app.app_context(): 
    db.create_all() 