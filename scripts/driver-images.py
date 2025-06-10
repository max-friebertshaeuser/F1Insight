import os
import requests

# List of 2025 F1 drivers with their details
drivers = [
    {"first_name": "Lando", "last_name": "Norris", "number": "04"},
    {"first_name": "Oscar", "last_name": "Piastri", "number": "81"},
    {"first_name": "Max", "last_name": "Verstappen", "number": "01"},
    {"first_name": "George", "last_name": "Russell", "number": "63"},
    {"first_name": "Charles", "last_name": "Leclerc", "number": "16"},
    {"first_name": "Lewis", "last_name": "Hamilton", "number": "44"},
    {"first_name": "Kimi", "last_name": "Antonelli", "number": "12"},
    {"first_name": "Alexander", "last_name": "Albon", "number": "23"},
    {"first_name": "Isack", "last_name": "Hadjar", "number": "06"},
    {"first_name": "Esteban", "last_name": "Ocon", "number": "31"},
    {"first_name": "Nico", "last_name": "Hulkenberg", "number": "27"},
    {"first_name": "Lance", "last_name": "Stroll", "number": "18"},
    {"first_name": "Carlos", "last_name": "Sainz", "number": "55"},
    {"first_name": "Pierre", "last_name": "Gasly", "number": "10"},
    {"first_name": "Yuki", "last_name": "Tsunoda", "number": "22"},
    {"first_name": "Oliver", "last_name": "Bearman", "number": "87"},
    {"first_name": "Liam", "last_name": "Lawson", "number": "30"},
    {"first_name": "Fernando", "last_name": "Alonso", "number": "14"},
    {"first_name": "Gabriel", "last_name": "Bortoleto", "number": "05"},
    {"first_name": "Jack", "last_name": "Doohan", "number": "07"},
    {"first_name": "Franco", "last_name": "Colapinto", "number": "20"}
]

# Base URL for driver images
base_url = "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/"

# Directory to save images
output_dir = "f1_driver_images"
os.makedirs(output_dir, exist_ok=True)

# Download each driver's image
for driver in drivers:
    first_name = driver["first_name"]
    last_name = driver["last_name"]
    number = driver["number"]

    driver_code = (first_name[:3] + last_name[:3] + number).upper()
    driver_code_lower = driver_code.lower()
    surname_initial = last_name[0].upper()
    full_name = f"{first_name}_{last_name}"

    image_url = f"{base_url}/{surname_initial}/{driver_code}_{full_name}/{driver_code_lower}.png"
    output_path = os.path.join(output_dir, f"{driver_code_lower}.png")

    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Downloaded {full_name} as {driver_code_lower}.png")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download {full_name} ({driver_code_lower}): {e}")
