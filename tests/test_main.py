import unittest

from app.main import process_request

class MainTests(unittest.TestCase):
    def test_pdf_refactor_mentions_2026_summit_prerequisite(self):
        response = process_request("pdf refactor")

        self.assertIn("2026 summit", response["response"])

if __name__ == "__main__":
    unittest.main()
