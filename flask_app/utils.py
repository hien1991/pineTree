from langchain.schema import HumanMessage
import os
import tiktoken

def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    return len(tokens)


def calculate_long_term_memory_tokens(longterm_memories):
    long_term_memories_text = " ".join([f"Source: ({item.get('source', '')}), date: {item.get('timestamp', '')}, context: {item.get('context', '')}" for item in longterm_memories])
    return count_tokens(long_term_memories_text)

def calculate_total_memory_tokens(input_text, short_term_memories, longterm_memories):
    long_term_memories_tokens = calculate_long_term_memory_tokens(longterm_memories)
    short_term_memories_text = stringify_history(short_term_memories)

    tokens_used = long_term_memories_tokens + count_tokens(short_term_memories_text) + count_tokens(input_text)
    return tokens_used

def get_readable_size(size: int, decimal_places: int = 2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

def get_file_size(temp_file_name: str):
    bytes_size = os.path.getsize(temp_file_name)
    file_size = get_readable_size(bytes_size)
    return file_size

def stringify_history(messages):
    formatted_messages = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            prefix = "User"
        else:
            prefix = "AI"
        content = f"{prefix}: {msg.content}"
        formatted_messages.append(content)
    return " | ".join(formatted_messages)

def truncate_chat_history(chat_history, char_limit=3000):
    truncated_history = []
    current_length = 0

    for msg in reversed(chat_history):
        if isinstance(msg, HumanMessage):
            prefix = "User"
        else:
            prefix = "AI"
        content = f"{prefix}: {msg.content}"
        
        if current_length + len(content) + 3 <= char_limit:
            truncated_history.insert(0, msg)
            current_length += len(content) + 3
        else:
            print("Token limit reached. Current history: ", truncated_history)
            break

    return truncated_history

