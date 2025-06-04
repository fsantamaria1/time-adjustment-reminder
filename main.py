"""
Main module of the time adjustment reminder script.
"""
import os
from res.api import APIConnector
from res.db.db_functions import (
    get_pay_period_by_start_date,
    get_worker_ids_with_missing_punches_by_pay_period
)
from res.db.database import Database
from res.date_util import DateUtil

# Get the environment variables for API key and brand ID
API_KEY = os.getenv("SLICK_TEXT_API_KEY")
if not API_KEY:
    raise ValueError("SLICK_TEXT_API_KEY environment variable is not set.")
BRAND_ID = os.getenv("SLICK_TEXT_BRAND_ID")
if not BRAND_ID:
    raise ValueError("SLICK_TEXT_BRAND_ID environment variable is not set.")

# Define the message content for the campaign
MESSAGE_CONTENT = """
Good morning,
This is a reminder that a time adjustment is needed on your timecard.
Please review your ADP timecard and enter a KPA Time adjustment as soon as possible, if you haven't already done so.
Thanks!
"""


def fetch_pay_period(session):
    """
    Fetch the pay period for the previous week.
    :param session: The database session.
    :return: The pay period object for the previous week.
    """
    last_monday = DateUtil().get_last_monday()
    return get_pay_period_by_start_date(session, last_monday)


def get_missing_punch_data(session, pay_period):
    """
    Get and log the worker IDs with missing punches for the specified pay period.
    :param session: The database session.
    :param pay_period: The pay period object.
    :return: A list of worker IDs with missing punches.
    """
    worker_ids = get_worker_ids_with_missing_punches_by_pay_period(
        session,
        pay_period.pay_period_id
    )

    return worker_ids


def process_contacts(api_connector, worker_ids):
    """
    Process contacts and match against worker IDs with missing punches.
    :param api_connector:
    :param worker_ids:
    :return:
    """
    contacts = api_connector.get_all_contacts(brand_id=BRAND_ID)
    contact_ids = []

    for contact in contacts:
        contact_id = contact.get('contact_id')
        adp_worker_id = contact.get('custom_fields', {}).get('adp_associate_id', None)

        if not adp_worker_id:
            continue

        if adp_worker_id in worker_ids:
            contact_ids.append(contact_id)

    return contact_ids


def create_campaign(api_connector, pay_period, contact_ids):
    """
    Create a campaign for the contacts with missing punches.
    :param api_connector: The API connector instance.
    :param pay_period: The pay period object.
    :param contact_ids: List of contact IDs to include in the campaign.
    :return: The campaign ID.
    """
    reminder_name = (f"Time Adjustment Reminder "
                         f"{pay_period.pay_period_start} - "
                         f"{pay_period.pay_period_end}")

    # Create contact list
    contact_list = api_connector.create_contact_list(reminder_name)
    contact_list_id = contact_list.get("contact_list_id")

    # Add contacts to the contact list
    api_connector.add_contacts_to_list(contact_ids, contact_list_id)

    # Create campaign
    campaign = api_connector.create_campaign(
        reminder_name,
        MESSAGE_CONTENT,
        contact_list_id
    )

    return campaign


def main():
    """
    Main function to run the time adjustment reminder script.
    """

    try:
        db = Database()
        with db.get_new_session() as session:
            # Retrieve the pay period for the previous week
            pay_period = fetch_pay_period(session)

            # Get worker IDs with missing punches
            worker_ids = get_missing_punch_data(session, pay_period)

            # Process contacts
            api_connector = APIConnector(token=API_KEY, brand_id=BRAND_ID)
            contact_ids = process_contacts(api_connector, worker_ids)

            if not contact_ids:
                return

            # Create a campaign for the contacts with missing punches
            create_campaign(api_connector, pay_period, contact_ids)
    except Exception as e:
        raise e


if __name__ == "__main__":
    main()
