from flask import session as flask_session
from LMS.domain.Member import Member


class Session:
    """Flask session을 래핑한 로그인 상태 관리 클래스"""

    @classmethod
    def is_login(cls) -> bool:
        return 'user_id' in flask_session

    @classmethod
    def login(cls, member: Member):
        flask_session['user_id'] = member.id
        flask_session['user_uid'] = member.uid
        flask_session['user_name'] = member.name
        flask_session['user_role'] = member.role

    @classmethod
    def logout(cls):
        flask_session.clear()

    @classmethod
    def get_login_member(cls) -> Member | None:
        if not cls.is_login():
            return None
        return Member(
            id=flask_session.get('user_id'),
            uid=flask_session.get('user_uid'),
            pw=None,
            name=flask_session.get('user_name'),
            role=flask_session.get('user_role'),
        )
