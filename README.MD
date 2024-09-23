# Library Database Report

## Overview

This project includes a Python script that interacts with a SQLite database (`library.db`) to generate various reports about books and authors. The script performs the following tasks:

1. Retrieves the book with the most pages.
2. Calculates the average page quantity of books.
3. Finds the youngest author based on birth date.
4. Lists authors who do not have any books.
5. Identifies authors who have written three or more books.

The results are saved into an Excel file (`report.xlsx`) and printed to the console.

## Installation

### Prerequisites

- Python 3.x
- Required Python packages: `pandas`, `Faker`, `SQLAlchemy`, `openpyxl`, `sqlite3` (included in the Python standard library)


## Usage

1. Run the Python script:

    ```bash
    python create_db.py
   python generate_data.py
   python main.py
    ```

3. The script will generate an Excel file named `report.xlsx` containing the report and print results to the console.


## Usage With SQLAlchemy

   ```bash
      pip install -r requirements.txt

      python using_sqlalchemy.py
   ```