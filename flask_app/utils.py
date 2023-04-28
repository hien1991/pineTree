from langchain.schema import HumanMessage
import tiktoken

def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    return len(tokens)

# It's unlikely, but if the very first message in chat_history exceeds the entire token limit alone, 
# the printed truncated_history will be empty since we don't allow it to go past the first message
# One token is roughly equal to 3 chars (in English)
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
            truncated_history.insert(0, content)
            current_length += len(content) + 3
        else:
            print("Token limit reached. Current history: ", truncated_history)
            break

    return " | ".join(truncated_history)

