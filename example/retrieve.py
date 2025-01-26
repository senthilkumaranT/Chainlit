from qdrant_client import QdrantClient  # qdrant client


# set url and api key
url = ""  
api_key = ""
client = QdrantClient(url=url, api_key=api_key)

# set model
client.set_model("sentence-transformers/all-MiniLM-L6-v2")
client.set_sparse_model("Qdrant/bm25")


def retrieve(question ,collection_name):
    # qdrant client
    # query
    points = client.query(
        collection_name=collection_name,
        query_text=question,
        limit=3,
        
    )

    # final response
    final_response = " "

    # loop through points
    for i, point in enumerate(points):
        final_response += point.document

    return final_response  



    

    
    
    
    

