"""
This module contains the APIConnector class for interacting with the SlickText API.
"""
import logging
import time
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
        "custom_fields": "/brands/{brand_id}/custom-fields/{field_id}"
    }

    def __init__(self, token: str):
        self.token = token
        self.session = requests.Session()

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
                       params: dict = None, retry_wait_time: int = 5):
        """
        Make a request to the SlickText API.
        :param url_key: The key for the endpoint
        :param method: The HTTP method (GET, POST, etc.)
        :param retry_wait_time: Time to wait before retrying in case of failure
        :return: The response from the API
        """
        url = self.__generate_url(url_key, dynamic_data)
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        retries = 5
        while retries > 0:
            try:
                logging.debug("Making %s request to %s with headers %s",
                              method.upper(), url, headers
                              )
                response = self.session.request(
                    method=method.upper(),
                    url=url,
                    headers=headers,
                    params=params)

                if response.status_code in [200, 201]:
                    logging.debug("Success: %s %s", method, url)
                    return response.json()

                logging.warning("Error %d: %s", response.status_code, response.text)
                retries -= 1
                time.sleep(retry_wait_time)
            except requests.exceptions.RequestException as e:
                logging.error("Request failed: %s", e)
                retries -= 1
                time.sleep(retry_wait_time)
                return None
        logging.error("Failed after %d retries: %s %s", 5, method, url)
        return None
