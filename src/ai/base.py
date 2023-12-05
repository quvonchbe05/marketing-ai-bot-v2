from src.config import OPENAI_API_KEY
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain.schema import HumanMessage, AIMessage
from src.ai.prompt import prompt_text
from langchain.tools import format_tool_to_openai_function
from src.db.database import async_session_maker
from src.db.models import ChatHistoryModel
from sqlalchemy import select, insert, update
import asyncio
from datetime import datetime


class Base:
    def __init__(
            self,
            openai_api_key=OPENAI_API_KEY,
            model="gpt-3.5-turbo",
            temperature=0.7,
            tools=None,
            prompt=prompt_text,
            user=None
    ) -> None:
        self.openai_api_key = openai_api_key
        self.tools = tools or []
        self.model = model
        self.temperature = temperature
        self.prompt = prompt
        self.user = user

    @staticmethod
    def convert_conversation_to_json(history):
        serialized = []
        for msg in history:
            if isinstance(msg, HumanMessage):
                serialized.append({
                    "role": "HumanMessage",
                    "content": msg.content,
                    'date': datetime.now().isoformat()
                })
            elif isinstance(msg, AIMessage):
                serialized.append({
                    "role": "AIMessage",
                    "content": msg.content,
                    'date': datetime.now().isoformat()
                })
        return serialized

    @staticmethod
    def convert_json_to_memory(data):
        serialized = []
        for msg in data:
            if msg['role'] == "HumanMessage":
                serialized.append(HumanMessage(content=msg["content"]))
            elif msg['role'] == "AIMessage":
                serialized.append(AIMessage(content=msg["content"]))
        return serialized

    @staticmethod
    async def get_chat_history(user):
        async with async_session_maker() as session:
            history = await session.scalar(
                select(ChatHistoryModel).where(
                    ChatHistoryModel.user_id == str(user)
                )
            )
            if history:
                history = history.content
            else:
                history = []

        return history

    @staticmethod
    async def create_or_update_history(user, content):
        async with async_session_maker() as session:
            user_db = await session.scalar(
                select(ChatHistoryModel).where(
                    ChatHistoryModel.user_id == str(user)
                )
            )
            if user_db:
                await session.execute(
                    update(ChatHistoryModel).values(content=content).where(ChatHistoryModel.user_id == str(user))
                )
                response_id = user
            else:
                await session.execute(
                    insert(ChatHistoryModel).values(user_id=user, content=content)
                )
                response_id = user

            await session.commit()
        return response_id

    async def create_llm(self):
        llm = ChatOpenAI(
            openai_api_key=self.openai_api_key,
            model=self.model,
            temperature=self.temperature,
        )

        return llm

    async def create_prompt(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        return prompt

    async def create_memory(self):
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        if self.user:
            converted_history = self.convert_json_to_memory(
                await self.get_chat_history(user=self.user)
            )
            for obj in converted_history:
                memory.buffer.append(obj)

            return memory

        return memory

    async def create_tools(self):
        llm = ChatOpenAI(
            openai_api_key=self.openai_api_key,
            model=self.model,
            temperature=self.temperature,
        )
        llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in self.tools])
        return llm_with_tools

    async def create_agent(self):
        agent = (
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_functions(
                        x["intermediate_steps"]
                    ),
                    "chat_history": lambda x: x["chat_history"],
                }
                | await self.create_prompt()
                | await self.create_tools()
                | OpenAIFunctionsAgentOutputParser()
        )

        agent_executor = AgentExecutor(
            agent=agent, tools=self.tools, memory=await self.create_memory(), verbose=True
        )

        return agent_executor

    async def send_message(self, message):
        agent = await self.create_agent()
        res = agent.invoke({"input": message})
        user = await self.create_or_update_history(self.user, self.convert_conversation_to_json((res['chat_history'])))
        return {
            'answer': res['output']
        }
