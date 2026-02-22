from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
import pyodbc
from forms import SignupForm, LoginForm, TimesheetForm
import bcrypt
from datetime import datetime
from functools import wraps


app = Flask(__name__)
app.secret_key = "my_secret_key"

conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=VASU\\SQLEXPRESS;"
    "Database=vasudb;"
    "Trusted_Connection=yes;"
)

def get_connection():
    return pyodbc.connect(conn_str)



#the footer year updates automatically
@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session:
            flash("Please login first", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function



def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" in session:
            flash("Please logout first", "error")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/signup", methods=["GET", "POST"])
@logout_required
def signup():

    # if "email" in session:
    #     return redirect(url_for("index"))

    form = SignupForm()
    conn = get_connection()
    cursor = conn.cursor()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data   # hash later

        # CHECK EMAIL EXISTS
        existing_user = cursor.execute(
            "SELECT Id FROM FlaskTodoUsers WHERE Email = ?",
            (email,)
        ).fetchone()

        if existing_user:
            # flash("Email already exists!", "error")
            form.email.errors.append("Email already exists!")
            return render_template("signup.html", form=form)
        
         # HASH PASSWORD
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # INSERT USER
        cursor.execute(
            "INSERT INTO FlaskTodoUsers (Name, Email, Password) VALUES (?, ?, ?)",
            (name, email, hashed_pw)
        )
        conn.commit()
        conn.close()

        flash("Signup successful!", "success")
        return redirect(url_for("login"))

    return render_template("signup.html", form=form)



# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     form = SignupForm()
#     conn = get_connection()
#     cursor = conn.cursor()

#     if form.validate_on_submit():
#         name = form.name.data
#         email = form.email.data
#         password = form.password.data   # hash later

#         # CHECK EMAIL EXISTS
#         existing_user = cursor.execute(
#             "SELECT Id FROM FlaskTodoUsers WHERE Email = ?",
#             (email,)
#         ).fetchone()

#         if existing_user:
#             flash("Email already exists!", "error")
#             return redirect(url_for("signup"))

#         # INSERT USER
#         cursor.execute(
#             "INSERT INTO FlaskTodoUsers (Name, Email, Password) VALUES (?, ?, ?)",
#             (name, email, password)
#         )
#         conn.commit()
#         conn.close()

#         flash("Signup successful!", "success")
#         return redirect(url_for("login"))

#     return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
@logout_required
def login():

    # if "email" in session:
    #     return redirect(url_for("index"))

    form = LoginForm()
    conn = get_connection()
    cursor = conn.cursor()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # CHECK EMAIL
        user = cursor.execute(
            "SELECT Id, Email, Password FROM FlaskTodoUsers WHERE Email = ?",
            (email,)
        ).fetchone()

        if not user:
            # flash("Email not registered", "error")
            form.email.errors.append("Email not registered")
            return render_template("login.html", form=form)
        
        stored_hashed_pw = user.Password  # from DB

        # Convert string → bytes
        stored_hashed_pw = stored_hashed_pw.encode("utf-8")

       # VERIFY PASSWORD
        if bcrypt.checkpw(password.encode("utf-8"), stored_hashed_pw):
            session["user_id"] = user[0]
            session["email"] = user[1]
            flash("Login successful", "success")
            return redirect(url_for("index"))
        else:
            #flash("Incorrect password", "error")
            form.password.errors.append("Incorrect password")
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)



# @app.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     conn = get_connection()
#     cursor = conn.cursor()

#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password.data

#         # CHECK EMAIL
#         user = cursor.execute(
#             "SELECT Id, Password FROM FlaskTodoUsers WHERE Email = ?",
#             (email,)
#         ).fetchone()

#         if not user:
#             flash("Email not registered", "error")
#             return redirect(url_for("login"))

#         # CHECK PASSWORD
#         if user.Password != password:   # hash check later
#             flash("Incorrect password", "error")
#             return redirect(url_for("login"))

#         # SUCCESS
#         flash("Login successful!", "success")
#         return redirect(url_for("index"))  

#     return render_template("login.html", form=form)







@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # if "email" not in session:
    #     flash("Please login first", "error")
    #     return redirect(url_for("login"))
    # else:
    #     flash("user can not access login page without logout", "error")
    
    email = session.get("email")

    conn = get_connection()
    cursor = conn.cursor()
    edit_todo = None

    try:
        if request.method == 'POST':
            task = request.form.get("task")
            id = request.form.get("id")

            if not task:
                flash("Task cannot be empty!", "error")
                return redirect(url_for('index'))

            if id:
                cursor.execute(
                    "UPDATE FlaskTodo SET Task = ? WHERE Id = ?",
                    (task, id)
                )
                flash("Task updated successfully!", "success")
            else:
                cursor.execute(
                    "INSERT INTO FlaskTodo (Task) VALUES (?)",
                    (task,)
                )
                flash("Task added successfully!", "success")

            conn.commit()
            return redirect(url_for('index'))

    except Exception as e:
        conn.rollback()
        flash("Something went wrong!", "error")

    # Load edit data
    edit_id = request.args.get("edit_id")
    if edit_id:
        edit_todo = cursor.execute(
            "SELECT * FROM FlaskTodo WHERE Id = ?",
            (edit_id,)
        ).fetchone()

    todos = cursor.execute("SELECT * FROM FlaskTodo").fetchall()
    conn.close()

    return render_template(
        "index.html",
        todos=todos,
        edit_todo=edit_todo,
        email=email
    )


@app.route('/delete/<int:id>')
def delete(id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM FlaskTodo WHERE Id = ?", (id,))
        conn.commit()
        flash("Task deleted successfully!", "success")
    except:
        conn.rollback()
        flash("Failed to delete task!", "error")
    finally:
        conn.close()

    return redirect(url_for('index'))




@app.route("/logout")
def logout():
    session.clear()   # removes all session data
    flash("Logged out successfully", "success")
    return redirect(url_for("login"))






@app.route("/form", methods=["GET", "POST"])
def form():

    form = TimesheetForm()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT project_id, project_name FROM tsprojects")
    projects = cursor.fetchall()

    # form.project.choices = [(row.project_id, row.project_name) for row in projects]
    # form.task.choices = []
    # form.activity.choices = []

    form.project.choices = [(0, "--select--")] + [
    (row.project_id, row.project_name) for row in projects
    ]
    form.task.choices = [(0, "--select--")]
    form.activity.choices = [(0, "--select--")]

    conn.close()

    return render_template("addTime.html", form=form)



@app.route("/get_tasks/<int:project_id>")
def get_tasks(project_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT task_id, task_name FROM tsproject_tasks WHERE project_id = ?", project_id)
    tasks = cursor.fetchall()

    result = []
    for row in tasks:
        result.append({
            "id": row.task_id,
            "name": row.task_name
        })

    conn.close()

    return jsonify(result)


@app.route("/get_activities/<int:task_id>")
def get_activities(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT activity_id, activity_name FROM tstask_activities WHERE task_id = ?",
        (task_id,)
    )

    activities = cursor.fetchall()

    result = []
    for row in activities:
        result.append({
            "id": row[0],
            "name": row[1]
        })

    conn.close()
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)








