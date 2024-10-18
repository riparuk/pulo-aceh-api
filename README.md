# Smeltub-API
API System for Collecting Gas Data Sensor

## Installation
To install and run the Smeltub-API project, follow these steps:

1. Clone the repository to your local machine:

    ```shell
    git clone https://github.com/riparuk/pulo-aceh-api.git
    ```

2. Navigate to the project directory:

    ```shell
    cd pulo-aceh-api
    ```

3. Create a virtual environment and activate it:

    ```shell
    python3 -m venv venv
    source venv/bin/activate
    ```

4. Install the required dependencies:

    ```shell
    pip install -r requirements.txt
    ```

5. Copy `.env.example` to `.env` and fill the key

## Running the Application

To run the API project, execute the following command:

```shell
fastapi dev app/main.py
```

This will start the FastAPI development server and reload the application whenever changes are made.

You can now access the API at `http://localhost:8000`.
