"""
Main module of the time adjustment reminder script.
"""
import os
import sys
from res.api import APIConnector
from res.db.db_functions import (
    get_pay_period_by_start_date,
    get_worker_ids_with_missing_punches_by_pay_period
)
from res.db.database import Database
from res.date_util import DateUtil

# Create a new database session
db = Database()
session = db.get_new_session()

# Get the pay period for the previous week
last_monday = DateUtil().get_last_monday()
previous_week_pay_period = get_pay_period_by_start_date(
    session,
    last_monday
)

# Get employees with missing punches for the previous week's pay period
worker_ids_with_missing_punches = get_worker_ids_with_missing_punches_by_pay_period(
    session,
    previous_week_pay_period.pay_period_id
)

# Get the environment variables for API key and brand ID
API_KEY = os.getenv("SLICK_TEXT_API_KEY")
if not API_KEY:
    raise ValueError("SLICK_TEXT_API_KEY environment variable is not set.")
BRAND_ID = os.getenv("SLICK_TEXT_BRAND_ID")
if not BRAND_ID:
    raise ValueError("SLICK_TEXT_BRAND_ID environment variable is not set.")

# Initialize the API connector
api_connector = APIConnector(token=API_KEY, brand_id=BRAND_ID)

# Fetch all contacts from the API
contacts = api_connector.get_all_contacts(brand_id=BRAND_ID)

# Filter contacts to find those with missing punches
contact_IDs = []
for contact in contacts:
    contact_id = contact.get('contact_id')
    first_name = contact.get('first_name')
    last_name = contact.get('last_name')
    email = contact.get('email')
    phone_number = contact.get('mobile')
    worker_id = contact.get('custom_fields', {}).get('adp_associate_id', None)

    if worker_id in worker_ids_with_missing_punches:
        # Add the contact ID to the list
        contact_IDs.append(contact_id)

# If no contacts with missing punches are found, exit the script
if not contact_IDs:
    sys.exit()

# Create a new contact list for the campaign
CONTACT_LIST_AND_CAMPAIGN_NAME = (f"Time Adjustment Reminder "
                                  f"{previous_week_pay_period.pay_period_start} - "
                                  f"{previous_week_pay_period.pay_period_end}")
new_contact_list = api_connector.create_contact_list(CONTACT_LIST_AND_CAMPAIGN_NAME)
contact_list_id = new_contact_list.get("contact_list_id")

# Add the contact IDs to the new list
api_connector.add_contacts_to_list(contact_IDs, contact_list_id)

# Define the message content for the campaign
MESSAGE_CONTENT = """
Good morning,

This is a reminder that a time adjustment is needed on your timecard.
Please review your ADP timecard and enter a KPA Time adjustment as soon as possible, if you haven't already done so.

Thanks!

"""

# Create the campaign with the specified message content
new_campaign = api_connector.create_campaign(
    CONTACT_LIST_AND_CAMPAIGN_NAME,
    MESSAGE_CONTENT,
    contact_list_id
)

campaign_id = new_campaign.get("campaign_id")
