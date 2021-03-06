from flask import session, g
from portal import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_index(client):
    response = client.get('/')
    assert b'<h1 class="h1head">TSCT Portal</h1>' in response.data
