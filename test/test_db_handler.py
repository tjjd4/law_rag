import os
import unittest
import shutil

from src.db_handler import ChromaDBHandler
from langchain.schema.document import Document

TEST_DB_PATH = "test_chroma"

class TestDbHandler(unittest.TestCase):

    test_documents = [
        Document(
            page_content="The Republic of China, founded on the Three Principles of the People, shall be a democratic republic of the people, to be governed by the people and for the people.",
            metadata={
                "id": "data/laws_en.json:1",
                "source": "data/laws_en.json",
                "LawLevel": "憲法",
                "EngLawName": "Constitution of the Republic of China (Taiwan)",
                "ArticleType": "A",
                "ArticleNo": "Article 1",
            }
        ),
        Document(
            page_content="The Executive Yuan shall, within four months after the end of each fiscal year, present final accounts of revenues and expenditures to the Control Yuan.",
            metadata={
                "id": "data/laws_en.json:2",
                "source": "data/laws_en.json",
                "LawLevel": "憲法",
                "EngLawName": "Constitution of the Republic of China (Taiwan)",
                "ArticleType": "A",
                "ArticleNo": "Article 60",
            }
        ),
        Document(
            page_content="Anyone who has access to the names and address of winners of the lottery shall keep that information confidential except otherwise provided by law. Violators shall be responsible for winner’s losses resulting from violations of the preceding paragraph upon winner’s request.",
            metadata={
                "id": "data/laws_en.json:3",
                "source": "data/laws_en.json",
                "LawLevel": "法律",
                "EngLawName": "Public Welfare Lottery Issue Act",
                "ArticleType": "A",
                "ArticleNo": "Article 10"
            }
        ),
        Document(
            page_content="In case an insured person temporarily loses his salary because of an injury for which he receives injury or sickness benefits or hospital care benefits, he may be exempted from paying his portion of the premiums so long as his salary is suspended. \r\nThe period during which an insured person is exempted from paying his portion of the insurance premiums referred to in the preceding paragraph shall be included in calculating his coverage period.",
            metadata={
                "id": "data/law_ch.json:4",
                "source": "data/law_ch.json",
                "LawLevel": "法律",
                "EngLawName": "Labor Insurance Act",
                "ArticleType": "A",
                "ArticleNo": "Article 18"
            }
        ),
        Document(
            page_content="If there is no applicable act for a civil case, the case shall be decided according to customs. If there is no such custom, the case shall be decided according to the jurisprudence.",
            metadata={
                "id": "data/law_ch.json:5",
                "source": "data/law_ch.json",
                "LawLevel": "法律",
                "EngLawName": "Civil Code",
                "ArticleType": "A",
                "ArticleNo": "Article 1"
            }
        ),
        Document(
            page_content="The property of an absent person, after his absence and up to the declaration of death, shall be administered according to the Family Act.",
            metadata={
                "id": "data/law_ch.json:6",
                "source": "data/law_ch.json",
                "LawLevel": "法律",
                "LawName": "Civil Code",
                "ArticleType": "A",
                "ArticleNo": "Article 10"
            }
        )
    ]

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEST_DB_PATH):
            shutil.rmtree(TEST_DB_PATH)

    def setUp(self) -> None:
        self.handler = ChromaDBHandler(path=TEST_DB_PATH)
        return super().setUp()
    
    def tearDown(self) -> None:
        # [TODO] clear ResourceWarning: unclosed socket
        self.handler.clear()
        return super().tearDown()
    
    def test_initialize(self):
        self.assertTrue(os.path.exists(TEST_DB_PATH), f"Directory {TEST_DB_PATH} was not created")

    def test_get_data_amount(self):
        amount = self.handler.get_data_amount()
        self.assertEqual(amount, 0)
    
    def test_check_documents_existed(self):
        for document in self.test_documents:
            self.assertFalse(self.handler.check_documents_existed(document.metadata.get("id")))

    def test_add_documents(self):
        self.assertEqual(self.handler.get_data_amount(), 0)
        self.handler.add_documents(self.test_documents)
        self.assertEqual(self.handler.get_data_amount(), 6)
        for document in self.test_documents:
            self.assertTrue(self.handler.check_documents_existed(document.metadata.get("id")))

    def test_clear(self):
        self.assertEqual(self.handler.get_data_amount(), 0)
        self.handler.add_documents(self.test_documents)
        self.assertEqual(self.handler.get_data_amount(), 6)
        self.handler.clear()
        self.assertEqual(self.handler.get_data_amount(), 0)

    def test_retrieve(self):
        self.handler.add_documents(self.test_documents)
        query = "If I am missing, who can use my money?"
        results = self.handler.retrieve(query=query, top_k=1)
        print(results)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].metadata.get("id"), 'data/law_ch.json:6')



if __name__ == '__main__':
    unittest.main()