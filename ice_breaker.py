from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from third_party.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent


def ice_break_with(search_str: str) -> str:
    linkedin_username = linkedin_lookup_agent(search_str)
    linkedin_data = scrape_linkedin_profile(linkedin_username, mock=True)
    summary_template = """
              Given the information {information} about a person from I want you to create:
              1. a short summary
              2. two interesting facts about them
        """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )
    # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    # llm = ChatGoogleGenerativeAI(temperature=0, model='gemini-1.5-pro')
    # llm = ChatOllama(model="llama3.2", temperature=0)
    llm = ChatOllama(model="mistral", temperature=0)

    chain = summary_prompt_template | llm | StrOutputParser()
    res = chain.invoke(input={"information": linkedin_data})
    return res


if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter")
    res = ice_break_with("Rohit Mishra Bajaj Finance, EPAM")
    print(res)
