from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from .chat import chat, initializeChat
from .database import Database
from .SaveMemories import get_categories_and_summary
from .upload import process_uploaded_file
from .SearchQuery import get_search_query
from .database import Database


app = Flask(__name__, static_folder='static', template_folder='templates')
openai_api_key_global = None
short_term_memories_global = [] # chat history between user & AI
pinecone_api_key_global = None
pinecone_environment_global = None
useGpt4_global = None
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx', 'ppt', 'pptx', 'md', 
                      'html', 'csv', 'jpg', 'jpeg', 'png', 'gif'}
CORS(app)  # Allows Cross-Origin Resource Sharing to prevent console error

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_search_result(memory_item, index):
    title = memory_item["filename"] if memory_item["filename"] is not None else f"Query result # {index + 1}"
    return {
        "title": title,
        "timestamp": memory_item["timestamp"],
        "source": memory_item["source"],
        "text": memory_item["text"]
    }

def saveUserInput(input_text):
    categories, summary = get_categories_and_summary(input_text, openai_api_key_global)
    memory_entry = Database.create_memory_entry(categories, summary)
    memory_id = list(memory_entry.keys())[0]
    if memory_entry[memory_id]["metadata"]["text"] != "N/A":
        Database.update_db(memory_entry)


@app.route('/chat', methods=['POST'])
def chat_route():
    global openai_api_key_global, short_term_memories_global, pinecone_api_key_global
    input_text = request.json.get('input_text', '')

    if not Database.is_initialized:
        return jsonify({"status": "error", "message": "The chat is not ready yet. Please wait for the initialization to complete."})

    try:
        search_query = get_search_query(input_text, short_term_memories_global, openai_api_key_global)
        longterm_memories = Database.get_relevant_memories(search_query)
        saveUserInput(input_text)  # Save relevant info from user into db
        response, short_term_memories_global = chat(input_text, short_term_memories_global, longterm_memories)

        formatted_search_results = [format_search_result(item, index) for index, item in enumerate(longterm_memories)]
        #print("search results: ", formatted_search_results)
        return jsonify({"response": response, "search_results": formatted_search_results, "db_query": search_query})
    except Exception as e:
        return jsonify({"status": "error", "message": "Error: " + str(e)})


@app.route('/upload', methods=['POST'])
def upload_file():
    global pinecone_api_key_global, pinecone_environment_global
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file and allowed_file(file.filename):
        result = process_uploaded_file(file, Database)
        return jsonify(result)
    else:
        return jsonify({"error": "Unsupported file type"}), 400
    

@app.route('/get_all_uploads', methods=['GET'])
def get_all_uploads():
    if not Database.is_initialized:
        return jsonify({"error": "Database is not initialized"})
    
    pine_docs_namespace = 'hien91-pineDocs' # hardcoded until userId + users feature
    uploaded_files = Database.get_all_uploaded_files(pine_docs_namespace)
    return uploaded_files


@app.route('/initialize', methods=['POST'])
def initialize_flask():
    global openai_api_key_global, pinecone_api_key_global, pinecone_environment_global, useGpt4_global
    data = request.json
    openai_api_key_global = data['openaiApiKey']
    pinecone_api_key_global = data['pineconeApiKey']
    pinecone_environment_global = data['pineconeEnvKey']
    useGpt4_global = data['useGpt4Key']
    try:
        Database.initialize(pinecone_api_key_global, pinecone_environment_global)
        initializeChat(openai_api_key_global, useGpt4_global)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('flask_app/static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
