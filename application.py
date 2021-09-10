from sys import float_repr_style
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(application)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Task %r>' % self.id

@application.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        chore_content = request.form['content']
        new_chore = Todo(content=chore_content)

        try:
            db.session.add(new_chore)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your chore'

    else:
        chores = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', chores=chores)

@application.route('/delete/<int:id>')
def delete(id):
    chore_to_delete = Todo.query.get_or_404(id)

    try: 
        db.session.delete(chore_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that chore'


@application.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    chore = Todo.query.get_or_404(id)

    if request.method == 'POST':
        chore.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except: 
            return 'There was a problem updating your chore'

    else:
        return render_template('update.html', chore=chore)

    if __name__ == "__main__":
      application.run(debug=True)