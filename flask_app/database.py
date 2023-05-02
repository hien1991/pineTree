import openai
import pinecone
from uuid import uuid4
from datetime import datetime
from tqdm.auto import tqdm

openai.api_key = ""
MODEL = "text-embedding-ada-002"
index_name = 'pinechat'
index = None

class Database:

    is_initialized = False

    @staticmethod
    def initialize(pinecone_api_key, pinecone_environment):
        global index
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)

        # Check if the index already exists, and if not, create it
        if index_name not in pinecone.list_indexes():
            print("creating index: ", index_name)
            pinecone.create_index(index_name, dimension=1536, metric='dotproduct')

        index = pinecone.Index(index_name)  # Connect to the Pinecone index
        Database.is_initialized = True

    @staticmethod
    def create_memory_entry(categories, summary):
        memory_id = f"memory_{str(uuid4())}"
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "categories": categories,
            "source": "user input",
            "text": summary
        }
        return {memory_id: {"text": summary, "metadata": metadata}}

    @staticmethod
    def update_db(data):
        data_items = list(data.items())
        batch_size = 32
        for i in tqdm(range(0, len(data_items), batch_size)):
            i_end = min(i + batch_size, len(data_items))

            texts_batch = [item[1]["metadata"]["text"] for item in data_items[i:i_end]]
            ids_batch = [item[0] for item in data_items[i:i_end]]

            res = openai.Embedding.create(input=texts_batch, engine=MODEL)
            embeds = [record["embedding"] for record in res["data"]]

            to_upsert = [{"id": memory_id, "values": embedding, "metadata": metadata} for memory_id, embedding, metadata in zip(ids_batch, embeds, [item[1]["metadata"] for item in data_items[i:i_end]])]
            index.upsert(vectors=to_upsert)

    @staticmethod
    def semantic_search(query, filter=None, top_k=5):
        xq = openai.Embedding.create(input=query, engine=MODEL)['data'][0]['embedding']
        meta_filter = None if filter is None else {"source": {"$eq": filter}}
        res = index.query(xq, top_k=top_k, filter=meta_filter, include_metadata=True)
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
    def get_relevant_memories(search_query):
        user_input_memories = Database.semantic_search(search_query, filter="user input", top_k=5)
        uploaded_memories = Database.semantic_search(search_query, filter="uploaded", top_k=5)
        longterm_memories = user_input_memories + uploaded_memories
        return longterm_memories

