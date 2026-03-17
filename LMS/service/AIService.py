import os

from anthropic import Anthropic

_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

_SYSTEM_PROMPT = """당신은 '도(道)서관'의 도로 안전 전문 AI 어시스턴트입니다.
운전자들이 더 안전하게 도로를 이용할 수 있도록 돕는 것이 목표입니다.

다음 주제에 대해 전문적으로 안내해주세요:
- 교통 법규 및 도로교통법 해석
- 사고 다발 구역의 위험 요소 분석
- 날씨·시간대별 안전 운전 팁
- 방어 운전 기술 및 긴급 상황 대처법
- 블랙박스 영상 속 상황 분석
- 차량 정비 및 안전 점검 항목

항상 한국어로 친절하고 명확하게 답변해주세요.
답변은 간결하게 핵심을 전달하되, 필요한 경우 단계별로 설명해주세요."""


class AIService:

    @staticmethod
    def ask(question: str, history: list = None) -> str:
        """
        도로 안전 AI에게 질문을 보내고 답변을 반환합니다.

        :param question: 사용자 질문
        :param history: 이전 대화 내역 [{"role": "user"|"assistant", "content": "..."}]
        :return: AI 답변 문자열
        """
        messages = list(history) if history else []
        messages.append({"role": "user", "content": question})

        response = _client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=_SYSTEM_PROMPT,
            messages=messages,
        )

        return response.content[0].text
