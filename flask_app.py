# all the imports
import MySQLdb
import md5
from flask import Flask, request, jsonify, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
DEBUG = True
SECRET_KEY = ''

app = Flask(__name__)
app.config.from_object(__name__)


if __name__ == '__main__':
    app.run()

@app.before_request
def before_request():
    g.db = MySQLdb.connect(host="mysql.server", user="", passwd="", db="goallist")

@app.after_request
def after_request(response):
    g.db.commit()
    g.db.close()
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username_entry = request.form['username']
        db_login = MySQLdb.connect(host="mysql.server", user="", passwd="", db="goallistusers")
        cur2 = db_login.cursor()
        cur2.execute("""select password from users where username=%s""", (username_entry))
        results = cur2.fetchall()
        password_entry = results[0][0]
        #if request.form['username'] != app.config['USERNAME']:
         #error = 'Invalid username'
        if md5.new(request.form['password']).hexdigest() != password_entry:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    error = None
    if request.method == 'POST':
        username_entry = request.form['username']
        db_login = MySQLdb.connect(host="mysql.server", user="", passwd="", db="goallistusers")
        cur2 = db_login.cursor()
        cur2.execute("""select password from users where username=%s""", (username_entry))
        results = cur2.fetchall()
        password_entry = results[0][0]
        #if request.form['username'] != app.config['USERNAME']:
         #error = 'Invalid username'
        if md5.new(request.form['password']).hexdigest() != password_entry:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/add', methods=['POST'])
def add_entry():
    cur = g.db.cursor()
    username = session['username']
    test_form1 = request.form['goal']
    test_form2 = request.form['priority']
    test_form3 = request.form['category']
    cur.execute("""INSERT INTO goals (goal, priority, category, subgoal, users) VALUES (%s, %s, %s, 0, %s)""", (test_form1, test_form2,test_form3,username))
    return redirect(url_for('show_entries'))

@app.route('/delete')
def delete_goal():
    username = session['username']
    cur = g.db.cursor()
    cur.execute("""DELETE FROM goals WHERE trash=1 and users=%s""",(username))
    return redirect(url_for('show_entries'))

@app.route('/')
def show_entries():
    cur = g.db.cursor()
    if 'username' in session:
        username = session['username']
        cur.execute("""select goal, done_value, priority, entered_time, id, category from goals where trash=0 and archive=0 and users=%s order by done_value asc, priority desc""",(username))
        entry_fetch = cur.fetchall()
        entries = [dict(goal=row[0], done_value=row[1], priority=row[2], entered_time=row[3], id=row[4], category=row[5]) for row in entry_fetch]
        cur.execute("""select count(goal) from goals where trash=0 and users=%s""",(username))
        count_fetch = cur.fetchall()
        count_goals = [dict(count=row[0]) for row in count_fetch]
        cur.execute("""select count(goal) from goals where trash=0 and users=%s and done_value=0""",(username))
        count_fetch = cur.fetchall()
        count_goals_undone = count_fetch[0][0]
        cur.execute("""select count(goal) from goals where trash=0 and users=%s and done_value=1""",(username))
        count_fetch = cur.fetchall()
        count_goals_done = count_fetch[0][0]
        return render_template('main.html', entries=entries, count_goals=count_goals,count_goals_undone=count_goals_undone,count_goals_done=count_goals_done)
    return redirect(url_for('login'))

@app.route('/trash')
def show_trash():
    cur = g.db.cursor()
    username = session['username']
    cur.execute("""select goal, done_value, priority, entered_time, id, category from goals where trash=1 and users=%s order by done_value asc""",(username))
    entry_fetch = cur.fetchall()
    entries = [dict(goal=row[0], done_value=row[1], priority=row[2], entered_time=row[3], id=row[4], category=row[5]) for row in entry_fetch]
    return render_template('main.html', entries=entries)

@app.route('/archive')
def show_archive():
    cur = g.db.cursor()
    username=session['username']
    cur.execute("""select goal, done_value, priority, entered_time, id, category from goals where archive=1 and trash=0 and users=%s order by done_value asc""",(username))
    entry_fetch = cur.fetchall()
    entries = [dict(goal=row[0], done_value=row[1], priority=row[2], entered_time=row[3], id=row[4], category=row[5]) for row in entry_fetch]
    return render_template('main.html', entries=entries)

@app.route('/_add_numbers')
def add_numbers():
    #a = id, b=+1
    a = request.args.get('a', 0, type=int)
    cur = g.db.cursor()
    cur.execute("""UPDATE goals SET priority = priority + 1 WHERE id=%s""", (a))
    cur.execute("""SELECT priority FROM goals WHERE id=%s""",(a))
    priority_fetch = cur.fetchall()
    new_priority = priority_fetch[0][0]
    if new_priority > 5:
        new_priority = 5
        cur.execute("""UPDATE goals SET priority = 5 WHERE id=%s""", (a))
    return jsonify(result=new_priority)

@app.route('/_subtract_numbers')
def subtract_numbers():
    #a = id, b=+1
    a = request.args.get('a', 0, type=int)
    cur = g.db.cursor()
    cur.execute("""UPDATE goals SET priority = priority - 1 WHERE id=%s""", (a))
    cur.execute("""SELECT priority FROM goals WHERE id=%s""",(a))
    priority_fetch = cur.fetchall()
    new_priority = priority_fetch[0][0]
    if new_priority < 1:
        new_priority = 1
        cur.execute("""UPDATE goals SET priority = 1 WHERE id=%s""", (a))
    return jsonify(result=new_priority)

@app.route('/_done_check')
def done_check():
    a = request.args.get('a', 0, type=int)
    cur = g.db.cursor()
    cur.execute("""UPDATE goals SET done_value = 1 WHERE id=%s""", (a))
    return jsonify(result='success!')

@app.route('/_done_uncheck')
def done_uncheck():
    a = request.args.get('a', 0, type=int)
    cur = g.db.cursor()
    cur.execute("""UPDATE goals SET done_value = 0 WHERE id=%s""", (a))
    return jsonify(result='success!')

@app.route('/_move_main')
def move_main():
    a = request.args.get('a', 0, type=int)
    cur = g.db.cursor()
    cur.execute("""UPDATE goals SET archive=0, trash=0 WHERE id=%s""", (a))
    return jsonify(result='success!')

@app.route('/_move_archive')
def move_archive():
    a = request.args.get('a', 0, type=int)
    cur = g.db.cursor()
    cur.execute("""UPDATE goals SET archive=1, trash=0 WHERE id=%s""", (a))
    return jsonify(result='success!')

@app.route('/_move_trash')
def move_trash():
    a = request.args.get('a', 0, type=int)
    cur = g.db.cursor()
    cur.execute("""UPDATE goals SET trash=1, archive=0 WHERE id=%s""", (a))
    return jsonify(result='success!')

@app.route('/jsonexample')
def jsonexample():
    return render_template('jsonexample.html')

@app.route('/checkbox')
def checkbox():
    return render_template('checkbox.html')

@app.route('/move_disappear')
def move_disappear():
    return render_template('move_disappear.html')

