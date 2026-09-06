from flask import Blueprint, redirect, render_template, request, url_for
from myapp.models import Board, db

boards_bp = Blueprint('boards', __name__, template_folder='templates', url_prefix='/boards')
@boards_bp.route('/boards')
def boards():
    boards = Board.query.filter_by(removed_on=None).all()
    return render_template('boards/boards.html', boards=boards)

@boards_bp.route('/boards/<int:board_id>')
def board_detail(board_id):
    board = Board.query.get_or_404(board_id)
    return render_template('boards/boardDetail.html', board=board)

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