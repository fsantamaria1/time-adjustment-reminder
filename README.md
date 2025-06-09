# Time Adjustment Reminder Script

This project is a Python-based script designed to automate the process of reminding employees to adjust their timecards. It integrates with a database and an external API to identify employees with missing punches and sends them reminders via a campaign.

## Features

- Fetches pay period data from a database.
- Identifies employees with missing punches for a specific pay period.
- Matches employees to contacts in an external API.
- Sends reminders via a campaign created in the external API.
- Logs all operations for auditing and debugging purposes.

## Requirements

- Python 3.9 or higher
- MS SQL Server
- ODBC Driver 17 for SQL Server

### Python Dependencies

The required Python packages are listed in the `requirements.txt` file:

```plaintext
python-dotenv~=1.0.1
SQLAlchemy~=2.0.37
pyodbc~=5.2.0
requests~=2.32.3
```


### Setup

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2. Install the dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```
3. Configure the `.env` file or environment variables with your database credentials, API key, and other settings. Use the `.env.example` file as a template:
    ```plaintext
    DB_SERVER='your_server'
    DB_USERNAME='your_username'
    DB_PASSWORD='your_password'
    DB_NAME='your_database'
    DB_SCHEMA='your_schema'
    SLICK_TEXT_API_KEY='your_api_key'
    SLICK_TEXT_BRAND_ID='your_brand_id'
    ```
4. Ensure the MS SQL Server is accessible and the required database schema and tables exist.

5. Run the script:
    ```bash
    python main.py
    ```

### Usage

The script performs the following steps:
- Retrieves the pay period for the previous week.
- Identifies employees with missing punches for the pay period.
- Matches employees to contacts in the external API.
- Sends reminders to the matched contacts via a campaign.

### Logging

The script logs all operations to a file named `time_adjustment.log` and also outputs logs to the console.

### Testing

Unit and integration tests are provided to ensure the functionality of the script. To run the tests, use `pytest`:

```bash
pytest tests/unit
```
```bash
pytest tests/integration
```

### Project Structure

```plaintext
.
├── main.py                  # Main script to execute the workflow
├── res/
│   ├── db/

│       ├── database.py      # Database session and engine management
│       ├── db_functions.py  # Functions to interact with the database
│       ├── models.py            # Data models for the application
│   ├── api.py               # API connector for external API
│   ├── date_util.py         # Utility functions for date operations
├── tests/
│   ├── integration/
│       ├── api_test.py  # Integration tests for API connector
│       ├── conftest.py  # Configuration for integration tests
│       ├── database_test.py  # Integration tests for database interactions
│       ├── db_functions_test.py  # Integration tests for database functions
│       ├── models_test.py  # Integration tests for data models
│   ├── unit/
│       ├── api_test.py      # Unit tests for API connector
│       ├── config_test.py  # Unit tests for configuration management
│       ├── database_test.py   # Unit tests for database module
│       ├── date_util_test.py  # Unit tests for date utilities
│       ├── models_test.py  # Unit tests for data models
├── .env                     # Environment variables (not included in version control)
├── .env.example             # Example environment variables file
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── time_adjustment.log      # Log file (generated during execution)
```

### Example Output

The script logs the following information:
- Pay period details (start and end dates).
- List of employees with missing punches.
- Contacts matched to employees.
- Campaign creation details.
