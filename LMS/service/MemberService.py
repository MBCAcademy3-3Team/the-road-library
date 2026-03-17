from LMS.common.db import fetch_query, execute_query
from LMS.domain.Member import Member


class MemberService:

    @staticmethod
    def find_by_uid_pw(uid: str, pw: str) -> Member | None:
        """로그인: uid + password 일치 여부 확인"""
        row = fetch_query(
            "SELECT * FROM members WHERE uid = %s AND password = %s",
            (uid, pw),
            one=True,
        )
        return Member.from_db(row) if row else None

    @staticmethod
    def find_by_id(member_id: int) -> Member | None:
        row = fetch_query("SELECT * FROM members WHERE id = %s", (member_id,), one=True)
        return Member.from_db(row) if row else None

    @staticmethod
    def is_uid_taken(uid: str) -> bool:
        """아이디 중복 확인"""
        row = fetch_query("SELECT id FROM members WHERE uid = %s", (uid,), one=True)
        return row is not None

    @staticmethod
    def create(uid: str, pw: str, name: str) -> int:
        """회원가입"""
        return execute_query(
            "INSERT INTO members (uid, password, name) VALUES (%s, %s, %s)",
            (uid, pw, name),
        )

    @staticmethod
    def update(member_id: int, name: str, pw: str) -> None:
        """회원 정보 수정"""
        execute_query(
            "UPDATE members SET name = %s, password = %s WHERE id = %s",
            (name, pw, member_id),
        )

    @staticmethod
    def deactivate(member_id: int) -> None:
        """계정 비활성화"""
        execute_query(
            "UPDATE members SET active = FALSE WHERE id = %s",
            (member_id,),
        )

    @staticmethod
    def delete(member_id: int) -> None:
        """회원 완전 삭제"""
        execute_query("DELETE FROM members WHERE id = %s", (member_id,))
