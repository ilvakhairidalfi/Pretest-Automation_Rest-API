import requests                     # Library untuk HTTP request (GET, POST, PUT, DELETE)
import pytest                       # Library untuk menjalankan testing otomatis
import uuid                         # Library untuk membuat email unik

# Konfigurasi
API_URL = "https://gorest.co.in/public-api/users"  # URL endpoint utama
TOKEN = "Bearer f657c28fb22ca92eff3fb06650de41bf996d4cc1d54f2f0be5ba7f08410f52f7"  # Token akses API

headers = {
    "Authorization": TOKEN,              # Token otorisasi
    "Content-Type": "application/json"   # Format request dalam JSON
}

# Fungsi generate email acak
def generate_unique_email():
    return f"ilva.auto.{uuid.uuid4().hex[:6]}@example.com"  # Prefix email diganti jadi ilva

# Data dasar user
base_user_data = {
    "name": "Ilva Automation",  # Nama user diganti jadi Ilva
    "gender": "Female",         # Gender disesuaikan kalau mau
    "status": "Active"
}

# File untuk menyimpan sementara user_id antar test
USER_ID_FILE = ".user_id.txt"

# Fungsi bantu simpan ID user ke file
def save_user_id(user_id):
    with open(USER_ID_FILE, "w") as f:
        f.write(str(user_id))

# Fungsi bantu ambil ID user dari file
def load_user_id():
    with open(USER_ID_FILE, "r") as f:
        return f.read().strip()

# ----------------- TEST PER STEP -----------------

def test_create_user_step():
    """Langkah 1: Membuat user baru (Ilva)"""
    data_user = base_user_data.copy()
    data_user["email"] = generate_unique_email()

    response = requests.post(API_URL, headers=headers, json=data_user)
    print("Create user response:", response.status_code, response.text)

    assert response.status_code == 200
    assert response.json().get("code") == 201

    user_id = response.json()["data"]["id"]   # Simpan ID user
    save_user_id(user_id)                     # Tulis ke file .user_id.txt

def test_create_user_negative():
    """Negative test: gagal karena email tidak valid"""
    invalid_data = base_user_data.copy()     # Salin data dasar
    invalid_data["email"] = "invalid_email"  # Masukkan email tidak valid

    response = requests.post(API_URL, headers=headers, json=invalid_data)  # Kirim POST request
    print("Negative create response:", response.status_code, response.text) # Cetak hasil response

    assert response.status_code == 200          # Server tetap akan balas HTTP 200
    assert response.json().get("code") == 422   # Tapi response code-nya 422 = validation error

def test_get_user_step():
    """Langkah 2: Ambil detail user Ilva dari ID yang sudah dibuat"""
    user_id = load_user_id()  # Ambil user ID dari file
    response = requests.get(f"{API_URL}/{user_id}", headers=headers)
    print("Get user response:", response.status_code, response.text)

    assert response.status_code == 200
    assert response.json().get("code") == 200
    assert str(response.json()["data"]["id"]) == user_id  # Cocokkan ID-nya / nanti ambil ke user_id.txt

def test_update_user_step():
    """Langkah 3: Update data user Ilva"""
    user_id = load_user_id()  # Ambil ID dari file
    update_data = {"name": "Ilva Updated"}  # Data baru

    response = requests.put(f"{API_URL}/{user_id}", headers=headers, json=update_data)
    print("Update user response:", response.status_code, response.text)

    assert response.status_code == 200
    assert response.json().get("code") == 200
    assert response.json()["data"]["name"] == "Ilva Updated"

def test_delete_user_step():
    """Langkah 4: Hapus user Ilva"""
    user_id = load_user_id()  # Ambil ID dari file

    response = requests.delete(f"{API_URL}/{user_id}", headers=headers)
    print("Delete user response:", response.status_code, response.text)

    assert response.status_code == 200
    assert response.json().get("code") == 204  # Delete berhasil