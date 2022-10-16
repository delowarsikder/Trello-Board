from os import stat
from flask import Flask, render_template, url_for, request, redirect,flash,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import null

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)
app.secret_key = 'secretKey'

###Target task model
class Todo(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  content=db.Column(db.String(200),nullable=False)
  date_created=db.Column(db.DateTime,default=datetime.utcnow)
  status=db.Column(db.Integer,nullable=False)

  def __repr__(self):
    return '<Task %r>' % self.id


@app.route('/',methods=['POST','GET'])
def index():

  if request.method == 'GET':
    allTasks=Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html',allTasks=allTasks)

  if request.method=='POST':
    status=0
    ##check status
    if request.form['click']=='todo_btn':
      status=0
    elif request.form['click']== 'doing_btn':
      status=1
    elif request.form['click']=='done_btn':
      status=2

    task_content=request.form['content']
    if task_content !="":
      new_task=Todo(content=task_content,status=status)
    else:
      return redirect('/')

    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an issue'



@app.route('/delete/<int:id>')
def delete(id):
  task_to_delete=Todo.query.get_or_404(id)
  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

  except:
    return 'There is a problem'


@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
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

###change task state Todo->Doing->Done
@app.route('/readyTask/<int:id>')
def readyTask(id):
  current_task=Todo.query.get_or_404(id)
  print ("before doing Task: ",current_task.status)
  if current_task.status==0:
    current_task.status=1
  elif current_task.status==1:
    current_task.status=2

  try:
    db.session.commit()
    return redirect('/')

  except:
    return 'There is a problem'

# Create the table
db.init_app(app)
with app.app_context():
    db.create_all()

##start main here
if __name__=='__main__':
  app.run(host='localhost',port=5000,debug=True)

