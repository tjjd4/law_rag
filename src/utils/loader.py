import os
import json
from langchain_community.document_loaders import JSONLoader 

DATA_PATH = "data"
PROJECT_PATH = "/home/aclab/Desktop/law_rag"

class Loader:
    def __init__(self):
        self.documents = None
        self.data = None

    def load_json_file(
            self, 
            file_path: str, 
            jq_schema: str, 
            text_content: bool = True, 
            content_key: str = None
        ):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"Input file not found: {file_path}")
            return
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return
        
        loader = JSONLoader(
            file_path=file_path,
            jq_schema=jq_schema,
            text_content=text_content,
            content_key=content_key,
            metadata_func=self.laws_en_metadata_func
        )

        self.documents = loader.load()
        return self.documents
    
    def laws_ch_metadata_func(self, record: dict, metadata: dict) -> dict:
        path = os.path.relpath(str(metadata.get("source")), "/home/aclab/Desktop/law_rag")
        metadata["id"] = path + ":" + str(metadata.get("seq_num"))
        metadata["source"] = path
        metadata["LawLevel"] = record.get("LawLevel")
        metadata["LawName"] = record.get("LawName")
        metadata["LawCategory"] = record.get("LawCategory")
        metadata["ArticleType"] = record.get("ArticleType")
        metadata["ArticleNo"] = record.get("ArticleNo")

        return metadata
    
    def laws_en_metadata_func(self, record: dict, metadata: dict) -> dict:
        path = os.path.relpath(str(metadata.get("source")), "/home/aclab/Desktop/law_rag")
        metadata["id"] = path + ":" + str(metadata.get("seq_num"))
        metadata["source"] = path
        metadata["LawLevel"] = record.get("LawLevel")
        metadata["EngLawName"] = record.get("EngLawName")
        metadata["EngArticleType"] = record.get("EngArticleType")
        metadata["EngArticleNo"] = record.get("EngArticleNo")

        return metadata
    
    def clear(self):
        self.documents = None
        self.data = None