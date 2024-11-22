# IFCO Data Engineering Challenge

This repository contains solutions for the **IFCO Data Engineering Challenge**, covering Tests 1 through 5. The project leverages **Python**, **PostgreSQL**, **DBT**, and **Docker** to provide a complete, reproducible environment for data analysis and computation.

---

### **Problem Statement**

You have been assigned the responsibility of assisting IFCO's Data Team in analyzing business data. For this purpose, you have been provided with two files:

- **orders.csv**: Contains factual information regarding the orders received.
- **invoicing_data.json**: Contains invoicing information.

### **Tests Implemented**

I've renamed each Test to 'Task' to differentiate them from the actual unit tests.

- **Task 1**: Calculate the distribution of crate types per company.
- **Task 2**: Create a DataFrame of orders with the full name of the contact.
- **Task 3**: Create a DataFrame of orders with contact addresses.
- **Task 4**: Compute sales team commissions based on business rules.
- **Task 5**: Create a DataFrame of companies with their sales owners.

---

## **Setup Instructions**

This project uses **Docker** to ensure all dependencies and services (like PostgreSQL) are properly configured and isolated. Follow these steps to set up the project:

---

### Step 1: Clone the Repository

Start by cloning this repository to your local machine:
```bash
git clone https://github.com/nicolasmns/data-engineering-test/tree/solution-assignment
git checkout solution-assignment
cd  solution
```

### Step 2: Start the Docker Containers

Build the Docker images and start the containers using the following command:

```bash
docker-compose up --build
```

This will:
* Build the Python environment with all necessary dependencies (managed by Poetry).
* Start a PostgreSQL database (used for Task 4).

### Step 3: Execute the Tasks
Each test is implemented as a standalone script or function. Below are the instructions to execute each test:

#### Task 1: Distribution of Crate Types Per Company
Run the script to calculate the distribution of crate types per company:
```bash
docker exec -it python_app poetry run python src/task_1/crate_distribution.py
```

#### Task 2: DataFrame of Orders with Full Name of the Contact
Run the script to create a DataFrame with order IDs and full contact names:
```bash
docker exec -it python_app poetry run python src/task_2/contact_fullname.py
```

#### Task 3: DataFrame of Orders with Contact Address
Run the script to create a DataFrame with order IDs and contact addresses:
```bash
docker exec -it python_app poetry run python src/task_3/contact_address.py
```

#### Task 4: Calculation of Sales Team Commissions
###### Step 1: Load Data into PostgreSQL
Execute the data loading script to populate the database:

```bash
docker exec -it python_app poetry run python src/task_4/load_data.py
```
This script will:

- Parse the data from orders.csv and invoicing_data.json.
- Create the necessary tables in the PostgreSQL database.
- Insert the parsed data into the respective table

###### Step 2: Execute DBT to Calculate Commissions
Once the data is loaded, run DBT to perform the calculations:
```bash
docker exec -it python_app poetry run dbt run --project-dir src/task_4/dbt
```

#### Task 5: DataFrame of Companies with Sales Owners
Run the script to generate a DataFrame of companies with their sales owners:
```bash
docker exec -it python_app poetry run python src/task_5/company_salesowners.py
```

### Step 5: Run Unit Tests
To validate the implementation, run the unit tests:

```bash
docker exec -it python_app poetry run pytest
```

### Step 6: Check coverage
```bash
docker exec -it python_app poetry --cov=src -cov-report=term-missing
```
---

## Notebooks for Each Task

Each task has a corresponding PDF that provides a detailed explanation of the implementation:

- **Task 1**: [task_1_crate_distribution.pdf](path_to_pdf)
- **Task 2**: [task_2_contact_fullname.pdf](path_to_pdf)
- **Task 3**: [task_3_contact_address.pdf](path_to_pdf)
- **Task 4**: [task_4_commissions.pdf](path_to_pdf)
- **Task 5**: [task_5_company_salesowners.pdf](path_to_pdf)

These PDFs are located in the `notebooks/` folder and are provided to help you understand each task's implementation and results.

---

## Notes
#### DBT and PostgreSQL:

* DBT is used to model and compute commissions, requiring PostgreSQL to be populated with data before running DBT. Make sure to load the data before running DBT.

#### Jupyter Notebooks:

If you prefer to explore the tasks interactively, Jupyter notebooks are available. You can check them as PDFs or run them locally if needed.

#### Docker:
Docker ensures that all dependencies, including Poetry, PostgreSQL, and DBT, are automatically installed and managed within isolated containers.