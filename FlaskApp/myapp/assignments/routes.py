from flask import Blueprint, redirect, render_template, request, url_for
from myapp.models import  RoleAssignment, datetime, db, timezone

assignments_bp = Blueprint('assignments', __name__, template_folder='templates', url_prefix='/assignments')
@assignments_bp.route('/')
def assignments():
    assignments = RoleAssignment.query.filter_by(end_date=None).all()
    return render_template('assignments/assignments.html', assignments=assignments)

@assignments_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Handle form submission and create a new assignment
        # You can access form data using request.form.get('field_name')
        # Example: person_id = request.form.get('person_id')
        # Add your logic to create a new RoleAssignment here
        return redirect(url_for('assignments.assignments'))
    return render_template('assignments/create.html')

@assignments_bp.route('/edit/<int:assignment_id>', methods=['GET', 'POST'])
def edit(assignment_id):
    assignment = RoleAssignment.query.get_or_404(assignment_id)
    if request.method == 'POST':
        # Handle form submission and update the assignment
        # You can access form data using request.form.get('field_name')
        # Example: assignment.person_id = request.form.get('person_id')
        # Add your logic to update the RoleAssignment here
        db.session.commit()
        return redirect(url_for('assignments.assignments'))
    return render_template('assignments/edit.html', assignment=assignment)


@assignments_bp.route('/delete/<int:assignment_id>', methods=['GET', 'POST'])
def delete(assignment_id):
    assignment = RoleAssignment.query.get_or_404(assignment_id)
    if request.method == 'POST':
        # Handle form submission and delete the assignment
        # You can mark the assignment as removed or delete it from the database
        assignment.end_date = datetime.now(timezone.utc)  # Mark as removed
        db.session.commit()
        return redirect(url_for('assignments.assignments'))
    return render_template('assignments/delete.html', assignment=assignment)