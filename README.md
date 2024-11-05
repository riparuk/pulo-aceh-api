# Pulo Aceh API
API System for Pulo Aceh Destination

## Quick Guide

- Register at `/users/auth/register`. To register as an admin, include `"is_admin": true` and fill `secret_key` same as in .env file.
- Only admins can view sensitive data or add data such as places.
- Start login by clicking the authorize button at the top right of the Swagger API for easy access to other endpoints (automatically adds access token to the header).
- Edit the token (result from `/users/auth/login`) in `dummy.py` and run it to easily create fake place data.

## Installation
To install and run the API project, follow these steps:

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

## Runnnig the Application with Docker

To run the API project using Docker, follow these steps:

1. Build the Docker image:

    ```shell
    docker build -t pulo-aceh-api .
    ```

    This command will create a Docker image named `pulo-aceh-api` based on the Dockerfile in the current directory.

2. Run the Docker container:

    ```shell
    docker run -d --name pulo-aceh-api -p 8000:8000 pulo-aceh-api
    ```

    This command will start a new container named `pulo-aceh-api` in detached mode, mapping port 8000 of the container to port 8000 on your host machine.

3. List running Docker containers:

    ```shell
    docker ps
    ```

    This command will display a list of all running Docker containers, allowing you to verify that `pulo-aceh-api` is running.

4. Stop the Docker container:

    ```shell
    docker stop pulo-aceh-api
    ```

    This command will stop the running `pulo-aceh-api` container.

5. Remove the Docker container:

    ```shell
    docker rm pulo-aceh-api
    ```

    This command will remove the stopped `pulo-aceh-api` container from your system.

    ## Checklist

    - [x] JWT Done
    - [x] OTP
    - [x] Register akun dengan OTP
    - [ ] Lupa Password dengan OTP
    - [ ] User bisa Ubah password
    - [ ] User bisa Ubah email OTP ke Email baru
    - [X] Upload gambar untuk update profile 
    - [X] Upload gambar tempat wisata 
    - [ ] Depend login atau belum saat akses endpoint masih bug/bad logic (harus login jika butuh get_current_user, tidak bisa hanya token/key)
    - [ ] User belum bisa kirim rating
    - [ ] Rating berdasarkan user rating