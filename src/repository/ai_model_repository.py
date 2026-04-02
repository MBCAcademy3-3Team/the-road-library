# src/repository/ai_model_repository.py
from src.common.db import execute_query


class AIModelRepository:

    def save_result(
        self,
        user_id: int,
        result_url: str,
        boar_count: int,
        water_deer_count: int,
        racoon_count: int,
    ):
        """AI 분석 결과 DB 저장"""
        execute_query(
            """
            INSERT INTO ai_analysis
            (user_id, filename, boar_count, water_deer_count, racoon_count, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            """,
            (user_id, result_url, boar_count, water_deer_count, racoon_count)
        )