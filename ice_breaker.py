from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    print("Hello, Langchain!")
    print(os.environ.get("COOL_API_KEY"))
