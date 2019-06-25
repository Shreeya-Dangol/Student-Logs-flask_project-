from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'flash_message'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'student'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    data = cur.fetchall()
    cur.close()

    cursor = mysql.connection.cursor()
    cursor.execute("Select passed_student.id, student.id, student.name, student.score from student "
                   "INNER JOIN passed_student ON student.id = passed_student.id")
    cursor.execute("Select fail_student.id, student.id, student.name, student.score from student "
                   "INNER JOIN fail_student ON student.id = fail_student.id")
    d = cursor.fetchall()
    cursor.close()

    cursor1 = mysql.connection.cursor()
    # changes
    # cursor1.execute("insert into passed_student2 (name,score,id) select distinct name,score,id from passed_student")
    cursor1.execute("SELECT distinct id,name,score FROM passed_student")
    #
    d1 = cursor1.fetchall()
    cursor1.close()

    cursor2 = mysql.connection.cursor()
    cursor2.execute("SELECT distinct id,name,score FROM fail_student")
    f = cursor2.fetchall()
    cursor2.close()

    return render_template('index.html', student=data, p_stu=d, x=d1, f=f)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Inserted Successfully!")
        name = request.form['name']
        email = request.form['email']
        score = request.form['score']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student (name,email,score,phone) values (%s,%s,%s,%s)", (name, email, score, phone))
        cur.close()

        cur1 = mysql.connection.cursor()
        cur1.execute(
            "insert into passed_student(name,score, id) select distinct name,score,id from student where score>32")

        # changes
        # cur1.execute("insert into passed_student2 (name,score,id) select distinct name,score,id from passed_student")
        mysql.connection.commit()
        cur1.close()

        cur2 = mysql.connection.cursor()
        cur2.execute(
            "insert into fail_student(name,score, id) select distinct name,score,id from student where score<32")
        mysql.connection.commit()
        cur2.close()

        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        id_data = request.form['id']
        name_data = request.form['name']
        email_data = request.form['email']
        score_data = request.form['score']
        phone_data = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE student SET name=%s, email=%s, score=%s, phone=%s WHERE id=%s",
                    (name_data, email_data, score_data, phone_data, id_data))
        cur.execute("UPDATE passed_student SET name=%s, score=%s WHERE id=%s",
                    (name_data, score_data,id_data))
        cur.execute("UPDATE fail_student SET name=%s, score=%s WHERE id=%s",
                    (name_data, score_data,id_data))
        flash("Updated Successfully!")

        # name_d1 = request.form['name']
        # score_d1 = request.form['score']
        # id_d1 = request.form['id']

        # cur1 = mysql.connection.cursor()
        # cur1.execute("UPDATE student SET pid=%s, name=%s, score=%s, id=%s WHERE id=%s", (pid_d1, name_d1, score_d1, id_d1))

    mysql.connection.commit()
    return redirect(url_for("index"))


@app.route("/delete/<string:id_data>", methods=['GET', 'POST'])
def delete(id_data):
    flash("Deleted Successfully!")

    cur = mysql.connection.cursor()
    cur.execute("DELETE from student where id = %s", (id_data))

    mysql.connection.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=5050, debug=True)
