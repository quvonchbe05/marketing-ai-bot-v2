from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.tools import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor
from src.ai.prompt import prompt_text
from src.ai.tools import search_from_documents
from langchain.schema import AIMessage, HumanMessage
from src.config import OPENAI_API_KEY
from datetime import datetime


class Base:
    def __init__(
        self,
        openai_api_key: str = None,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        tools: list = [],
        prompt: str = None,
    ) -> None:
        self.openai_api_key = openai_api_key
        self.tools = tools
        self.model = model
        self.temperature = temperature
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

    async def create_tools(self):
        llm = ChatOpenAI(
            openai_api_key=self.openai_api_key,
            model=self.model,
            temperature=self.temperature,
        )
        llm_with_tools = llm.bind(
            functions=[format_tool_to_openai_function(t) for t in self.tools]
        )
        return llm_with_tools

    async def create_agent(self):
        agent_schema = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_functions(
                    x["intermediate_steps"]
                ),
                "chat_history": lambda x: x["chat_history"],
            }
            | self.prompt
            | await self.create_tools()
            | OpenAIFunctionsAgentOutputParser()
        )

        agent_executor = AgentExecutor(
            agent=agent_schema,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
        )

        return agent_executor

    async def get_history(self):
        return self.memory.buffer
    
    async def set_history(self, history):
        for obj in history:
            self.memory.buffer.append(obj)

    @staticmethod
    def convert_conversation_to_json(history):
        serialized = []
        for msg in history:
            if isinstance(msg, HumanMessage):
                serialized.append(
                    {
                        "role": "HumanMessage",
                        "content": msg.content,
                        "date": datetime.now().isoformat(),
                    }
                )
            elif isinstance(msg, AIMessage):
                serialized.append(
                    {
                        "role": "AIMessage",
                        "content": msg.content,
                        "date": datetime.now().isoformat(),
                    }
                )
        return serialized

    @staticmethod
    def convert_json_to_memory(data):
        serialized = []
        for msg in data:
            if msg["role"] == "HumanMessage":
                serialized.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "AIMessage":
                serialized.append(AIMessage(content=msg["content"]))
        return serialized

    async def send_message(self, message):
        agent = await self.create_agent()
        response = agent.invoke({"input": message})

        return response["output"]


class MarketingAIBot(Base):
    def __init__(self):
        super().__init__(
            OPENAI_API_KEY, "gpt-3.5-turbo", 0.7, [search_from_documents], prompt_text
        )
