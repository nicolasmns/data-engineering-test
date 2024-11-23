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
git clone https://github.com/nicolasmns/data-engineering-test
git checkout solution-assignment
cd solution
```

### Step 2: Start the Docker Containers

Build the Docker images and start the containers using the following command:

```bash
docker-compose up --build -d
```

This will:
* Build the Python environment with all necessary dependencies (managed by Poetry).
* Start a PostgreSQL database (used for Task 4).

### Step 3: Connect to the Docker container

```bash
docker exec -it python_app bash
```

### Step 4: Execute the Tasks
Each task is implemented as a standalone script or function. Below are the instructions to execute each task:

#### Task 1: Distribution of Crate Types Per Company
Run the script to calculate the distribution of crate types per company:
```bash
python src/task_1/crate_distribution.py
```

#### Task 2: DataFrame of Orders with Full Name of the Contact
Run the script to create a DataFrame with order IDs and full contact names:
```bash
python src/task_2/contact_fullname.py
```

#### Task 3: DataFrame of Orders with Contact Address
Run the script to create a DataFrame with order IDs and contact addresses:
```bash
python src/task_3/contact_address.py
```

#### Task 4: Calculation of Sales Team Commissions
```bash
python src/task_4/task_4_comissions.py
```
This script will:

- Retrieve the files from the src/resources directory.
- Insert the data from orders.csv and invoicing_data.json into their respective tables.
- Runs DBT to create the calculate_commissions view.

#### Task 5: DataFrame of Companies with Sales Owners
Run the script to generate a DataFrame of companies with their sales owners:
```bash
python src/task_5/company_sales_owners.py
```

### Step 5: Run Unit Tests
To validate the implementation, run the unit tests:

```bash
pytest
```

### Step 6: Check coverage
```bash
pytest --cov=src --cov-report=term-missing
```
---

## Notebooks for Each Task

Each task has a corresponding PDF that provides a detailed explanation of the implementation:

- **Task 1**: [notebook_task_1_analysis](https://github.com/nicolasmns/data-engineering-test/tree/solution-assignment/solution/notebooks/notebook_task_1_analysis.ipynb)
- **Task 2**: [notebook_task_2_analysis](https://github.com/nicolasmns/data-engineering-test/tree/solution-assignment/solution/notebooks/notebook_task_2_analysis.ipynb)
- **Task 3**: [notebook_task_3_analysis](https://github.com/nicolasmns/data-engineering-test/tree/solution-assignment/solution/notebooks/notebook_task_3_analysis.ipynb)
- **Task 4**: [notebook_task_4_analysis](https://github.com/nicolasmns/data-engineering-test/tree/solution-assignment/solution/notebooks/notebook_task_4_analysis.ipynb)
- **Task 5**: [notebook_task_5_analysis](https://github.com/nicolasmns/data-engineering-test/tree/solution-assignment/solution/notebooks/notebook_task_5_analysis.ipynb)

These ipynb are located in the `notebooks/` folder and are provided to help you understand each task's implementation and results, additionally I added some plots to help understand the data.

To open Jupyter, inside the container you can execute the following command:

```bash
PYTHONWARNINGS="ignore" jupyter notebook --allow-root --ip=0.0.0.0 --port=8888
```
This will print in the terminal a link with a token, something like:

```bash
    To access the server, open this file in a browser:
        file:///root/.local/share/jupyter/runtime/jpserver-15-open.html
    Or copy and paste one of these URLs:
        http://0f30fc02d8ff:8888/tree?token=<your_token>
        http://127.0.0.1:8888/tree?token=<your_token>
```
---

## Notes
#### DBT and PostgreSQL:

* DBT is used to model and compute the calculation of commissions, requiring PostgreSQL to be populated with data before running DBT.

#### Jupyter Notebooks:

* If you prefer to explore the tasks interactively, Jupyter notebooks are available. you can run them locally if needed.

#### Docker:
* Docker ensures that all dependencies, including Poetry, PostgreSQL, and DBT, are automatically installed and managed within isolated containers.