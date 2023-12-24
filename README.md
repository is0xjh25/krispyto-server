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
Welcome to the backend repository of the Crypto Price Analysis project! Here, you'll discover the server-side implementation of a system dedicated to analyzing historical crypto prices and delivering pertinent data through a RESTful API. Developed using Python and Flask, it employs a structured architecture with controllers and models utilizing Object–Relational Mapping. The deployment is seamlessly handled through Amazon Web Services (AWS). This readme comprehensively outlines the API endpoints and details the phases of structuring the database, development, and deployment. Feel free to explore the website and the backend server repository using the links provided below.
> - _[Krispyto's Website](url)_
> - _[Krispyto's Web Server](https://github.com/is0xjh25/krispyto-web)_

## API Endpoints
### 1. Search Crypto Prices
- **Endpoint:** `/dashboard`
- **Method:** `GET`
- **Description:** Retrieve historical crypto prices based on specified parameters.
- **Parameters:**
  - `id` (string, required): ID of the currency to retrieve prices for.
  - `date` (string, required, default: '2022-10-9'): Date to filter prices.
  - `order_by` (string, required, default: 'crypto', enum: ['crypto', 'price', '24h', '7d', '1m', '24h-volume', 'market_cap']): Attribute to order results by.
  - `order_type` (string, required, default: 'desc', enum: ['asc', 'desc']): Order results in 'asc' (ascending) or 'desc' (descending) order.
- **Responses:**
  - `200`: Search results matching criteria.
  - `204`: No data available.
  - `400`: Bad input parameter.
  - `404`: Bad request.
  - `500`: Database connection error.
- **Example:**
  - `[GET] http://localhost:5000/dashboard?id=all&date=2022-12-24&order_by=price&order_type=desc`
  - `[GET] http://localhost:5000/dashboard?id=btc,aave&date=2021-11-9&order_by=1m&order_type=asc`
### 2. Search Crypto Exists In Database
- **Endpoint:** `/search`
- **Method:** `GET`
- **Description:** Retrieve the name of a specific currency by name.
- **Parameters:**
  - `name` (string, required): Name or symbol of the currency to retrieve.
- **Responses:**
  - `200`: Crypto found.
  - `204`: No data available.
  - `400`: Bad input parameter.
  - `404`: Bad request.
  - `500`: Database connection error.
- **Example:**
  - `[GET] http://localhost:5000/search?name=Bitcoin`
  - `[GET] http://localhost:5000/search?name=btc`
 
> _To explore the API documentation and test its functionality, please visit this [SwaggerHub](https://app.swaggerhub.com/apis/is0xjh25/Krispyto/1.0.0) link._  
## Development and Technologies
  ### 1. Server
  - **Language =>** Python
  - **Framework =>** Flask
  - **Hosting =>** AWS
  - **API =>** RESTful API meticulously documented using Swagger
  ### 2. Database
  - **Type =>** SQL
  - **Database System =>** PostgreSQL
  - **Hosting =>** AWS RDS
  - **Schema**
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
    
  - **ORM =>** Utilizing SQLAlchemy, seamlessly integrated with Flask in Python
  - **Migration**
    ```shell
    > flask db init
    > flask db migrate -m "Create Currency and Record tables"
    > flask db upgrade
    ```
    > Before running migration, please comment out the following line in the `create_app` function in `app/__init__.py`:
    ```python
      def create_app(config_class=Config):
          app = Flask(__name__)
          app.config.from_object(config_class)

          db.init_app(app)
          migrate.init_app(app, db)
    
          inspect_database(app) # Comment out the line below before migration

      return app
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
  ### 1. AWS
  ### 2. Docker
  ### 3. Virtulenv
  
## Advanced Solution
## Developed By
- The application is developed by _[is0xjh25 (Yun-Chi Hsiao)](https://is0xjh25.github.io)_.
- Special thanks to the _[Greythorn Team](https://greythorn.com)_ for providing this coding challenge and their guidance throughout the development process. 
<br/>
<p align="left">
  <img alt="Favicon" src="images/is0-favicon.png" width="250" >
