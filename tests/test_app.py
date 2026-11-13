import threading
import unittest
import urllib.request
from http.server import HTTPServer

from app.app import Handler


class AppTest(unittest.TestCase):
    def test_get_returns_greeting(self):
        server = HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.shutdown)
        with urllib.request.urlopen(f"http://127.0.0.1:{server.server_port}/") as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("hello from the pipeline", resp.read().decode())


if __name__ == "__main__":
    unittest.main()
