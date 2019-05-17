from flask import Flask, redirect,request, render_template
from mysqlconnection import connectToMySQL
app = Flask(__name__)

@app.route("/users")
def main():
    mysql = connectToMySQL('users')

    allUsers = mysql.query_db("SELECT * FROM all_users;")
    return render_template("users.html",all_my_users =allUsers )

@app.route("/add_new")
def addUser():
    return render_template("addUser.html")

@app.route("/username", methods=['POST'])
def username():
    found = False
    mysql = connectToMySQL('users')        # connect to the database
    query = "SELECT first_name FROM all_users WHERE first_name = %(fn)s;"
    data = { 
        'fn': request.form['fname'],
     }
    result = mysql.query_db(query, data)
    if result:
        found = True
    return render_template('partials/username.html', found=found)

@app.route("/process",methods=['POST'])
def add_to_db():
    mysql = connectToMySQL("users") #name of your schema

    query = "INSERT INTO all_users (first_name,last_name,email,created_at) VALUES (%(fn)s,%(ln)s,%(em)s,NOW());"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "em": request.form["email"]
    }
    new_user_id = mysql.query_db(query,data)
    return redirect("/users")

@app.route("/users/<id>")
def showOne(id):
    mysql = connectToMySQL("users")

    query = "SELECT * FROM all_users WHERE id = %(id_num)s;"
    data = {
        'id_num' : id
    }
    this_One = mysql.query_db(query, data)
    print(data)
    return render_template("showOne.html",oneUser = this_One)

@app.route("/edit/<id>")
def edit(id):
    mysql = connectToMySQL("users")

    query = "SELECT * FROM all_users WHERE id = %(id_num)s;"
    data = {
        'id_num' : id
    }
    edit_One = mysql.query_db(query, data)
    print(data)
    return render_template("edit.html",edit_this = edit_One)

@app.route("/update/<id>",methods = ["POST"])
def update(id):
    mysql = connectToMySQL("users")

    query = "UPDATE all_users SET first_name=%(fn)s,last_name=%(ln)s,email=%(em)s WHERE id = %(id_num)s;"
    data = {
        'id_num' : id,
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "em": request.form["email"]
    }
    update_One = mysql.query_db(query, data)
    print(data)
    return redirect("/users")

@app.route("/delete/<id>", methods= ["GET"])
def destroy(id):
    mysql = connectToMySQL("users")

    query = "DELETE FROM all_users WHERE id = %(id_num)s;"
    data = {
        'id_num' : id
    }
    update_One = mysql.query_db(query, data)
    print(data)
    return redirect("/users")

if __name__=='__main__':
    app.run(debug = True)