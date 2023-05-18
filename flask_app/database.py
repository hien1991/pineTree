import openai
import pinecone
from uuid import uuid4
from datetime import datetime
from tqdm.auto import tqdm

openai.api_key = ""
MODEL = "text-embedding-ada-002"
index_name = 'pinechat'

class Database:

    is_initialized = False
    index = None

    @staticmethod
    def initialize(pinecone_api_key, pinecone_environment):
        global index
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)

        # Check if the index already exists, and if not, create it
        if index_name not in pinecone.list_indexes():
            print("creating index: ", index_name)
            pinecone.create_index(index_name, dimension=1536, metric='dotproduct')

        Database.index = pinecone.Index(index_name)
        Database.is_initialized = True

    @staticmethod
    def create_memory_entry(categories, summary, file_name='', source='user input'):
        memory_id = f"memory_{str(uuid4())}"
        metadata = {
            "timestamp": datetime.now(),
            "filename": file_name,
            "categories": categories,
            "source": source,
            "text": summary
        }
        return {memory_id: {"text": summary, "metadata": metadata}}
    
    # Used by PineDocs page to retrieve info on all user's uploads
    @staticmethod
    def insert_uploads_record(file_name, num_chunks, file_size):
        pine_docs_namespace = 'hien91-pineDocs' # Will un-hardcode when usernames exist
        metadata = {
            "timestamp": datetime.now(),
            "filename": file_name,
            "num_chunks": num_chunks,
            "file_size": file_size,
            "text": file_name
        }

        memory_id = f"file_{str(uuid4())}"
        memory_entry = {memory_id: {"text": file_name, "metadata": metadata}}
        Database.update_db(memory_entry, namespace=pine_docs_namespace)


    @staticmethod
    def get_all_uploaded_files(pine_docs_namespace):
        query_vector = [0] * 1536
        results = Database.index.query(query_vector, top_k=100, namespace=pine_docs_namespace, include_metadata=True)

        uploaded_files = []
        for item in results['matches']:
            file_metadata = item['metadata']
            file_metadata['id'] = item['id'] # Add the memory_id to the metadata
            uploaded_files.append(item['metadata'])
        
        print("uploaded_file: ", uploaded_files)
        return uploaded_files
    
    @staticmethod
    def delete_file_by_filename(filename, pine_docs_namespace, user_namespace=""):
        try:
            Database.index.delete(
                namespace=pine_docs_namespace,
                filter={
                    "filename": {"$eq": filename},
                }
            )
            # TODO replace default namespace with userId one
            Database.index.delete(
                namespace=user_namespace,
                filter={
                    "filename": {"$eq": filename},
                    "source": "uploaded",
                }
            )

            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        

    @staticmethod
    def update_db(data, namespace=None):
        data_items = list(data.items())
        batch_size = 32
        for i in tqdm(range(0, len(data_items), batch_size)):
            i_end = min(i + batch_size, len(data_items))

            texts_batch = [item[1]["metadata"]["text"] for item in data_items[i:i_end]]
            ids_batch = [item[0] for item in data_items[i:i_end]]

            res = openai.Embedding.create(input=texts_batch, engine=MODEL)
            embeds = [record["embedding"] for record in res["data"]]

            to_upsert = [{"id": memory_id, "values": embedding, "metadata": metadata} for memory_id, embedding, metadata in zip(ids_batch, embeds, [item[1]["metadata"] for item in data_items[i:i_end]])]
            Database.index.upsert(vectors=to_upsert, namespace=namespace)

    @staticmethod
    def semantic_search(query, filter=None, top_k=5):
        xq = openai.Embedding.create(input=query, engine=MODEL)['data'][0]['embedding']
        res = Database.index.query(xq, top_k=top_k, filter=filter, include_metadata=True)
        results = []

        for item in res['matches']:
            results.append({
                'text': item['metadata']['text'],
                'timestamp': item['metadata'].get('timestamp', 'N/A'),
                'source': item['metadata'].get('source', 'N/A'),
                'filename': item['metadata'].get('filename', None)
            })

        return results


    @staticmethod
    def search_selected_files(filenames, query, top_k=10):
        meta_filter = {"filename": {"$in": filenames}}
        return Database.semantic_search(query, filter=meta_filter, top_k=top_k)

    @staticmethod
    def get_relevant_memories(search_query):
        user_input_memories = Database.semantic_search(search_query, filter={"source": {"$eq": "user input"}}, top_k=5)
        uploaded_memories = Database.semantic_search(search_query, filter={"source": {"$eq": "uploaded"}}, top_k=5)
        longterm_memories = user_input_memories + uploaded_memories
        return longterm_memories
