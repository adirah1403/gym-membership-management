from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Connection Setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sqlplus#123",
    database="gym_management"
)
cursor = db.cursor()

# Home Page Route
@app.route('/')
def home():
    return render_template('home.html')  

# Register a New Member
@app.route('/register', methods=['GET', 'POST'])
def register_member():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        contact_no = request.form['contact_no']
        email = request.form['email']
        address = request.form['address']
        duration = int(request.form['membership_duration'])
        
        
        monthly_fee = 2000  
        total_bill = duration * monthly_fee
        
        cursor.execute("INSERT INTO members (name, age, contact_no, email, address, membership_start_date, membership_duration, total_bill) VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s)", 
                       (name, age, contact_no, email, address, duration, total_bill))
        db.commit()
        return redirect(url_for('view_all_members'))
    
    return render_template('register.html')

# View All Members
@app.route('/members')
def view_all_members():
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    return render_template('view_members.html', members=members)

# Search Members by Name Only
@app.route('/search', methods=['GET'])
def search_members():
    query = request.args.get('query')
    cursor.execute("SELECT * FROM members WHERE name LIKE %s", 
                   (f'%{query}%',))  
    members = cursor.fetchall()
    return render_template('search.html', members=members)

# Update Member
@app.route('/update/<int:member_id>', methods=['GET', 'POST'])
def update_member(member_id):
    cursor.execute("SELECT * FROM members WHERE member_id = %s", (member_id,))
    member = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        contact_no = request.form['contact_no']
        email = request.form['email']
        address = request.form['address']
        duration = int(request.form['membership_duration'])

        monthly_fee = 2000
        total_bill = duration * monthly_fee

        cursor.execute("""UPDATE members SET name = %s, age = %s, contact_no = %s, email = %s, 
                          address = %s, membership_duration = %s, total_bill = %s WHERE member_id = %s""",
                       (name, age, contact_no, email, address, duration, total_bill, member_id))
        db.commit()

        return redirect(url_for('view_all_members'))
    
    return render_template('update_member.html', member=member)

# Delete Member
@app.route('/delete/<int:member_id>')
def delete_member(member_id):
    cursor.execute("DELETE FROM members WHERE member_id = %s", (member_id,))
    db.commit()
    return redirect(url_for('view_all_members'))

if __name__ == '__main__':
    app.run(debug=True)
