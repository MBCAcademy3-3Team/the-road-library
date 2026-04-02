# src/repository/member_repository.py
from typing import Optional
from src.common.db import fetch_query, execute_query
from src.domain.member import Member


class MemberRepository:

    # ────────────────────────────────────────
    # 단건 조회
    # ────────────────────────────────────────
    def find_by_uid(self, uid: str) -> Optional[Member]:
        row = fetch_query(
            "SELECT * FROM members WHERE uid = %s",
            (uid,), one=True
        )
        return Member.from_db(row) if row else None

    def find_by_id(self, member_id: int) -> Optional[Member]:
        row = fetch_query(
            "SELECT * FROM members WHERE id = %s",
            (member_id,), one=True
        )
        return Member.from_db(row) if row else None

    # ────────────────────────────────────────
    # 중복 확인
    # ────────────────────────────────────────
    def exists_by_uid(self, uid: str) -> bool:
        row = fetch_query(
            "SELECT id FROM members WHERE uid = %s",
            (uid,), one=True
        )
        return row is not None

    # ────────────────────────────────────────
    # 생성
    # ────────────────────────────────────────
    def create(
        self,
        uid: str,
        password: str,
        name: str,
        nickname: str,
        birthdate: str,         # 'YYYY-MM-DD' 형식
    ) -> int:
        execute_query(
            "INSERT INTO members (uid, password, name, nickname, birthdate) "
            "VALUES (%s, %s, %s, %s, %s)",
            (uid, password, name, nickname, birthdate)
        )
        row = fetch_query("SELECT LAST_INSERT_ID() AS new_id", one=True)
        return row['new_id'] if row else -1

    def update_profile_img(self, member_id: int, file_url: str):
        """프로필 이미지 URL 업데이트"""
        execute_query(
            "UPDATE members SET profile_img = %s WHERE id = %s",
            (file_url, member_id)
        )