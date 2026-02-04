# Data Warehouse Project: Cybersecurity Incidents and Financial Impact
**A Star Schema implementation for analyzing global threats and economic losses.**

> **Author:** Giovanni Canedoli, Sapienza University of Rome

---

### Project Overview
This project implements a complete ETL (Extract, Transform, Load) pipeline to analyze cybersecurity threats. It transforms raw data into a star schema model to execute queries regarding attack types, geographic distribution, and the resulting financial losses.

### Description of the Dataset
The data warehouse integrates three primary datasets to provide a holistic view of the global cybersecurity landscape:

1. **Organization Data Breaches**: A comprehensive list of historical data breaches, detailing affected entities, the method of attack, and the total number of records compromised.
   Source: [Data Breaches Dataset (Kaggle)](https://www.kaggle.com/datasets/thedevastator/data-breaches-a-comprehensive-list)

2. **Cybersecurity Incidents**: Focused on the financial and administrative impact of net crimes, including metrics on total complaints and financial losses.
   Source: [Loss from Net Crime Dataset (Kaggle)](https://www.kaggle.com/datasets/huzpsb/cybersecurity-incidents-dataset)

3. **Global Cybersecurity Threats (2015-2024)**: Provides granular details on attack types, target industries, vulnerability types, and defense mechanisms.
Source: [Global Cybersecurity Threats Dataset (Kaggle)](https://www.kaggle.com/datasets/atharvasoundankar/global-cybersecurity-threats-2015-2024)
### Technical Architecture
These are the fact tables and the dimensions used in the datawarehouse:
- **Fact Tables:** `fact_cyber_incidents`, `fact_net_crime_stats`.
- **Dimension Tables:** `time_dimension`, `geography_dimension`, `attack_dimension`, `defense_dimension`, and `entity_dimension`.

---

### Run Project

#### 1. Prerequisites
Ensure you have Docker and Docker Compose installed on your system.

#### 2. Execution
To run the project, simply execute the following command in your terminal:
```shell
sudo docker compose up
```

#### 3. Access and Analysis
* **Interface**: Once the containers are running, navigate to [http://localhost:5050](http://localhost:5050) to access the pgAdmin 4 management interface.
* **Database Connection**: To connect pgAdmin to your database, right-click **"Servers" > "Register" > "Server..."**. Under the **"Connection"** tab, enter the following credentials:

| Field | Value |
| :--- | :--- |
| **Host name/address** | `db` |
| **Port** | `5432` |
| **Maintenance database** | `datawarehouse` |
| **Username** | `postgres` |
| **Password** | `postgres` |

> **Note**: You must use `db` as the host name because pgAdmin is communicating with the database over the internal Docker network.
* **Analytical Queries**: A collection of ROLAP queries (aggregations, drill-downs, and trend analysis) is available in `queries.sql`.

---

### Project Structure
* `load_data.sql`: Contains the DDL for staging, dimensions, and fact tables, as well as the logic for data transformation and insertion.
* `docker-compose.yml`: Orchestrates the PostgreSQL and pgAdmin containers.
* `data/`: Directory containing the CSV sources (later modifies by the main.py file in the docker container).

---
*Developed for the Data Management course at Sapienza University of Rome.*