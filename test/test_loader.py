import unittest

from src.utils.loader import Loader
from langchain.schema.document import Document

class TestLoader(unittest.TestCase):
    def setUp(self) -> None:
        self.loader = Loader()
        self.loader.load_json_file(
            file_path="data/laws_ch.json",
            jq_schema=".[]",
            content_key="ArticleContent",
            text_content=False
        )
        return super().setUp()
    
    def tearDown(self) -> None:
        self.loader.clear()
        return super().tearDown()
    
    def test_load_json_file(self):
        self.assertIsInstance(self.loader.data, list, "data is not a list.")
        self.assertIsInstance(self.loader.data[0], dict, "data in list is not a dict.")

        self.assertTrue(len(self.loader.documents) > 0, "Returned data is empty.")
        self.assertIsInstance(self.loader.documents[0], Document, "First element is not a Document.")
        print(self.loader.documents[0].metadata)

    def test_document_metadata(self):
        required_keys = ["id", "source", "LawLevel", "LawName", "LawCategory"]

            # 確保 metadata 中包含所有所需鍵
        for key in required_keys:
            with self.subTest(key=key):
                self.assertIn(key, self.loader.documents[0].metadata, f"Metadata is missing key: {key}")
        

    def test_clear(self):
        self.loader.clear()
        self.assertEqual(self.loader.data, None)
    
if __name__ == '__main__':
    unittest.main()