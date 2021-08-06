from flask import Flask, render_template, request, redirect, sessions, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///pratik.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'any random string'


class User(db.Model):
    name = db.Column(db.String, primary_key=True)
    passwd = db.Column(db.String, nullable=False)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    user_t_no = db.Column(db.Integer, nullable=False)
    Issue = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    i_o = db.Column(db.String(10), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


# db.create_all()


# newUser=User(name="admin",passwd="admin")
# newUser2=User(name="user",passwd="user")
# db.session.add(newUser)
# db.session.add(newUser2)
# db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        newUser = User.query.filter_by(name=request.form['name']).first()
        if newUser is None:
            return render_template('loginPage.html')
        else:
            # username is correct check for password
            if newUser.passwd == request.form['password']:
                # if password is correct then user will be logged in
                session['username'] = newUser.name
                return redirect('/render_name')
            else:
                # if password is wrong then login page will render again
                return render_template('loginPage.html')
    else:
        return render_template('loginPage.html')


@app.route('/name')
def hello_name():
    return 'Hello, This is Pratik Patil...!'


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/render_name', methods=['GET', 'POST'])
def hello_home():
    if 'username' in session:
        if request.method == 'POST':
            # sno=request.form['sno']
            username = request.form['user1']
            token1 = request.form['to']
            desc = request.form['desc']
            i_o = request.form['i_o']

            todo = Todo(username=username, user_t_no=token1,
                        Issue=desc, i_o=i_o)
            db.session.add(todo)
            db.session.commit()
        #db.execute("SELECT * FROM todo2 WHERE i_o=?", ("in",))
        allTodo = Todo.query.all()
        isAdmin = False
        if session['username'] == 'admin':
            isAdmin = True
        return render_template('index.html', allTodo=allTodo, isadmin=isAdmin)
    else:
        return redirect('/')


@app.route('/delete/<int:sno>')
def delete(sno):
    if 'username' in session:
        todo = Todo.query.filter_by(sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect("/render_name")
    else:
        return redirect('/')


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if 'username' in session:
        if request.method == 'POST':
            username = request.form['user1']
            token1 = request.form['to']
            desc = request.form['desc']
            i_o = request.form['i_o']

            todo = Todo.query.filter_by(sno=sno).first()
            todo.username = username
            todo.user_t_no = token1
            todo.Issue = desc
            todo.i_o = i_o
            db.session.add(todo)
            db.session.commit()
            return redirect("/render_name")
        todo = Todo.query.filter_by(sno=sno).first()
        return render_template('update.html', todo=todo)

        return render_template('update.html', todo=todo)
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)  # app.run(debug=True,port=8000 )
