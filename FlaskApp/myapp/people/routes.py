from flask import Blueprint, redirect, render_template, request, url_for
from myapp.models import Person, db

people_bp = Blueprint('people', __name__, template_folder='templates', url_prefix='/people')
@people_bp.route('/people')
def people():
    people = Person.query.filter_by(removed_on=None).all()
    return render_template('people/people.html', people=people)


@people_bp.route('/people/<int:person_id>')
def person_detail(person_id):
    person = Person.query.get_or_404(person_id)
    return render_template('people/personDetail.html', person=person)

@people_bp.route('/people/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        honorific_title = request.form.get('honorific_title')
        email = request.form.get('email')
        phone = request.form.get('phone')
        person = Person(first_name=first_name, last_name=last_name, honorific_title=honorific_title, email=email, phone=phone)
        db.session.add(person)
        db.session.commit()
        return redirect(url_for('people.people'))
    return render_template('people/create.html')

@people_bp.route('/people/edit', methods=['GET', 'POST'])
def edit(person_id):
    return render_template('people/edit.html', person_id=person_id)

@people_bp.route('/people/delete', methods=['GET', 'POST'])
def delete(person_id):
    return render_template('people/delete.html', person_id=person_id)   

