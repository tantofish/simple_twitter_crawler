from nose.tools import *
from twitwi.model.uri import Uri


def setup():
    print("SETUP!")

def teardown():
    print("TEAR DOWN!")

def test_constructor():
    uri = Uri('http://www.yahoo.com:80/path/to/example?date=20170101&time=1830&user=tantofish')
    assert uri.scheme == 'http'
    assert_equal(uri.hostname, 'www.yahoo.com')
    assert uri.port == 80
    assert uri.path == 'path/to/example'
    assert uri.params['user'] == 'tantofish'
    #assert uri.getUrl() == 'http://www.yahoo.com:80/path/to/example?date=20170101&time=1830&user=tantofish'

def test_constructor2():
    uri = Uri('http://www.yahoo.com')
    assert_equal(uri.scheme,   'http')
    assert_equal(uri.hostname, 'www.yahoo.com')
    assert_equal(uri.getUrl(), 'http://www.yahoo.com')

def test_updateParams():
    uri = Uri('http://www.yahoo.com').updateParams({'unittest':'true'})
    assert_equal(uri.params['unittest'], 'true')

def test_query2dict():
    params = Uri.query2dict('?a=1&b=hello&c=&d=qa123&')
    assert_equal(
        params,
        {
            'a' : '1',
            'b' : 'hello',
            'c' : '',
            'd' : 'qa123'
        }
    )


