import sys
import unittest

sys.path.append("..")

import utils
import api


class ApiTest(unittest.TestCase):
    def test_dropbox_token_valid(self):
        client = api.DropboxClient(utils.access_secret())
        self.assertEqual(client.initialised, True)
        self.assertEqual(client.connected, True)
        self.assertEqual(client.authenticated, True)

    def test_dropbox_token_invalid(self):
        client = api.DropboxClient(utils.bad_secret())
        self.assertEqual(client.initialised, True)
        self.assertEqual(client.connected, True)
        self.assertEqual(client.authenticated, False)