from nose.tools import *
from twitwi.dao.twitterdao import TwitterDao
from twitwi.model.uri import Uri

def setup():
    print("SETUP!")

def teardown():
    print("TEAR DOWN!")

def test_constructor():
    dao = TwitterDao()
    assert_equal(dao.getUri().params['q'], 'helloworld')

def test_setParams():
    dao = TwitterDao().setParams({'q':'unittest'})
    assert_equal(dao.getUri().params['q'], 'unittest')

def test_getUri():
    dao = TwitterDao()
    assert isinstance(dao.getUri(), Uri)

def test_getAjaxUri():
    dao = TwitterDao()
    assert isinstance(dao.getAjaxUri(), Uri)
