from LMS.common.db import fetch_query, execute_query


class BoardService:

    @staticmethod
    def get_boards():
        """전체 게시글 목록 (작성자 JOIN)"""
        sql = """
            SELECT b.*, m.name AS writer_name
            FROM boards b
            JOIN members m ON b.member_id = m.id
            WHERE b.active = TRUE
            ORDER BY b.id DESC
        """
        return fetch_query(sql)

    @staticmethod
    def get_board(board_id: int):
        """게시글 단건 조회 + 조회수 증가"""
        execute_query(
            "UPDATE boards SET visits = visits + 1 WHERE id = %s",
            (board_id,),
        )
        sql = """
            SELECT b.*, m.name AS writer_name
            FROM boards b
            JOIN members m ON b.member_id = m.id
            WHERE b.id = %s AND b.active = TRUE
        """
        return fetch_query(sql, (board_id,), one=True)

    @staticmethod
    def create_board(member_id: int, title: str, content: str) -> int:
        """게시글 작성"""
        return execute_query(
            "INSERT INTO boards (member_id, title, content) VALUES (%s, %s, %s)",
            (member_id, title, content),
        )

    @staticmethod
    def update_board(board_id: int, title: str, content: str) -> None:
        """게시글 수정"""
        execute_query(
            "UPDATE boards SET title = %s, content = %s WHERE id = %s",
            (title, content, board_id),
        )

    @staticmethod
    def delete_board(board_id: int) -> None:
        """게시글 소프트 삭제"""
        execute_query(
            "UPDATE boards SET active = FALSE WHERE id = %s",
            (board_id,),
        )
