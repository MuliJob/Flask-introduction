from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder="template") 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            print("Your task was added successfully")
            return redirect('/')
        except:
            return "Error!!! Failed to add task to database"
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    delete_task = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(delete_task)
        db.session.commit()
        print("Task was deleted successfully")
        return redirect('/')
    except:
        return "An error occured when deleting the task"
    
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content'] 
        
        try:
            db.session.commit()
            print("Task updated successfully")
            return redirect('/')
        except:
            return "There was an issue updating the database"
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True) 