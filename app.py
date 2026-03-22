# app.py    : Debian 13: ~/flaskdev/bblogdev/
# Source - https://stackoverflow.com/a/67474104
# Posted by furas, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-21, License - CC BY-SA 4.0

from flask import Flask, render_template, request, render_template_string, redirect
import sqlite3 as sql

app = Flask(__name__)

DB_PATH = 'bibleblog.sqlite3'       # sqlite3 DB file

def create_database():
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS bblogtest (
                    Bid INTEGER PRIMARY KEY AUTOINCREMENT,
                    Bdate TEXT,
                    Book TEXT,
                    Chapter INTEGER,
                    Feedback TEXT
                )
                """)

    conn.commit()

    conn.close()

def generate_data():
    """Generate fake data. Use once."""
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    for i in range(1, 11):
        cur.execute("""INSERT INTO bblogtest (Bdate, Book, Chapter, Feedback) VALUES (?, ?, ?, ?)""",
                    (f"Bdate {i}", f"Book {i}", f"Chapter {i}", f"Feedback {i}"))

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '<a href="/list">LIST</a>'

@app.route('/about')
def about():
    fname="Ed"; lname="Farinholt"
    full_name = f"{fname} {lname}"
    render_template('about.html', full_name=full_name)

@app.route('/list')
def list():

    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    # Get lasted Blog Id of unedited Feedback
    sql1 = "SELECT MIN(Bid) FROM bblog2428 WHERE Feedback IS NULL ORDER BY Bid ASC"
    next_id = cur.execute(sql1).fetchone()[0]
    prev_id=next_id-1
    # Get the previously edited and remaining unedited records from the DB Table
    cur.execute("SELECT * FROM  bblog2428 WHERE Bid >= ?",(prev_id,))
    rows = cur.fetchall()

    conn.close()

    return render_template("list.html", rows=rows)
    #return render_template_string(template_list, rows=rows)


@app.route('/edit/<int:number>', methods=['GET', 'POST'])
def edit(number):

    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == 'POST':
        item_bid      = number
        item_bdate    = request.form['Bdate']
        item_book = request.form['Book']
        item_chapter  = request.form['Chapter']
        item_feedback = request.form['Feedback']

        cur.execute("UPDATE bblog2428 SET Bdate = ?, Book = ?, Chapter = ?, Feedback = ? WHERE Bid = ?",
                    (item_bdate, item_book, item_chapter, item_feedback, item_bid))
        conn.commit()

        return redirect('/list')

    cur.execute("SELECT * FROM bblog2428 WHERE Bid = ?", (number,))
    item = cur.fetchone()

    conn.close()

    return render_template("edit.html", item=item)
    #return render_template_string(template_edit, item=item)

@app.route('/delete/<int:number>')
def delete(number):

    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DELETE FROM bblog2428 WHERE Bid = ?", (number,))

    conn.commit()
    conn.close()

    return redirect('/list')

@app.route('/add', methods=['GET', 'POST'])
def add():

    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == 'POST':
        Title = "Bible Blog List"
        item_type    = request.form['Bdate']
        item_receipt = request.form['Book']
        item_amount  = request.form['Chapter']
        item_description = request.form['Feedback']

        cur.execute("""INSERT INTO bblog2428 (Bdate, Book, Chapter, Feedback) VALUES (?, ?, ?, ?)""",
                    (item_bdate, item_book, item_chapter, item_feedback))
        conn.commit()

        return redirect('/list', Title=Title) 

    return render_template("add.html", item=item)
    #return render_template_string(template_add)

template_list = """

"""

template_add = """

"""

template_edit = """

"""


if __name__ == '__main__':
    create_database()
    #generate_data()
    app.run(debug=True)
