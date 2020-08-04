from urlshort import create_app

def test_shorten(client):
    responce = client.get('/')
    assert b'Shorten' in responce.data  # b is used for converting it into bytes