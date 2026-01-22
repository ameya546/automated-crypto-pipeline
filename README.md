# Automated Crypto ELT Pipeline

**Project Overview**
This project is a real-time data pipeline that extracts live cryptocurrency market data, loads it into a local SQL Server data warehouse, and visualizes volatility in Power BI.

**Architecture**
* **Extract:** Python script (`requests`) fetches live JSON data from the CoinGecko API.
* **Load:** Data is cleaned and inserted into Microsoft SQL Server using `pyodbc`.
* **Automation:** The pipeline runs on a 60-second continuous loop for high-frequency tracking.
* **Visualize:** Power BI connects via DirectQuery/Import to monitor price trends.

**Tech Stack**
* Python (Requests, PyODBC)
* Microsoft SQL Server (SSMS)
* Power BI (DAX, Data Modeling)
