"""
This module contains the integration tests for the APIConnector class.
"""
import os
import pytest
from dotenv import load_dotenv
from res.api import APIConnector

# Load the environment variables
load_dotenv()
token = os.environ.get('SLICK_TEXT_API_KEY') or os.getenv('SLICK_TEXT_API_KEY')
brand_id = os.environ.get('SLICK_TEXT_BRAND_ID') or os.getenv('SLICK_TEXT_BRAND_ID')


class TestAPIConnectorIntegration:
    """
    Integration tests for the APIConnector class.
    """
    @pytest.fixture
    def api_connector(self):
        """
        Fixture to return an APIConnector object.
        :return: APIConnector object
        """
        return APIConnector(token=token)

    def test_get_brands_integration(self, api_connector):
        """
        Test that the get_brands method returns a list of brands.
        :param api_connector: The APIConnector object
        """
        brands = api_connector.get_brands()
        assert isinstance(brands, dict)
        # Ensure the list is not empty
        assert len(brands) > 0
        # Ensure the dictionary contains an account_id key
        assert "_account_id" in brands

    def test_get_contacts_integration(self, api_connector):
        """
        Test that the get_contacts method returns a list of contacts.
        :param api_connector: The APIConnector object
        """
        contacts = api_connector.get_contacts(brand_id)
        assert isinstance(contacts, dict)
        assert len(contacts) > 0
        assert "data" in contacts
        assert isinstance(contacts["data"], list)
        assert len(contacts["data"]) > 0
        assert 'pagingData' in contacts

    def test_get_all_contacts_integration(self, api_connector):
        """
        Test that the get_all_contacts method returns a list of contacts.
        :param api_connector: The APIConnector object
        """
        contacts = api_connector.get_all_contacts(brand_id)
        assert isinstance(contacts, list)
        assert len(contacts) > 0
