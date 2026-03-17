from flask import Blueprint, render_template, request, redirect, url_for, flash

from LMS.common.session import Session
from LMS.service.BoardService import BoardService

board_bp = Blueprint('board', __name__)


@board_bp.route('/')
def list_board():
    boards = BoardService.get_boards()
    return render_template('board/list.html', boards=boards)


@board_bp.route('/write', methods=['GET', 'POST'])
def write():
    if not Session.is_login():
        flash('로그인 후 이용 가능합니다.', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        member = Session.get_login_member()

        if not title or not content:
            flash('제목과 내용을 입력해주세요.', 'danger')
            return render_template('board/write.html')

        BoardService.create_board(member.id, title, content)
        flash('게시글이 등록되었습니다.', 'success')
        return redirect(url_for('board.list_board'))

    return render_template('board/write.html')


@board_bp.route('/<int:board_id>')
def detail(board_id):
    board = BoardService.get_board(board_id)
    if not board:
        flash('존재하지 않는 게시글입니다.', 'danger')
        return redirect(url_for('board.list_board'))
    return render_template('board/detail.html', board=board)


@board_bp.route('/<int:board_id>/edit', methods=['GET', 'POST'])
def edit(board_id):
    if not Session.is_login():
        flash('로그인 후 이용 가능합니다.', 'warning')
        return redirect(url_for('auth.login'))

    board = BoardService.get_board(board_id)
    if not board:
        flash('존재하지 않는 게시글입니다.', 'danger')
        return redirect(url_for('board.list_board'))

    member = Session.get_login_member()
    if board['member_id'] != member.id and not member.is_admin():
        flash('수정 권한이 없습니다.', 'danger')
        return redirect(url_for('board.detail', board_id=board_id))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not content:
            flash('제목과 내용을 입력해주세요.', 'danger')
            return render_template('board/write.html', board=board, edit=True)

        BoardService.update_board(board_id, title, content)
        flash('게시글이 수정되었습니다.', 'success')
        return redirect(url_for('board.detail', board_id=board_id))

    return render_template('board/write.html', board=board, edit=True)


@board_bp.route('/<int:board_id>/delete', methods=['POST'])
def delete(board_id):
    if not Session.is_login():
        flash('로그인 후 이용 가능합니다.', 'warning')
        return redirect(url_for('auth.login'))

    board = BoardService.get_board(board_id)
    member = Session.get_login_member()

    if board and (board['member_id'] == member.id or member.is_admin()):
        BoardService.delete_board(board_id)
        flash('게시글이 삭제되었습니다.', 'success')
    else:
        flash('삭제 권한이 없습니다.', 'danger')

    return redirect(url_for('board.list_board'))
