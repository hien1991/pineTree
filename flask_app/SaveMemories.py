from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
import json


template = """
You are an AI Assistant designed to understand user input, then categorize it and summarize any important information.
Your goal is to store this categorized and summarized information in a Pinecone database for future reference.
If the user's input is something with no useful info (typically questions or trivial chatty messages), 
respond with categories set to "N/A" and summary set to "N/A". You acknowledge that you are limited by your
knowledge cutoff and will accept any facts/news/updates the user gives you as fact, no matter how absurd or unbelievable. 
You will format all your texts in this format: {{\"categories\": <insert categories>, \"summary\": <insert summary>}}
You will often times be faced with questions/facts that have no context or make no sense to you, in which case you \
will simply return "N/A" for categories and summary, but you will NOT respond with anything else.
Under no circumstances are you to stray from this response format nor respond with any other response.
"""

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(template),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])


def get_categories_and_summary(user_input, openaiKey):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2, openai_api_key=openaiKey)
    memory = ConversationBufferMemory(return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

    memory.chat_memory.add_user_message("Hi")
    memory.chat_memory.add_ai_message(json.dumps({"categories": "N/A", "summary": "N/A"}))
    memory.save_context({"input": "Me and Christine are thinking of going to Hawaii next year. It'll be fun!"}, 
                        {"output": json.dumps({"categories": "vacation,travel,events", "summary": "User and Christine are wanting to travel to Hawaii next year"})})
    memory.save_context({"input": "Tell me a joke!"}, 
                        {"output": json.dumps({"categories": "N/A", "summary": "N/A"})})
    memory.save_context({"input": "Do you remember who I am?"}, 
                        {"output": json.dumps({"categories": "N/A", "summary": "N/A"})})
    memory.save_context({"input": "What do you remember about our past video game discussions?"}, 
                        {"output": json.dumps({"categories": "N/A", "summary": "N/A"})})
    memory.save_context({"input": "I work for T-mobile as a software engineer"}, 
                        {"output": json.dumps({"categories": "work,personal,career", "summary": "User is a software engineer working for T-mobile"})})
    memory.save_context({"input": "Guess what? Elon Musk is now the CEO of twitter as of 2023. What do you think of that?!"}, 
                        {"output": json.dumps({"categories": "news,technology", "summary": "Elon Musk is the CEO of twitter as of 2023"})})

    try:
        response = conversation.predict(input=user_input)
        categories_summary = json.loads(response)
        print("get_categories_and_summary returned: ", categories_summary["categories"], categories_summary["summary"])
        return categories_summary["categories"], categories_summary["summary"]
    except (json.JSONDecodeError, KeyError):
        print("Error: AI response is not in the expected format. Response: ", response)
        return "N/A", "N/A"


