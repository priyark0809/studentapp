from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'

db = SQLAlchemy(app)


# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    major = db.Column(db.String(50), nullable=False)



# Initialize the database
with app.app_context():
    db.create_all()


# Route to display all students
@app.route('/', methods=['GET'])
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)


# Route to render the 'Add Student' form
@app.route('/add-student')
def add_student():
    return render_template('add_student.html')


# Route to handle student creation
@app.route('/submit-student', methods=['POST'])
def create_student():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    major = request.form['major']


    new_student = Student(name=name, email=email, age=age, major=major)
    db.session.add(new_student)

    try:
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An error occurred while adding the student: {e}'}), 500


# Route to delete a student by ID
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)

    if not student:
        return jsonify({'message': 'Student not found'}), 404

    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An error occurred while deleting the student: {e}'}), 500


# Route to update student details
@app.route('/update-student/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.age = request.form['age']
        student.major = request.form['major']

        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            return f'There was an issue updating the student: {e}'

    return render_template('update_student.html', student=student)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)
