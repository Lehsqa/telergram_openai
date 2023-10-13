import asyncio
from typing import Any, Dict, List

from langchain.chat_models import ChatOpenAI
from langchain.schema import LLMResult, HumanMessage
from langchain.callbacks.base import AsyncCallbackHandler


class AsyncHandler(AsyncCallbackHandler):
    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        await asyncio.sleep(0.3)

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        await asyncio.sleep(0.3)


class Chat:
    chat = ChatOpenAI(
        max_tokens=25,
        callbacks=[AsyncHandler()]
    )

    async def get_response(self, content: str) -> str:
        llm_result = await self.chat.agenerate([[HumanMessage(content=content)]])
        return llm_result.generations[0][0].text
