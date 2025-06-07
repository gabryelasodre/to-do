from cProfile import label

from flask import Flask, request
import sqlite3


con = sqlite3.connect("todo.db", check_same_thread=False)


# CRUD - Create read update delete
#        POST   GET  PUT    DELETE

app = Flask(__name__)

@app.route("/")
def obter_lista():
    return "<p>Hello, World!</p>"

@app.route("/", methods=["POST"])
def criar_todo():
    cur = con.cursor()
    label = request.json ['label']
    cur.execute(f"INSERT INTO TODO VALUES ('{label}') ")
def atualizar_todo():
    pass
def deletar_todo():
    pass

