
# Financial Data Pipeline
# Introduction
This project is an 8-week internship where we built a robust data pipeline for collecting, processing, and analyzing financial data from various sources including stocks, forex, and cryptocurrencies.

# Project Overview
The financial data pipeline consists of multiple microservices orchestrated to work seamlessly. The primary components include:

Data Ingestion Service: Fetches financial data from different sources.
Data Processing Service: Processes the fetched data, applies analytics, and performs sentiment analysis on news data.
Data Storage Service: Stores the processed data efficiently in a PostgreSQL database.
API Endpoint Service: Exposes endpoints for clients to query and retrieve specific financial data.

# Technologies Used

Programming Languages: Python (main language), SQL

Microservices Architecture: Docker, Docker Compose

Workflow Orchestration: Apache Airflow

Data Storage: PostgreSQL

Data Processing and Analysis: Pandas, Scikit-Learn

Sentiment Analysis: NLP tools, Sentiment analysis libraries

Version Control: Git

Setup and Usage

To set up and run the financial data pipeline, follow these steps:

Clone this repository.

Install Docker and Docker Compose.

Run docker-compose up to start the services.

Detailed setup instructions and usage guidelines can be found in the respective service directories.

# Directory Structure
**gras** /data_ingestion: Contains the data ingestion service code.
**gras**/data_processing: Contains the data processing service code.
**gras**/data_storage: Contains the data storage service code.
**gras**/api_endpoint: Contains the API endpoint service code.
Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Contact
For any inquiries or feedback, contact us at your-email@example.com.
