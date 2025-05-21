"""
This module contains integration tests for the database functions.
"""
from res.db.db_functions import (
    get_all_employees,
    get_employee_by_associate_id,
    get_employee_by_worker_id,
)
from res.db.models import Employee


class TestDBFunctionsIntegration:
    """
    Integration tests for the database functions.
    """

    def test_get_all_employees(self, db_session, valid_employee: Employee):
        """
        Test that all employees can be retrieved from the database.
        """
        db_session.add(valid_employee)
        db_session.commit()
        employees = get_all_employees(db_session)

        assert len(employees) > 0, "No employees found in the database."
        assert employees[0].associate_id == valid_employee.associate_id

    def test_get_employee_by_associate_id(self, db_session, valid_employee: Employee):
        """
        Test that an employee can be retrieved by associate ID.
        """
        db_session.add(valid_employee)
        db_session.flush()
        employee = get_employee_by_associate_id(db_session, valid_employee.associate_id)

        assert employee is not None, "Employee not found in the database."
        assert employee.associate_id == valid_employee.associate_id
        assert employee.first_name == valid_employee.first_name
        assert employee.last_name == valid_employee.last_name

    def test_get_employee_by_worker_id(self, db_session, valid_employee: Employee):
        """
        Test that an employee can be retrieved by worker ID.
        """
        db_session.add(valid_employee)
        db_session.flush()
        employee = get_employee_by_worker_id(db_session, valid_employee.worker_id)

        assert employee is not None, "Employee not found in the database."
        assert employee.worker_id == valid_employee.worker_id
        assert employee.first_name == valid_employee.first_name
        assert employee.last_name == valid_employee.last_name
