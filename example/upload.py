from qdrant_client import QdrantClient
from docling.chunking import HybridChunker
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter

# Qdrant configuration
url = ""  
api_key = ""

# Initialize Qdrant client
client = QdrantClient(url=url, api_key=api_key)

# Set models
client.set_model("sentence-transformers/all-MiniLM-L6-v2")
client.set_sparse_model("Qdrant/bm25")

def upload_document(file_path, collection_name):
  
    # Initialize document converter with supported formats
    doc_converter = DocumentConverter(
        allowed_formats=[
            InputFormat.PPTX,
            InputFormat.PDF,
            InputFormat.DOCX,
            InputFormat.XLSX
        ]
    )

    # Convert document
    result = doc_converter.convert(file_path)

    # Process document chunks
    documents, metadatas = [], []
    for chunk in HybridChunker().chunk(result.document):
        documents.append(chunk.text)
        metadatas.append(chunk.meta.export_json_dict())

    # Upload to Qdrant
    client.add(
        collection_name=collection_name,
        documents=documents,
        metadata=metadatas,
        batch_size=64
    )



upload_document("11067791.pdf","chainlit")