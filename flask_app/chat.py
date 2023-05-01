from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import (AIMessage, HumanMessage)
from langchain.prompts.chat import (
    ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate,
)
from .utils import *


template = "You are a personal assistant AI. Your purpose is to help me by answering questions, providing recommendations, chatting, \
and assisting with tasks based on the context and information provided by the user. You should also use any relevant memories and \
context available to you. When you review the retrieved long term memories, they will come with the date the memory was given to you, a \
source field that tells you where the memory came from (ex: 'user input' means that the user told you this info in a previous chat, \
or 'uploaded' meaning the user uploaded a file). You acknowledge that your knowledge cutoff limits your knowledge of current events, \
so you will believe without question whatever I tell you"

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(template),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

# LLM and ConversationChain will be initialized with the keys passed from frontend
llm = None
memory = ConversationBufferMemory(return_messages=True)
conversation = None
max_tokens = 3500 # 4000 tokens available, you wanna save at least 500 for output


# Called upon load-up & when settings are saved. Frontend sends key values -> __init__.py -> here
def initializeChat(openai_api_key, useGpt4):
    global llm, conversation
    model_name = 'gpt-4' if useGpt4 else 'gpt-3.5-turbo'
    print("using model: ", model_name)
    llm = ChatOpenAI(model_name=model_name, temperature=0.5, openai_api_key=openai_api_key)
    conversation = ConversationChain(llm=llm, prompt=prompt, memory=memory)


def chat(input_text, short_term_memories, longterm_memories):

    # Count tokens in long-term memories in order to calculate # tokens we have left for short-term memories
    available_tokens = max_tokens - calculate_long_term_memory_tokens(longterm_memories)

    # Add long-term memories to the conversation
    memory.chat_memory.clear()
    memory.chat_memory.add_ai_message("These are my long term memories retrieved: ")
    for memory_item in longterm_memories:
        context, timestamp, source, filename = memory_item.values()
        filename_info = f", filename: {filename}" if filename is not None else ""
        memory.chat_memory.add_user_message(f"Source: ({source}){filename_info}, date: {timestamp}, context: {context}")

    memory.chat_memory.add_ai_message("I've received the mentioned memories. I'll use them as needed throughout our conversation to provide accurate and helpful information, keeping in mind that the user cannot see this message nor anything prior.")

    # Add short-term memories (chat history) after long term memories (db retrievals)
    # Truncating will cut off chat history where needed to make it fit 4000 token limit
    short_term_memories = truncate_chat_history(short_term_memories, available_tokens * 3)
    for msg in short_term_memories:
        if isinstance(msg, HumanMessage):
            memory.chat_memory.add_user_message(msg.content)
        elif isinstance(msg, AIMessage):
            memory.chat_memory.add_ai_message(msg.content)

    memory.chat_memory.add_user_message(input_text)
    response = conversation.predict(input=input_text) # AI response

    # Update short-term memories with the new response
    short_term_memories.append(HumanMessage(content=input_text))
    short_term_memories.append(AIMessage(content=response))

    # Calculate available tokens left after appending all memories and user input
    available_tokens = max_tokens - calculate_total_memory_tokens(input_text, short_term_memories, longterm_memories)
    print("Remaining tokens (saving 500 for output): ", available_tokens, " / ", max_tokens)

    return response, short_term_memories
