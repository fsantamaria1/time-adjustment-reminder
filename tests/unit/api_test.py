"""
Unit tests for the APIConnector class.
"""
from unittest.mock import MagicMock
import requests
import pytest
from res.api import APIConnector


class TestAPIConnectorUnit:
    """
    Unit tests for the APIConnector class.
    """
    @pytest.fixture
    def api_connector(self):
        """
        Fixture to return an APIConnector object.
        :return: APIConnector object
        """
        return APIConnector(token="test_token")

    def test_init(self, api_connector: APIConnector):
        """
        Test the __init__ method to ensure the session is initialized.
        :param api_connector: The APIConnector object
        """
        assert api_connector.token == "test_token"
        assert api_connector.session is not None
        assert isinstance(api_connector.session, requests.Session)

    def test_generate_url(self, monkeypatch, api_connector: APIConnector):
        """
        Test that the generated URL inside a public method matches expectations.
        """
        expected_url = f"{APIConnector.BASE_URL}{APIConnector.ENDPOINTS['brands']}"

        # Mock response object with expected status & data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"test_data 1": 1}, {"test_data 2": 2}]}

        # Mock session.request to return the mock response
        mock_request = MagicMock(return_value=mock_response)
        monkeypatch.setattr(api_connector.session, "request", mock_request)

        # Call get_brands(), which internally calls __generate_url()
        api_connector.get_brands()

        # Extract the actual URL used in the request
        actual_url = mock_request.call_args[1]["url"]  # Fetch 'url' from kwargs in the mock call
        assert actual_url == expected_url

    def test_make_request_get_success(self, monkeypatch, api_connector: APIConnector):
        """
        Test that the __make_request method returns the correct data for a successful GET request.
        :param monkeypatch: The monkeypatch fixture
        :param api_connector: The APIConnector object
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"test_data 1": 1}, {"test_data 2": 2}]}

        mock_request = MagicMock(return_value=mock_response)
        monkeypatch.setattr(api_connector.session, "request", mock_request)

        # Call get_brands(), which internally calls __make_request()
        result = api_connector.get_brands()

        assert result == {"data": [{"test_data 1": 1}, {"test_data 2": 2}]}

    def test_make_request_failure(self, monkeypatch, api_connector: APIConnector):
        """
        Test that the __make_request method returns None when the request fails.
        :param monkeypatch: The monkeypatch fixture
        :param api_connector: The APIConnector object
        """
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"result": None}

        mock_request = MagicMock(return_value=mock_response)
        monkeypatch.setattr(api_connector.session, "request", mock_request)

        # Prevent actual sleep during the test
        monkeypatch.setattr("time.sleep", lambda x: None)

        # Call get_brands(), which internally calls __make_request()
        result = api_connector.get_brands()

        assert result is None
        assert mock_request.call_count == 5

    def test_handle_non_success_status_code(self, monkeypatch, api_connector):
        """
        Test that the __make_request method handles non-success status codes correctly.
        :param monkeypatch: The monkeypatch fixture
        :param api_connector: The APIConnector object
        :return:
        """

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"

        mock_request = MagicMock(return_value=mock_response)
        monkeypatch.setattr(api_connector.session, "request", mock_request)

        # Prevent actual sleep during the test
        monkeypatch.setattr("time.sleep", lambda x: None)

        # Call get_brands(), which internally calls __make_request()
        result = api_connector.get_brands()

        # Should retry 5 times
        assert api_connector.session.request.call_count == APIConnector.MAX_RETRIES
        # Should return None after all retries fail
        assert result is None
