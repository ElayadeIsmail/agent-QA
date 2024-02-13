from langchain.agents.openai_functions_agent.base import create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate,HumanMessagePromptTemplate,MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.agents import AgentExecutor,create_openai_functions_agent,BaseSingleActionAgent,OpenAIFunctionsAgent
from langchain.memory import ConversationBufferMemory

from dotenv import load_dotenv

from tools.sql import run_query_tool,list_tables,describe_table_tools
from tools.report import write_report_tool
from handlers.chat_model_start_handler import ChatModelStartHandler


load_dotenv()  # take environment variables from .env.

# Add This Handle Just t debug the messages sended to chatgpt
handler = ChatModelStartHandler()

chat = ChatOpenAI(
    # callbacks=[handler]
)

tables = list_tables()

prompt = ChatPromptTemplate(
    input_variables=["input"],
    messages=[
        SystemMessage(content=(
            "You are an AI that has access to a SQLITE database.\n"
            f"the database has tables of: {tables}\n"
            "Do not make any assumptions about what tables exist "
            "What columns exists. Instead use 'describe_tables' function"
        )),
         MessagesPlaceholder(variable_name="chat_history"),
         HumanMessagePromptTemplate.from_template("{input}"),
         MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)

tools = [run_query_tool,describe_table_tools,write_report_tool]

agent:OpenAIFunctionsAgent = create_openai_functions_agent(chat,tools,prompt)

agent_executor=AgentExecutor.from_agent_and_tools(agent=agent ,tools=tools,memory=memory)

while True:
    print("What Do You Wanna Know About Your Database?\n")
    content = input(">> ")
    result = agent_executor.invoke({"input": content})
    print(f"{result['output']}\n")
