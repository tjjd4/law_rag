from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

from src.utils.loader import Loader
from src.db_handler import ChromaDBHandler
from pprint import pprint

class Rag:
    def __init__(self):
        self.loader = Loader()
        self.handler = ChromaDBHandler()
        self.llm = ChatOllama(
            model = "llama3.2",
            temperature = 0.2
        )
        self.prompt_template = PromptTemplate.from_template(
            """
            You are an law assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

            Question: {question} 

            Context: {context} 

            Answer:
            """
        )

    def add_json_file(self, file_path, jq_schema, content_key=None, text_content=True):
        docs = self.loader.load_json_file(
            file_path=file_path,
            jq_schema=jq_schema,
            content_key=content_key,
            text_content=text_content
        )
        print(len(docs))
        if docs != None and len(docs) > 0:
            self.handler.add_documents(docs=docs)

    def invoke(self, question, top_k=5):
        docs = self.handler.retrieve(query=question, top_k=top_k)
        for doc in docs:
            print(f"法律名稱：{doc.metadata.get("EngLawName")}")
            print(f"第幾條：{doc.metadata.get("EngArticleNo")}")
            print(f"內容：{doc.page_content}")
        prompt = self.prompt_template.invoke({ "question": question, "context": docs })
        response = self.llm.invoke(prompt)
        return response

if __name__ == '__main__':
    rag = Rag()
    # rag.add_json_file(
    #     file_path="data/laws_en.json",
    #     jq_schema=".[]",
    #     content_key="EngArticleContent",
    #     text_content=False
    # )
    response = rag.invoke("Tell me about the law with context like Articles 47 to 52 and Article 75 of the Commercial Case Adjudication...")
    print(response.content)