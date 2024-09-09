from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Your MySQL server address
app.config['MYSQL_USER'] = 'root'        # Your MySQL username
app.config['MYSQL_PASSWORD'] = 'root' # Your MySQL password
app.config['MYSQL_DB'] = 'blog_db'      # Your database name

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/regis')
def registration():
    return render_template('registration.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            phone = request.form['phone']
            gender = request.form['gender']

            # Database operation
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO users (name, email, password, phone, gender) VALUES (%s, %s, %s, %s, %s)", (name, email, password, phone, gender))
            mysql.connection.commit()
            cur.close()

            # Redirect to login page if successful
            return redirect(url_for('login'))

        except Exception as e:
            # Rollback if error occurs
            mysql.connection.rollback()
            msg = f"Error in registration: {e}"

    # Render registration page with error message if any
    return render_template('registration.html', msg=msg)

@app.route('/login')
def login():
    return render_template('login.html')
    

@app.route('/login_check', methods=['GET', 'POST'])
def login_check():
    msg = ''
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']

            # Database operation
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
            user = cur.fetchone()
            cur.close()

            if user:
                return redirect(url_for('posts'))
                # return redirect(url_for('posts'))
            else:
                msg = "Invalid email or password"

        except Exception as e:
            msg = f"Error in login: {e}"

    # Render login page with error message if any
    return render_template('login.html', msg=msg)
           


@app.route('/posts')
def posts():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM posts")
    post = cur.fetchall()
    cur.close()
    return render_template("blogs.html", post=post )

@app.route('/create_post')
def create_post():
    return render_template('create_post.html')


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    msg = ''
    if request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['content']
            author_id = request.form['author_id']

            # Database operation
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO posts (title, content,author_id) VALUES (%s, %s, %s)", (title, content,author_id))
            mysql.connection.commit()
            cur.close()

            # Redirect to login page if successful
            return redirect(url_for('posts'))

        except Exception as e:
            # Rollback if error occurs
            mysql.connection.rollback()
            msg = f"Error in registration: {e}"

    # Render registration page with error message if any
    return redirect(url_for('posts'))


@app.route('/delete_post')
def delete_post():
    return render_template('delete_post.html')

@app.route('/deletepost', methods=['GET', 'POST'])
def deletepost():
    msg = ''
    if request.method == 'POST':
        try:
            title = request.form['title']
            post_id = request.form['post_id']

            # Database operation
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("DELETE FROM posts WHERE title=%s and post_id=%s", (title,post_id))
            mysql.connection.commit()
            cur.close()

            # Redirect to login page if successful
            return redirect(url_for('posts'))

        except Exception as e:
            # Rollback if error occurs
            mysql.connection.rollback()
            msg = f"Error in registration: {e}"

    # Render registration page with error message if any
    return redirect(url_for('posts'))


if __name__ == '__main__':
    app.run(debug=True)
