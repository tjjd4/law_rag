from langchain.schema.document import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

embedding_model = "nomic-embed-text"
CHROMA_PATH = "chroma"

class ChromaDBHandler:

    def __init__(self, model=embedding_model, path=CHROMA_PATH):
        self.persist_directory = path
        self.embedding_function = OllamaEmbeddings(model=model)
        self.chroma_db = self._initialize_chromadb()

    def _initialize_chromadb(self):
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function,
        )
    
    def get_data_amount(self):
        existing_items = self.__get_all_data()
        existing_ids = set(existing_items["ids"])
        return len(existing_ids)
    
    def check_documents_existed(self, source_id):
        existing_items = self.chroma_db.get(include=[])  # IDs are always included by default
        existing_ids = set(existing_items["ids"])

        return source_id in existing_ids
    
    def add_documents(self, docs: list[Document]):
        # chroma db max batch size
        MAX_BATCH_SIZE = 41665
        new_docs = []
        new_ids = []
        for doc in docs:
            if not doc.metadata.get("id"):
                raise ValueError(f"Document is missing 'id'. Document: {doc}")

            if self.check_documents_existed(doc.metadata.get("id")):
                continue

            new_docs.append(doc)
            new_ids.append(doc.metadata.get("id"))
        if new_docs:
            print(f"Adding {len(new_docs)} new documents in batches.")
        
            for i in range(0, len(new_docs), MAX_BATCH_SIZE):
                batch_docs = new_docs[i:i + MAX_BATCH_SIZE]
                batch_ids = new_ids[i:i + MAX_BATCH_SIZE]
                print(f"Inserting batch {i // MAX_BATCH_SIZE + 1}: {len(batch_docs)} documents.")
                self.chroma_db.add_documents(batch_docs, ids=batch_ids)
        else:
            print("Nothing new to add!")

    def get_chroma_db(self):
        return self.chroma_db
    
    def __get_all_data(self)-> dict:
        existing_items = self.chroma_db.get(include=["metadatas"])
        return existing_items
    
    def clear(self):
        self.chroma_db.reset_collection()
        # docs = self.__get_all_data()
        # del_ids = docs.get("ids")
        # if len(del_ids) > 0:
        #     print(f"Delete all documents in DB: {len(del_ids)}")
        #     self.chroma_db.delete(ids=docs.get("ids"))

    def retrieve(self, query, top_k=5)-> list[Document]:
        results = self.chroma_db.similarity_search(query=query, k=top_k)
        return results
