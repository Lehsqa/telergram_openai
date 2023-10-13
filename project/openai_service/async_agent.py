from langchain.agents import initialize_agent, load_tools, AgentType
from langchain.document_loaders import AssemblyAIAudioTranscriptLoader
from langchain.llms.openai import OpenAI


class Agent:
    llm = OpenAI(temperature=0)
    agent_chain = initialize_agent(
        tools=load_tools(["openweathermap-api"], llm),
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    async def get_response(self, content: str) -> str:
        return await self.agent_chain.arun(content)

    @staticmethod
    def get_transcribe(audio_file: str) -> str:
        loader = AssemblyAIAudioTranscriptLoader(file_path=audio_file)
        docs = loader.load()
        return docs[0].page_content
