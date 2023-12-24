# Krispyto's Server
<p align="left">
  <img alt="Logo" src="images/krispyto-logo.png" width="450" >
  
## Table of Contents
* [Overview](#overview)
* [API Endpoints](#api-endpoints)
* [Deveploment and Technologies](#development-and-technologies)
* [Deployment](#deployment)
* [Advanced Solution](#advanced-solution)
* [Developed By](#developed-by)
  
## Overview
Welcome to the backend repository for the Crypto Price Analysis project. This repository contains the server-side implementation of a system that analyzes historical crypto prices and provides relevant data through a RESTful API.

## API Endpoints
## Development and Technologies
  ### 1. Server
  - Language: Python
  - Framework: Flask
  - Hosting: AWS
  - API: RESTful API meticulously documented using Swagger
  ### 2. Database
  - Type: SQL
  - Database System: PostgreSQL
  - Hosting: AWS RDS
  - Schema:
    | Currency Table  |           | Record Table           |           |
    |-----------------|-----------|------------------------|-----------|
    | id (PK)         | Integer   | id (PK)                | Integer   |
    | name            | String(50)| currency_id (FK)       | Integer   |
    | symbol          | String(10)| date                   | DateTime  |
    |                 |           | high                   | Float     |
    |                 |           | low                    | Float     |
    |                 |           | open                   | Float     |
    |                 |           | close                  | Float     |
    |                 |           | volume                 | Float     |
    |                 |           | marketcap              | Float     |
    
  - ORM: Utilizing SQLAlchemy, seamlessly integrated with Flask in Python
  - Migration:
    ```
    > flask db init
    > flask db migrate -m "Create Currency and Record tables"
    > flask db upgrade
    ```
  ### 3. Testing
  ### 4. Security
  - Environment Variables
    - Ensure the security of your application by handling sensitive information through environment variables.
    - A crucial step is to create an `.env` file to store sensitive configuration details.
  - Sample .env Configuration
  ```dotenv
  DB_ENDPOINT="your_database_endpoint"

  DB_USERNAME="your_database_username"

  DB_PASSWORD="your_database_password"

  DB_NAME="your_database_name"

  GOOGLE_FILE_ID="your_google_file_id"

  CSV_FILE_FOLDER="your_csv_file_folder"
  ```
- Protect the Credentials
  - Never expose your .env file publicly or commit it to version control systems.
  - Add the .env file to the .gitignore to prevent accidental exposure.

## Deployment
  ### 1. Virtulenv
  ### 2. Docker
  ### 3. AWS
## Advanced Solution
## Developed By
- The application is developed by _[is0xjh25 (Yun-Chi Hsiao)](https://is0xjh25.github.io)_.
- Special thanks to the _[Greythorn Team](https://greythorn.com)_ for providing this coding challenge and their guidance throughout the development process. 
<br/>
<p align="left">
  <img alt="Favicon" src="images/is0-favicon.png" width="250" >
