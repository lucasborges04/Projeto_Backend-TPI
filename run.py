from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Definir modelo de dados
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), unique=True, nullable=False)

@app.route('/')
def index():
    tasks = Tasks.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/create', methods=["POST"])
def create_task():
    description = request.form['description']

    # Valida se a task já foi criada
    exist_task = Tasks.query.filter_by(description=description).first()
    if exist_task:
        return 'Erro: Task já existe!', 400

    new_task = Tasks(description = description)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)