from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.String(200), nullable=False)
    favorite = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)




db.create_all()

@app.route('/', methods=['POST', 'GET'])

def index():
    if request.method == 'POST':
        recipe_name = request.form['name']
        recipe_ingredient= request.form['ingredients']
        recipe_instructions= request.form['instructions']
        recipe_favourite= request.form['favorite']
        new_task = Recipe(name=recipe_name, ingredients=recipe_ingredient, instructions=recipe_instructions, favorite=False)


        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print("error",e)
            return 'There was an issue adding your task'
            
        return render_template('index.html')
    else:
        tasks = Recipe.query.order_by(Recipe.date_created).all()
        return render_template('index.html', recipes=tasks)



@app.route('/add', methods=['POST', 'GET'])

def add():
    if request.method == 'POST':
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        tasks = Recipe.query.order_by(Recipe.date_created).all()
        return render_template('add.html', names= tasks)


'''

def index():
    if request.method == 'POST':
        task_name = request.form['name']
        new_task = Recipe(name=task_name)


        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
        return render_template('index.html')
    else:
        tasks = Recipe.query.order_by(Recipe.date_created).all()
        return render_template('index.html', tasks=tasks)
        '''

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Recipe.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Recipe.query.get_or_404(id)

    if request.method == 'POST':
        task.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        tasks = Recipe.query.order_by(Recipe.date_created).all()
        return render_template('update.html', recipes= tasks,recipe=task)

if __name__ == '__main__':
    app.run(debug=True)