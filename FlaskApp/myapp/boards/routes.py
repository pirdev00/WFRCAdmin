from flask import Blueprint, redirect, render_template, request, send_file, url_for
from FlaskApp.myapp.documents.generators import generate_roster_docx
from myapp.models import Board, db, timezone
from datetime import datetime

boards_bp = Blueprint('boards', __name__, template_folder='templates', url_prefix='/boards')
@boards_bp.route('/boards')
def boards():
    boards = Board.query.filter_by(removed_on=None).all()
    return render_template('boards/boards.html', boards=boards)

@boards_bp.route('/boards/<int:board_id>')
def board_detail(board_id):
    board = Board.query.get_or_404(board_id)
    assignments = [a for a in board.role_assignments if a.end_date is None]
    
    return render_template('boards/boardDetail.html', board=board, assignments=assignments)

@boards_bp.route('/boards/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        board = Board(name=name)
        db.session.add(board)
        db.session.commit()
        return redirect(url_for('boards.boards'))
        pass
    return render_template('boards/create.html')   

@boards_bp.route('/boards/<int:board_id>/edit', methods=['GET', 'POST'])
def edit(board_id):
    board = Board.query.get_or_404(board_id)
    if request.method == 'POST':
        board.name = request.form.get('name')
        db.session.commit()
        return redirect(url_for('boards.board_detail', board_id=board.id))
    return render_template('boards/edit.html', board=board)

@boards_bp.route('/boards/<int:board_id>/delete', methods=['GET', 'POST'])
def delete(board_id):
    board = Board.query.get_or_404(board_id)
    if request.method == 'POST':
        board.removed_on = datetime.now(timezone.utc)
        db.session.commit()
        for assignment in board.role_assignments:
            assignment.end_date = datetime.now(timezone.utc)
            db.session.commit()
        return redirect(url_for('boards.boards'))
    return render_template('boards/delete.html', board=board)


@boards_bp.route('/<int:board_id>/roster.docx')
def download_roster(board_id):
    board = Board.query.get_or_404(board_id)
    buf = generate_roster_docx(board)
    return send_file(
        buf,
        as_attachment=True,
        download_name=f'{board.name}_roster.docx',
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )