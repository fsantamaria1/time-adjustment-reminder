"""
Main module of the time adjustment reminder script.
"""
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
