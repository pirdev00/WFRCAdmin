from flask import Blueprint, redirect, render_template, request, url_for
from myapp.models import Board, Person, datetime, db, timezone, RoleAssignment

people_bp = Blueprint('people', __name__, template_folder='templates', url_prefix='/people')
@people_bp.route('/')
def people():
    people = Person.query.filter_by(removed_on=None).all()
    return render_template('people/people.html', people=people)


@people_bp.route('/<int:person_id>')
def person_detail(person_id):
    person = Person.query.get_or_404(person_id)
    return render_template('people/personDetail.html', person=person)

@people_bp.route('/create', methods=['GET', 'POST'])
def create():
    boards = Board.query.filter_by(removed_on=None).all()  # Fetch all boards to display in the form
    if request.method == 'POST':
        db.session.commit()
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        honorific_title = request.form.get('honorific_title')
        email = request.form.get('email')
        phone = request.form.get('phone')
        person = Person(first_name=first_name, last_name=last_name, honorific_title=honorific_title, email=email, phone=phone)
        db.session.add(person)
        db.session.commit()
        for board_id in request.form.getlist('boards'):
            assignment = RoleAssignment(person_id=person.id, board_id=int(board_id), role_type_id=5, start_date=datetime.now(timezone.utc))
            db.session.add(assignment)
        db.session.commit()
        return redirect(url_for('people.people'))
    return render_template('people/create.html', allboards=boards) 

@people_bp.route('/edit/<int:person_id>/<int:board_id>', methods=['GET', 'POST'])
def edit(person_id, board_id):
    person = Person.query.get_or_404(person_id)
    board = Board.query.get_or_404(board_id)
    if request.method == 'POST':
        person.first_name = request.form.get('firstName')
        person.last_name = request.form.get('lastName')
        person.honorific_title = request.form.get('honorific')
        person.email = request.form.get('email')
        person.phone = request.form.get('phone')
        db.session.commit()
        return redirect(url_for('boards.board_detail', board_id=board_id))
    return render_template('people/edit.html', person=person, board=board)

@people_bp.route('/delete/<int:person_id>/<int:board_id>', methods=['GET', 'POST'])
def delete(person_id, board_id):
    person = Person.query.get_or_404(person_id)
    board = Board.query.get_or_404(board_id)
    assignment = RoleAssignment.query.filter_by(person_id=person_id, board_id=board_id, end_date=None).first()
    if not assignment:
        return "Assignment not found", 404
    if request.method == 'POST':
        person.removed_on = datetime.now(timezone.utc)
        assignment.end_date = datetime.now(timezone.utc)
        db.session.commit()
        return redirect(url_for('boards.board_detail', board_id=board_id))
    
    return render_template('people/delete.html', person=person, board=board)   

@people_bp.route('/editCard/<int:person_id>', methods=['GET', 'POST'])
def edit_card(person_id):
    person = Person.query.get_or_404(person_id)
    boards = Board.query.filter_by(removed_on=None).all()  # Fetch all boards to display in the form
    assignmentBoardIds = [assignment.board_id for assignment in person.role_assignments if assignment.end_date is None]

    if request.method == 'POST':
        boardList = request.form.getlist('boards')  # Get the list of selected board IDs from the form
        for board in boardList:
            if board in assignmentBoardIds:
                continue  # Skip if the assignment already exists
            else:
                new_assignment = RoleAssignment(
                    person_id=person.id,
                    board_id=int(board),
                    role_type_id=5,  # Default role type, adjust as needed
                    start_date=datetime.now(timezone.utc)
                )
                db.session.add(new_assignment)
        person.first_name = request.form.get('firstName')
        person.last_name = request.form.get('lastName')
        person.honorific_title = request.form.get('honorific')
        person.email = request.form.get('email')
        person.phone = request.form.get('phone')
        db.session.commit()
        return redirect(url_for('people.people'))
    return render_template('people/edit_Card.html', person=person, boards=boards, assignmentBoardIds=assignmentBoardIds)

@people_bp.route('/deleteCard/<int:person_id>', methods=['GET', 'POST'])
def delete_card(person_id):
    person = Person.query.get_or_404(person_id)
    assignments = RoleAssignment.query.filter_by(person_id=person_id, end_date=None).all()
    if request.method == 'POST':
        person.removed_on = datetime.now(timezone.utc)
        db.session.add(person)
        for assignment in assignments:
            assignment.end_date = datetime.now(timezone.utc)  # Mark each assignment as removed
            db.session.add(assignment)
        db.session.commit()
        return redirect(url_for('people.people'))
    return render_template('people/delete_Card.html', person=person)