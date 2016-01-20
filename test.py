import os
import server
import unittest
import tempfile
import json


class FlaskrTestCase(unittest.TestCase):
    db_file = "./test.db"

    def setUp(self):
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        db_conf = "sqlite:///{}".format(self.db_file)
        server.app.config['SQLALCHEMY_DATABASE_URI'] = db_conf
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        server.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])
        os.unlink(self.db_file)

    def test_initial_page_status_code(self):
        rv = self.app.get('/')
        # import code; code.interact(local=locals())
        assert rv.status_code == 200

    def test_posts_list_status_code(self):
        rv = self.app.get('/posts')
        assert rv.status_code == 200

    def test_posts_list_response(self):
        rv = self.app.get('/posts')
        data = json.loads(rv.data)
        self.assertTrue('posts' in data)

    def test_posts_list_contains_array(self):
        rv = self.app.get('/posts')
        data = json.loads(rv.data)
        self.assertTrue(isinstance(data['posts'], list))

if __name__ == '__main__':
    unittest.main()
