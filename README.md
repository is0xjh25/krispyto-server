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
> - _[Krispyto's Website](http://13.239.27.73:3000)_
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
    
  - **Hosting =>** Amazon Elastic Container Service
    
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
    ```python
    # app/models.py
    
    db = SQLAlchemy()
    
    class Currency(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50))
        symbol = db.Column(db.String(10))
        records = db.relationship('Record', back_populates='currency')
    
    class Record(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
        date = db.Column(db.DateTime)
        high = db.Column(db.Float)
        low = db.Column(db.Float)
        open = db.Column(db.Float)
        close = db.Column(db.Float)
        volume = db.Column(db.Float)
        marketcap = db.Column(db.Float)
        currency = db.relationship('Currency', back_populates='records')
    ```
  - **Migration**
    ```shell
    > flask db init
    > flask db migrate -m "Create Currency and Record tables"
    > flask db upgrade
    ```
      > Before running migration, please comment out the following line in the `create_app` function in `app/__init__.py`:
    ```python
      # app/__init__.py
    
      def create_app(config_class=Config):
          app = Flask(__name__)
          app.config.from_object(config_class)

          db.init_app(app)
          migrate.init_app(app, db)
    
          inspect_database(app) if not app.config['TESTING'] else None  # Comment out before migration

      return app
      ```
  
  ### 3. Testing
  - **inspect_database() =>** The `inspect_database()` function in the Flask application uses SQLAlchemy's Inspector to assess the database status. It excludes the "alembic_version" table and raises an exception if no tables are found, indicating the need for migrations. The function verifies each table for data existence, initiating a process to download, extract, and upload data from [Google Drive](https://drive.google.com/file/d/1XBMlxjtyuAGdrfB0tPXDQT7H_qLIvJGF/view?usp=sharing) (supplied by the _[Greythorn Team](https://greythorn.com)_) if any table is empty. This ensures the database's integrity with essential information and concludes by printing a completion message.

    ```python
    # utilities/helper.py
    
    def inspect_database(app):

      with app.app_context():
          inspector = inspect(db.engine)
          table_names = inspector.get_table_names()
          table_names = [table for table in table_names if table != "alembic_version"]
    
          # Check if there are tables
          if not table_names:
              raise Exception("No tables found. Please run migrations first.")
  
          # Loop through all tables and check if each table has at least one row of data
          for table_name in table_names:
              query = text(f"SELECT 1 FROM {table_name} LIMIT 1")
              query_result = db.session.execute(query).fetchone()
              if query_result is None:
                  # Download and extract the data from Google Drive
                  download_and_extract_zip(app.config['GOOGLE_FILE_ID'], app.config['CSV_FILE_FOLDER'])
                  # Process data
                  read_files_and_upload(app, app.config['CSV_FILE_FOLDER'])
                  break
    ```
  - **Pytest**
    | **File**        | **Test Category**                 | **Test Description**                                           |
    |-----------------|----------------------------------|----------------------------------------------------------------|
    | **test_db.py**  | Database Connection Test         | The `test_database_connection` function ensures successful database connectivity.                                           |
    |                 | Empty Database Test               | The `test_database_empty` function checks if the database is not empty.                                                     |
    |                 | First Table Data Test             | The `test_first_table_has_data` function verifies that the first table has data.                                            |
    | **test_api.py** | Search Crypto Prices Tests        | `test_search_crypto_prices_all` tests searching crypto prices for all cryptocurrencies.                                    |
    |                 |                                  | `test_search_crypto_prices_favourite` tests searching crypto prices for a specific cryptocurrency (favorite).             |
    |                 |                                  | `test_search_crypto_prices_not_found` tests searching crypto prices with invalid parameters.                               |
    |                 | Search Crypto Existence Tests     | `test_search_crypto_exists_name` tests searching crypto existence by name.                                                  |
    |                 |                                  | `test_search_crypto_exists_symbol` tests searching crypto existence by symbol.                                              |
    |                 |                                  | `test_search_crypto_exists_name_not_found` tests searching for a non-existing crypto by name.                             |
    |                 | Bad Request Handling Test         | `test_bad_request` ensures proper handling of bad requests with a 404 status.                                               |

    > The app fixture in test_api.py orchestrates the establishment of a testing Flask app. This includes configuring a dedicated testing environment using the TestConfig class, which inherits from the base Config class. In this configuration, TESTING is set to True, and the SQLALCHEMY_DATABASE_URI is configured to use an in-memory SQLite database ('sqlite:///:memory:'). This setup ensures the creation of a lightweight database tailored for testing purposes, distinct from the main application's configuration.

- **Postman =>** Concerning Postman, which is utilized for API testing, it serves the purpose of testing the API against a live or real database. Additionally, it includes similar tests to those executed in the testing environment.

  > _To explore the API documentation and test its functionality, please visit this [Postman](https://api.postman.com/collections/17378533-074e5fc8-38fe-4099-917d-9f6faa5990b7?access_key=PMAT-01HJF3WYB2HGGNR1VBTXH93SEJ) link._  

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
  I leverage _[AWS Fargate](https://aws.amazon.com/fargate/)_, a serverless compute engine for containers, compatible with both _[Amazon Elastic Container Service (ECS)](https://aws.amazon.com/ecs/)_. I create the Dockerfile locally, push the image to the [Amazon Elastic Container Registry](https://aws.amazon.com/ecr/) using AWS CLI, and set up the service. This ensures both the API server and the frontend web server can be accessed publicly. For detailed instructions, refer to the article ["Deploying a Docker container with ECS and Fargate"](https://aws.plainenglish.io/deploying-a-docker-container-in-aws-using-fargate-5a19a140b018) by Esteban. Furthermore, the database is hosted on [Amazon RDS](https://aws.amazon.com/free/database/?trk=f8c749c2-a797-41e7-9b4d-743b10b206a3&sc_channel=ps&ef_id=Cj0KCQiAkKqsBhC3ARIsAEEjuJh1_2zTQF8FjZkweM1KxlXTQtH0rt2n1Aj_YvutO6p1EJGqzlCuYFoaAuGuEALw_wcB:G:s&s_kwcid=AL!4422!3!549058196825!p!!g!!aws%20sql%20database!11539887576!114142397722&gclid=Cj0KCQiAkKqsBhC3ARIsAEEjuJh1_2zTQF8FjZkweM1KxlXTQtH0rt2n1Aj_YvutO6p1EJGqzlCuYFoaAuGuEALw_wcB) as a SQL database server.

  > Now, you can access the mentioned API via http://3.26.53.87:8000

  > Example: `http://3.107.0.250:8000/search?name=BTC` would return `{"name":"Bitcoin","symbol":"BTC"}`
  ### 2. Docker
  Place the Docker file in the same directory and execute the following command.
  ```shell
  > docker build -t krispyto-server .  # Builds a Docker image with the tag "krispyto-server."
  > docker run -p 8000:8000 --env-file ./.env  # Runs a Docker container, mapping port 8000 and using environment variables from ".env."
  ```
  ```dockerfile
  # dockerfile

  # Use a base image
  FROM python:3.9
  
  # Set the working directory
  WORKDIR /app
  
  # Copy the application files
  COPY . . 
  
  ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL True
  
  # Install MPICH
  RUN apt-get update && apt-get install -y mpich
  RUN pip install --upgrade pip
  
  # Install dependencies from a list
  RUN pip install -r requirements.txt
  
  # Expose the application port
  EXPOSE 8000
  
  # Start the application
  CMD ["flask", "run","--host","0.0.0.0","--port","8000"]
  ```
  > To enhance security and facilitate dynamic configuration changes, exclude the .env file from the local project directory when building the Docker image. This ensures that sensitive information is not shipped with the image, and modifications to the database URL won't necessitate rebuilding the image.
  ### 3. Virtulenv
  All development occurs within the virtual environment, ensuring a stable environment with all required libraries and their versions listed in the [requirements.txt](/requirements.txt) file.
  ```shell
  > python3 -m venv venv        # Creates a virtual environment named "venv."
  > source venv/bin/activate    # Activates the virtual environment.
  > pip install --upgrade pip   # Upgrades the pip package manager.
  > pip install -r requirements.txt   # Installs dependencies listed in the "requirements.txt" file.
  > pip freeze > requirements.txt   # Freezes and saves the current package versions to "requirements.txt."
  ```
  
## Advanced Solution
### Overview
Incorporate an in-memory caching layer to boost performance and keep the AWS RDS database up-to-date.

### Components
1. **Application Layer:**
   - Interacts with caching layer and AWS RDS.

2. **Caching Layer:**
   - Uses Redis/Memcached.
   - Periodically updates cache from AWS RDS.
   - Handles cache misses by fetching from AWS RDS.

3. **AWS RDS (Original Database):**
   - Source of truth.
   - Continuously updated by caching layer.

### Operations
1. **Read:**
   - Check cache.
   - Cache hit: return data.
   - Cache miss: fetch from AWS RDS, update cache, return.

2. **Write:**
   - Write to cache and AWS RDS for consistency.

3. **Cache Update:**
   - Time intervals or triggered by events.
   - Eviction policies for cache management.

### Benefits
- **Improved Read Performance:** Caches frequently accessed data.
- **Data Consistency:** Updates both cache and database on writes.
- **Reduced Database Load:** Caching layer handles many read requests

## Developed By
- The application is developed by _[is0xjh25 (Yun-Chi Hsiao)](https://is0xjh25.github.io)_.
- Special thanks to the _[Greythorn Team](https://greythorn.com)_ for providing this coding challenge and their guidance throughout the development process. 
<br/>
<p align="left">
  <img alt="Favicon" src="images/is0-favicon.png" width="250" >
