from url_fixture import url
import pytest
import requests
import urllib

@pytest.fixture
def initialisation(url):