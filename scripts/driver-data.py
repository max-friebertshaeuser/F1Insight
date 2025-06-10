import requests
import re
import json
import time

# List of drivers with their first and last names
drivers = [
    {"first_name": "Lando", "last_name": "Norris"},
    {"first_name": "Oscar", "last_name": "Piastri"},
    {"first_name": "Max", "last_name": "Verstappen"},
    {"first_name": "George", "last_name": "Russell"},
    {"first_name": "Charles", "last_name": "Leclerc"},
    {"first_name": "Lewis", "last_name": "Hamilton"},
    {"first_name": "Kimi", "last_name": "Antonelli"},
    {"first_name": "Alexander", "last_name": "Albon"},
    {"first_name": "Isack", "last_name": "Hadjar"},
    {"first_name": "Esteban", "last_name": "Ocon"},
    {"first_name": "Nico", "last_name": "Hulkenberg"},
    {"first_name": "Lance", "last_name": "Stroll"},
    {"first_name": "Carlos", "last_name": "Sainz"},
    {"first_name": "Pierre", "last_name": "Gasly"},
    {"first_name": "Yuki", "last_name": "Tsunoda"},
    {"first_name": "Oliver", "last_name": "Bearman"},
    {"first_name": "Liam", "last_name": "Lawson"},
    {"first_name": "Fernando", "last_name": "Alonso"},
    {"first_name": "Gabriel", "last_name": "Bortoleto"},
    {"first_name": "Jack", "last_name": "Doohan"},
    {"first_name": "Franco", "last_name": "Colapinto"}
]

# Base URL for driver profiles
base_url = "https://www.formula1.com/en/drivers"

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0"
}

# List to store driver data
drivers_data = []

for driver in drivers:
    first_name = driver["first_name"]
    last_name = driver["last_name"]
    profile_slug = f"{first_name.lower()}-{last_name.lower()}"
    profile_url = f"{base_url}/{profile_slug}"

    try:
        response = requests.get(profile_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve {profile_url}: Status code {response.status_code}")
            continue

        page_content = response.text

        # Extract full name
        name_match = re.search(r'<h1[^>]*class="[^"]*f1--xxl[^"]*"[^>]*>([^<]+)</h1>', page_content)
        full_name = name_match.group(1).strip() if name_match else f"{first_name} {last_name}"

        # Extract team
        team_match = re.search(r'Team</span>\s*<span[^>]*>([^<]+)</span>', page_content)
        team = team_match.group(1).strip() if team_match else "N/A"

        # Extract nationality
        nationality_match = re.search(r'Country</span>\s*<span[^>]*>([^<]+)</span>', page_content)
        nationality = nationality_match.group(1).strip() if nationality_match else "N/A"

        # Extract date of birth
        dob_match = re.search(r'Date of birth</span>\s*<span[^>]*>([^<]+)</span>', page_content)
        date_of_birth = dob_match.group(1).strip() if dob_match else "N/A"

        # Extract car number
        number_match = re.search(r'Number</span>\s*<span[^>]*>([^<]+)</span>', page_content)
        car_number = number_match.group(1).strip() if number_match else "N/A"

        driver_info = {
            "full_name": full_name,
            "team": team,
            "nationality": nationality,
            "date_of_birth": date_of_birth,
            "car_number": car_number,
            "profile_url": profile_url
        }

        drivers_data.append(driver_info)
        print(f"Collected data for {full_name}")

    except Exception as e:
        print(f"An error occurred while processing {profile_url}: {e}")

    # Pause to be respectful to the server
    time.sleep(1)

# Save the collected data into a JSON file
with open("f1_drivers_2025.json", "w", encoding="utf-8") as f:
    json.dump(drivers_data, f, ensure_ascii=False, indent=4)

print("Driver data collection complete. Data saved to f1_drivers_2025.json.")
