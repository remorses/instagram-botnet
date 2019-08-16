import pytest
from .templates import all

@pytest.fixture(params=list(all.values()), ids=list(all.keys()))
def template(request):
    return request.param
