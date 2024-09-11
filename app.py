from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'blog_db'

mysql = MySQL(app)



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            flash("You need to login first", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        gender = request.form['gender']
        
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO users (name, email, password, phone, gender) VALUES (%s, %s, %s, %s, %s)", 
                        (name, email, password, phone, gender))
            mysql.connection.commit()
            cur.close()
            flash("Registration successful!", "success")
            return redirect(url_for('login'))
        except Exception as e:
            mysql.connection.rollback()
            msg = f"Error in registration: {e}"
    
    return render_template('registration.html', msg=msg)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
            user = cur.fetchone()
            cur.close()
            
            if user:
                session['loggedin'] = True
                session['username'] = user['name']
                flash("Login successful!", "success")
                return redirect(url_for('posts'))
            else:
                msg = "Invalid email or password"
        except Exception as e:
            msg = f"Error in login: {e}"
    
    return render_template('login.html', msg=msg)

# Logout Route
@app.route('/logout')
@login_required
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    flash("You have been logged out", "success")
    return redirect(url_for('login'))

# Posts Route (Protected)
@app.route('/posts')
@login_required
def posts():
    if 'loggedin' not in session:
        flash("You need to login first", "warning")
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM posts")
    post = cur.fetchall()
    cur.close()
    
    return render_template("blogs.html", post=post)

@app.route('/create_post')
@login_required
def create_post():
    if 'loggedin' not in session:
        flash("You need to login first", "warning")
        return redirect(url_for('login'))
    return render_template("create_post.html")

# Create Post Route
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author_id = request.form['author_id']
        
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO posts (title, content, author_id) VALUES (%s, %s, %s)", (title, content, author_id))
            mysql.connection.commit()
            cur.close()
            flash("Post created successfully!", "success")
            return redirect(url_for('posts'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f"Error in creating post: {e}", "danger")
    
    return render_template('create_post.html')


@app.route('/deletepost')
def deletepost():
    return render_template('delete_post.html')
# Delete Post Route
@app.route('/delete_post', methods=['GET', 'POST'])

def delete_post():
    
    if request.method == 'POST':
        post_id = request.form['post_id']
        
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("DELETE FROM posts WHERE post_id=%s", (post_id,))
            mysql.connection.commit()
            cur.close()
            flash("Post deleted successfully!", "success")
            return redirect(url_for('posts'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f"Error in deleting post: {e}", "danger")
    
    return render_template('delete_post.html')

# Contact Route
@app.route('/contact')
@login_required
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)
