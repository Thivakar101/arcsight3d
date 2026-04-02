import pytest
from backend.utils.image_utils import allowed_file

def test_allowed_file():
    assert allowed_file("test.png") == True
    assert allowed_file("test.jpg") == True
    assert allowed_file("test.jpeg") == True
    assert allowed_file("test.pdf") == False
    assert allowed_file("test") == False
