from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import (AIMessage, HumanMessage)
from langchain.prompts.chat import (
    ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate,
)
from .utils import truncate_chat_history, count_tokens


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

# Frontend sends stored key values via API call in __init__.py by calling this
def initializeChat(openai_api_key):
    global llm, conversation
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5, openai_api_key=openai_api_key)
    conversation = ConversationChain(llm=llm, prompt=prompt, memory=memory)


def chat(input_text, short_term_memories, longterm_memories):

    # Calculate total tokens in long-term memories, then available tokens for short term memories
    long_term_memories_text = " ".join([f"Source: ({item.get('source', '')}), date: {item.get('timestamp', '')}, context: {item.get('context', '')}" for item in longterm_memories])
    long_term_memories_tokens = count_tokens(long_term_memories_text)
    available_tokens = max_tokens - long_term_memories_tokens

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
    truncated_chat_history = truncate_chat_history(short_term_memories, available_tokens * 3)
    short_term_memories = [] # Re-build short term memories to copy truncated ones
    for msg in truncated_chat_history.split(" | "):
        if ": " in msg:
            prefix, content = msg.split(": ", 1)
            message_class = HumanMessage if prefix == "User" else AIMessage
            new_message = message_class(content=content)
            memory.chat_memory.messages.append(new_message)
            short_term_memories.append(new_message)


    memory.chat_memory.add_user_message(input_text)
    response = conversation.predict(input=input_text)

    # Update short-term memories with the new response
    short_term_memories.append(HumanMessage(content=input_text))
    short_term_memories.append(AIMessage(content=response))

    # Calculate available tokens left after appending all memories and user input
    tokens_used = count_tokens(truncated_chat_history) + count_tokens(input_text)
    tokens_left = available_tokens - tokens_used
    print("Tokens left after appending all memories and user input:", tokens_left)

    return response, short_term_memories
