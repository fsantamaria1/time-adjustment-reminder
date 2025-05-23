"""
This module contains the APIConnector class for interacting with the SlickText API.
"""
import logging
import time
import json
import requests


class APIConnector:
    """
    Class for making requests to the SlickText API.
    """
    BASE_URL = "https://dev.slicktext.com/v1"
    ENDPOINTS = {
        "brands": "/brands",
        "brand_details": "/brands/{brand_id}",
        "contacts": "/brands/{brand_id}/contacts",
        "contact_details": "/brands/{brand_id}/contacts/{contact_id}",
        "create_list": "/brands/{brand_id}/lists",
        "add_contact_to_list": "/brands/{brand_id}/lists/contacts",
        "campaigns": "/brands/{brand_id}/campaigns",
        "custom_fields": "/brands/{brand_id}/custom-fields/{field_id}"
    }
    DEFAULT_RETRY_WAIT_TIME = 5
    MAX_RETRIES = 5

    def __init__(self, token: str, brand_id: str = None):
        self.token = token
        self.brand_id = brand_id
        self.session = requests.Session()

    def set_brand_id(self, brand_id: str):
        """
        Set the brand ID for the API requests.
        :param brand_id: The brand ID to set.
        """
        self.brand_id = brand_id

    def __generate_url(self, key: str, dynamic_data: dict = None) -> str:
        """
        Generate a URL for the given key.
        :param key: The key for the endpoint
        :param dynamic_data: A dictionary with dynamic values to be placed in the url.
        :return: A complete URL string with the base endpoint and the given key
        """
        url = f"{self.BASE_URL}{self.ENDPOINTS[key]}"
        if dynamic_data:
            # Replace any dynamic parts of the URL, like {address}
            url = url.format(**dynamic_data)
        return url

    def __make_request(self, url_key: str = None, method: str = "GET", dynamic_data: dict = None,
                       params: dict = None, body: dict or list = None):
        """
        Make a request to the SlickText API.
        :param url_key: The key for the endpoint
        :param method: The HTTP method (GET, POST, etc.)
        :return: The response from the API or None if the request fails
        """
        url = self.__generate_url(url_key, dynamic_data)
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        retries = self.MAX_RETRIES
        while retries > 0:
            try:
                logging.debug("Making %s request to %s with headers %s",
                              method.upper(), url, headers
                              )
                response = self.session.request(
                    method=method.upper(),
                    url=url,
                    headers=headers,
                    params=params,
                    json=body)

                if response.status_code in [200, 201]:
                    logging.debug("Success: %s %s", method, url)
                    try:
                        return response.json()
                    except json.JSONDecodeError as e:
                        logging.error(
                            "Failed to decode JSON response for %s %s: %s",
                            method,
                            url,
                            e
                        )
                        return None

                logging.warning("Error %d: %s", response.status_code, response.text)
            except requests.exceptions.RequestException as e:
                logging.error("Request failed: %s", e)
            retries -= 1
            time.sleep(self.DEFAULT_RETRY_WAIT_TIME)
        logging.error("Failed after %d retries: %s %s", self.MAX_RETRIES, method, url)
        return None

    def get_brands(self):
        """
        Get all brands associated with the account.
        :return: Dictionary containing brand data.
        """
        return self.__make_request("brands")

    def get_contacts(self, limit=None, offset=None, page=None, page_size=None, **filters):
        """
        Get contacts with pagination and filtering.
        :param limit: Max items per request (max 250)
        :param offset: Items to skip
        :param page: Page number (0-based)
        :param page_size: Items per page
        :param filters: Filter parameters as key=value
        """
        if not self.brand_id:
            raise ValueError("brand_id must be set to call get_contacts")

        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size
        params.update(filters)

        return self.__make_request(
            "contacts",
            dynamic_data={"brand_id": self.brand_id},
            params=params
        )

    def get_all_contacts(self, **filters):
        """Get all contacts with automatic pagination."""
        all_contacts = []
        limit = 250
        offset = 0

        while True:
            batch = self.get_contacts(
                limit=limit,
                offset=offset,
                **filters
            )

            if not batch or not isinstance(batch.get('data'), list):
                break
            all_contacts.extend(batch.get('data', []))
            if not batch.get('pagingData', {}).get('hasMore', False):
                break
            offset += limit

        return all_contacts

    def get_contact_details(self, contact_id):
        """
        Get details of a specific contact.
        """
        if not self.brand_id:
            raise ValueError("brand_id must be set to call get_contact_details")

        return self.__make_request(
            "contact_details",
            dynamic_data={"brand_id": self.brand_id, "contact_id": contact_id}
        )

    def create_contact_list(self, name=None, description=None):
        """
        Creates a contact list
        """
        if not self.brand_id:
            raise ValueError("brand_id must be set to call create_contact_list")
        if not name:
            raise ValueError("name must be provided to create a contact list")
        return self.__make_request(
            "create_list",
            method="POST",
            dynamic_data={"brand_id": self.brand_id},
            body={
                "name": name,
                "description": description
            }
        )

    def add_contact_to_list(self, contact_id, list_id):
        """
        Add a contact to a list.
        """
        if not self.brand_id:
            raise ValueError("brand_id must be set to call add_contact_to_list")
        if not contact_id:
            raise ValueError("contact_id must be provided to add a contact to a list")
        if not list_id:
            raise ValueError("list_id must be provided to add a contact to a list")

        return self.__make_request(
            "add_contact_to_list",
            method="POST",
            dynamic_data={"brand_id": self.brand_id},
            body=[{
                "contact_id": int(contact_id),
                "lists": [list_id]
            }]
        )

    def add_contacts_to_list(self, contact_ids, list_id):
        """
        Add multiple contacts to a list.
        :param contact_ids: List of contact IDs to add.
        :param list_id: The ID of the list to add contacts to.
        """
        if not self.brand_id:
            raise ValueError("brand_id must be set to call add_contacts_to_list")
        if not contact_ids or not isinstance(contact_ids, list):
            raise ValueError("contact_ids must be provided to add contacts to a list")
        if not list_id:
            raise ValueError("list_id must be provided to add contacts to a list")
        if len(contact_ids) < 1:
            return ValueError("contact_ids list must contain at least one contact ID")

        body = [{"contact_id": int(contact_id), "lists": [list_id]} for contact_id in contact_ids]

        return self.__make_request(
            "add_contact_to_list",
            method="POST",
            dynamic_data={"brand_id": self.brand_id},
            body=body
        )

    def get_custom_field(self, field_id):
        """Get details for a custom field."""
        if not self.brand_id:
            raise ValueError("brand_id must be set to call get_custom_field")

        return self.__make_request(
            "custom_fields",
            dynamic_data={"brand_id": self.brand_id, "field_id": field_id}
        )

    def create_campaign(self, name, message, contact_list, send_time=None):
        """
        Create a new campaign.
        :param name: The name of the campaign.
        :param message: The message content of the campaign.
        :param contact_list: The ID of the contact list to send the campaign to.
        :param send_time: Optional send time for the campaign.
        :return: The response from the API.
        """
        if not self.brand_id:
            raise ValueError("brand_id must be set to call create_campaign")

        body = {
            "name": name,
            "body": message,
            "status": "scheduled" if send_time else "send",
            "audience": {
                "contact_lists": [contact_list]
            },
            "scheduled": send_time
        }

        return self.__make_request(
            "campaigns",
            method="POST",
            dynamic_data={"brand_id": self.brand_id},
            body=body
        )
