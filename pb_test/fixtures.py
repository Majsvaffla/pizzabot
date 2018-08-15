import pytest 

@pytest.fixture
def dummy_view_class():
    def decorated_fixture(response):
        class ViewClass:
            def view_method(self, *args, **kwargs):
                return response

        return ViewClass

    return decorated_fixture
