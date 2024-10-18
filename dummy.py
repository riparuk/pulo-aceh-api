import requests
from faker import Faker
import random

# Inisialisasi Faker
fake = Faker()

# URL endpoint FastAPI
url = "http://localhost:8000/places/"  # Ganti dengan endpoint yang sesuai

# Token yang didapat dari proses login
token = "Bearer YOUR_ACCESS_TOKEN"  # Ganti dengan token yang valid dari admin login

# Fungsi untuk membuat data dummy untuk PlaceCreate
def create_dummy_place():
    return {
        "name": fake.company(),
        "description": fake.text(),
        "location_name": fake.city(),
        "latitude": float(fake.latitude()),  # Convert Decimal to float
        "longitude": float(fake.longitude()),  # Convert Decimal to float
        "rating": random.uniform(1, 5),  # Assuming rating is a float between 1 and 5
        "image_url": fake.image_url()
    }

# Mengirimkan data dummy ke FastAPI
def send_dummy_data(num_places):
    headers = {
        "Authorization": token,  # Menambahkan token di header
        "Content-Type": "application/json"
    }
    
    for _ in range(num_places):
        place_data = create_dummy_place()
        response = requests.post(url, json=place_data, headers=headers)
        
        if response.status_code == 201:  # Cek jika berhasil
            print(f"Place created: {place_data}")
        else:
            print(f"Failed to create place: {response.text}")

# Mengirimkan 10 data dummy
send_dummy_data(10)