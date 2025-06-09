from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CRUD - Create read update delete
#        POST   GET  PUT    DELETE


def cria_tabelas_sql_nativo():
    with db.engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS to_do (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(120) NOT NULL,
                checked INTEGER DEFAULT 0
            );
        """))

        conn.commit()


with app.app_context():
    cria_tabelas_sql_nativo()


@app.route("/")
def obter_lista():
    with db.engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM to_do"))
        rows = result.fetchall()
        lista = []
        for row in rows:
            # converte o Row em dict explicitamente
            lista.append({
                "id": row[0],
                "title": row[1],
                "checked": bool(row[2])
            })
        return jsonify(lista)


@app.route("/", methods=["POST"])
def criar_todo():
    title = request.json['title']
    with db.engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO to_do (title)
            VALUES (:title)
        """), {
            'title': title
        })

        conn.commit()

    return {
        "mensagem": "sucesso"
    }, 200


@app.route("/", methods=["PUT"])
def atualizar_todo():
    todo_id = request.args.get('id')
    with db.engine.begin() as conn:
        result = conn.execute(text("SELECT  *FROM to_do WHERE id = :id"), {'id': todo_id})
        row = result.fetchone()
        checked = row[2]
        if checked == 0:
            checked = 1
        else:
            checked = 0

        conn.execute(text("""
                UPDATE to_do SET checked = :checked
                WHERE id = :id 
            """), {
            'checked': checked,
            'id': todo_id
        })

        conn.commit()

    return {}, 200


@app.route("/<int:todo_id>", methods=["DELETE"])
def deletar_todo(todo_id):
    with db.engine.begin() as conn:
        result = conn.execute(
            text("DELETE FROM to_do WHERE id = :id"),
            {'id': todo_id})

        linhas_afetadas = result.rowcount

    if linhas_afetadas == 0:
        return {"mensagem": "Tarefa não encontrada"}, 204
    else:
        conn.commit()
        return {"mensagem": f"{linhas_afetadas} to-do deletado :("}, 200


if __name__ == "__main__":
    app.run(debug=True)
