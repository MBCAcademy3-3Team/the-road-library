from flask import Blueprint, render_template, request, redirect, url_for, flash

from LMS.common.session import Session
from LMS.service.PostService import PostService

post_bp = Blueprint('post', __name__)


@post_bp.route('/')
def list_post():
    posts = PostService.get_posts()
    return render_template('post/list.html', posts=posts)


@post_bp.route('/write', methods=['GET', 'POST'])
def write():
    if not Session.is_login():
        flash('로그인 후 이용 가능합니다.', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        files = request.files.getlist('files')
        member = Session.get_login_member()

        if not title or not content:
            flash('제목과 내용을 입력해주세요.', 'danger')
            return render_template('post/write.html')

        PostService.save_post(member.id, title, content, files)
        flash('자료가 등록되었습니다.', 'success')
        return redirect(url_for('post.list_post'))

    return render_template('post/write.html')


@post_bp.route('/<int:post_id>')
def detail(post_id):
    post, files = PostService.get_post_detail(post_id)
    if not post:
        flash('존재하지 않는 자료입니다.', 'danger')
        return redirect(url_for('post.list_post'))
    return render_template('post/detail.html', post=post, files=files)


@post_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
def edit(post_id):
    if not Session.is_login():
        flash('로그인 후 이용 가능합니다.', 'warning')
        return redirect(url_for('auth.login'))

    post, files = PostService.get_post_detail(post_id)
    if not post:
        flash('존재하지 않는 자료입니다.', 'danger')
        return redirect(url_for('post.list_post'))

    member = Session.get_login_member()
    if post['member_id'] != member.id and not member.is_admin():
        flash('수정 권한이 없습니다.', 'danger')
        return redirect(url_for('post.detail', post_id=post_id))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        new_files = request.files.getlist('files')

        PostService.update_post(post_id, title, content, new_files)
        flash('자료가 수정되었습니다.', 'success')
        return redirect(url_for('post.detail', post_id=post_id))

    return render_template('post/write.html', post=post, files=files, edit=True)


@post_bp.route('/<int:post_id>/delete', methods=['POST'])
def delete(post_id):
    if not Session.is_login():
        flash('로그인 후 이용 가능합니다.', 'warning')
        return redirect(url_for('auth.login'))

    post, _ = PostService.get_post_detail(post_id)
    member = Session.get_login_member()

    if post and (post['member_id'] == member.id or member.is_admin()):
        PostService.delete_post(post_id)
        flash('자료가 삭제되었습니다.', 'success')
    else:
        flash('삭제 권한이 없습니다.', 'danger')

    return redirect(url_for('post.list_post'))
