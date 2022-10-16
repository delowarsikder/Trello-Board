from flask import Flask, render_template, url_for, request, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='trello'
db=MySQL(app)



class Todo(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  content=db.Column(db.String(200),nullable=False)
  date_created=db.Column(db.DateTime,default=datetime.utcnow)

  def __repr__(self):
    return '<Task %r>' % self.id


with app.app_context():
    db.create_all()


@app.route('/',methods=['POST','GET'])
def index():
  print("shouted from index")
  if request.method=='POST':
    task_content=request.form['content']
    if task_content !="":
      new_task=Todo(content=task_content)
    else:
      flash("No task add")
      # return "No task add"
      return redirect('/')

    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an issue'
  else:
    tasks=Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html',tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
  # print("shouted from delete section")
  task_to_delete=Todo.query.get_or_404(id)
  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

  except:
    return 'There is a problem'


@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
  print("shouted from Update section") 
  task_to_update=Todo.query.get_or_404(id)

  if request.method=="POST":
    info=request.form['content']
    task_to_update.content=request.form['content']

    if info!="":
      try:
        db.session.commit()
        return redirect('/') 
      except:
        return 'There was error when updating task'
    else:
      print("Your update section is blank")
      return redirect('/')

  else:
    return render_template('update.html',task=task_to_update)

###complete task

@app.route('/complete/<int:id>')
def complete(id):
  task_to_done=Todo.query.get_or_404(id)
  print("completed task :",task_to_done.content)
  return "your task is completed"







##start main here
if __name__=='__main__':
  app.run(host='localhost',port=5050,debug=True)

