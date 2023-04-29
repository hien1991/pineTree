from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from .utils import truncate_chat_history, stringify_history
import json


# We don't have to make it use that json format response, but it makes it easier to error-handle if it goes off-prompt
template = """
You are an AI designed to generate context-aware search phrases for querying a Pinecone vector database, as part of an AI Assistant \
project. You help retrieve long-term memories and uploaded files/documents by analyzing user inputs and chat history to deduce the best \
search phrases. With every user input (they can be questions, statements, anything), you will create search phrases, even if the history \
is unrelated. These database memories contain in the metadata categories that can help you find them, so keep that in mind when coming up \
with search queriess. Always format your response like this: {{\"search_phrase\": <insert search phrase>}}. Do not stray from this format \
or respond with any other response under any circumstance.
"""

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(template),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

def get_search_query(user_input, chat_history, openaiKey):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2, openai_api_key=openaiKey)
    memory = ConversationBufferMemory(return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

    reduced_chat_history = truncate_chat_history(chat_history, 3000)
    chat_history_string = stringify_history(reduced_chat_history)
    combined_input = chat_history_string + " | User Input: " + user_input

    # Example memories to help "train" the AI
    memory.save_context(
        {"input": "User: I just got the lease for my new apartment at Blue Village. | User Input: What is the pool policy?"},
        {"output": json.dumps({"search_phrase": "Blue Village apartment pool policy"})}
    )
    memory.save_context(
        {"input": "User: Yes, I believe you're right, George Washington is better! | AI: I'm glad you agree with me on George Washington. | User Input: How much caffeine did I say I drank?"},
        {"output": json.dumps({"search_phrase": "How much caffeine do I drink? Caffeine per day I drink."})}
    )
    memory.save_context(
        {"input": "User Input: Did we ever talk about tennis?"},
        {"output": json.dumps({"search_phrase": "tennis, sports"})}
    )
    memory.save_context(
        {"input": "User Input: How old am I?"},
        {"output": json.dumps({"search_phrase": "how old am I?, I'm x years old, personal info"})}
    )
    memory.save_context(
        {"input": "User: I have to go to work today.. I hate work | AI: I understand that work can be challenging sometimes. Let's talk about something more enjoyable, like video games. | User Input: I think Playstation is better than Xbox"},
        {"output": json.dumps({"search_phrase": "Playstation better than Xbox"})}
    )
    memory.save_context(
        {"input": "User: What are your recommendations for fast food? | AI: I recommend Whataburger's shake and fries | User Input: What are some other recommendations?"},
        {"output": json.dumps({"search_phrase": "Whataburger recommendations, fast food, shake and friess"})}
    )
    memory.save_context(
        {"input": "User: I love the Marvel shows on Netflix like Daredevil, Jessica Jones, Iron Fist, etc. | AI: Yes, the cancellation of the Marvel shows on Netflix was disappointing for many fans. However, Marvel has been releasing new content on Disney Plus such as WandaVision, The Falcon and The Winter Soldier, and Loki. | User Input: I'll give them a try, thanks! Any other recommendations?"},
        {"output": json.dumps({"search_phrase": "similar shows to Daredevil, Jessica Jones, Iron Fist on Disney Plus"})}
    )
    memory.save_context(
        {"input": "User: I'm thinking about traveling to Japan next year. | AI: Japan is a wonderful destination with a rich culture and history. Some popular cities to visit are Tokyo, Kyoto, and Osaka. | User Input: Can you recommend some must-visit places in Japan?"},
        {"output": json.dumps({"search_phrase": "must-visit places in Japan"})}
    )
    memory.save_context(
        {"input": "User: I need you to find an uploaded resume called myTestResume.docx and print the results in it's original format"},
        {"output": json.dumps({"search_phrase": "myTestResume.docx, resume"})}
    )

    try:
        response = conversation.predict(input=combined_input)
        search_phrase = json.loads(response)
        print("Returned search phrase: ", search_phrase["search_phrase"])
        return search_phrase["search_phrase"]
    except (json.JSONDecodeError, KeyError):
        print("Error: AI response is not in the expected format. Response: ", response)
        return user_input
