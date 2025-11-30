import pytest
import requests

# Simple Pytest test to verify setup
def test_pytest_setup():
    """Test that Pytest is working correctly"""
    assert 1 + 1 == 2

def test_basic_math():
    """Test basic mathematical operations"""
    assert 2 * 3 == 6
    assert 10 / 2 == 5

def test_string_operations():
    """Test string operations"""
    text = "hello world"
    assert len(text) == 11
    assert text.upper() == "HELLO WORLD"