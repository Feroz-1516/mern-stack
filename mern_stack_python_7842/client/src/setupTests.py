# setupTests.py

# pytest adds custom pytest assertions for asserting on DOM nodes.
# This allows you to do things like:
# assert element.has_text_content("react", case_insensitive=True)
# Learn more: https://docs.pytest.org/en/stable/

import pytest
from pytest_django.asserts import *

# Add any custom test setup here if needed