from dotenv import load_dotenv

load_dotenv()
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.tools import get_profile_url_tavily


def lookup(name: str) -> str:
    llm = ChatOllama(model="mistral", temperature=0)
    template = """
    given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page. Your answer should contain only a URL
    """

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tool_for_agent = [
        Tool(
            name="Crawl Google for linked profile page",
            func=get_profile_url_tavily,
            description="userful for when you need to get the Linkedin Page URL",
        )
    ]
    react_prompt = hub.pull("hwchase17/react")

    """
    https://smith.langchain.com/hub/hwchase17/react
    react_prompt: This react prompt is defined as
    ============================================
    Answer the following questions as best you can. You have access to the following tools:
    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!
    
    Question: {input}
    Thought:{agent_scratchpad}
    """
    agent = create_react_agent(llm=llm, tools=tool_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tool_for_agent, verbose=True)
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    linked_profile_url = result["output"]
    return linked_profile_url


if __name__ == "__main__":
    linkedin_url = lookup(name="Ankit Verma Nagarro EPAM")
    print(linkedin_url)
