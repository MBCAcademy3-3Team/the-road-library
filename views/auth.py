from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from LMS.common.session import Session
from LMS.service.MemberService import MemberService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if Session.is_login():
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        uid = request.form.get('uid', '').strip()
        pw = request.form.get('pw', '').strip()

        member = MemberService.find_by_uid_pw(uid, pw)

        if member is None:
            flash('아이디 또는 비밀번호가 올바르지 않습니다.', 'danger')
            return render_template('auth/login.html')

        if not member.active:
            flash('비활성화된 계정입니다. 관리자에게 문의하세요.', 'warning')
            return render_template('auth/login.html')

        Session.login(member)
        flash(f'{member.name}님, 환영합니다!', 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    Session.logout()
    flash('로그아웃 되었습니다.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/join', methods=['GET', 'POST'])
def join():
    if Session.is_login():
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        uid = request.form.get('uid', '').strip()
        pw = request.form.get('pw', '').strip()
        name = request.form.get('name', '').strip()

        if not uid or not pw or not name:
            flash('모든 항목을 입력해주세요.', 'danger')
            return render_template('auth/signup.html')

        if MemberService.is_uid_taken(uid):
            flash('이미 사용 중인 아이디입니다.', 'danger')
            return render_template('auth/signup.html')

        MemberService.create(uid, pw, name)
        flash('회원가입이 완료되었습니다. 로그인해주세요.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')


@auth_bp.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if not Session.is_login():
        flash('로그인 후 이용 가능합니다.', 'warning')
        return redirect(url_for('auth.login'))

    member = Session.get_login_member()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update':
            new_name = request.form.get('name', '').strip()
            new_pw = request.form.get('pw', '').strip()
            MemberService.update(member.id, new_name or member.name, new_pw or member.pw)
            # 세션 동기화
            session['user_name'] = new_name or member.name
            flash('정보가 수정되었습니다.', 'success')

        elif action == 'deactivate':
            MemberService.deactivate(member.id)
            Session.logout()
            flash('계정이 비활성화되었습니다.', 'info')
            return redirect(url_for('main.index'))

        return redirect(url_for('auth.mypage'))

    return render_template('auth/mypage.html', member=member)
