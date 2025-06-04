"""
Main module of the time adjustment reminder script.
"""
from res.db.db_functions import (
    get_pay_period_by_start_date,
    get_worker_ids_with_missing_punches_by_pay_period
)
from res.db.database import Database
from res.date_util import DateUtil


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
            get_missing_punch_data(session, pay_period)

    except Exception as e:
        raise e


if __name__ == "__main__":
    main()
