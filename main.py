import requests
from datetime import datetime, timezone
import smtplib
import time

MY_LAT = 24.161297
MY_LNG = 35.525017


def check_distance():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    response_contents = response.json()

    iss_longitude = float(response_contents["iss_position"]["longitude"])
    iss_latitude = float(response_contents["iss_position"]["latitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LNG - 5 <= iss_longitude <= MY_LNG + 5:
        return True


parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
}


def is_night():
    second_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    second_response.raise_for_status()
    second_response_contents = second_response.json()

    sunrise_hour = int(second_response_contents["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(second_response_contents["results"]["sunset"].split("T")[1].split(":")[0])
    current_hour = datetime.now(tz=timezone.utc).hour

    if current_hour > sunset_hour or current_hour < sunrise_hour:
        return True


while True:
    time.sleep(60)
    if check_distance() and is_night():
        with smtplib.SMTP("smtp.google.com", 586) as connection:
            connection.starttls()
            connection.login(user="someone", password="something")
            connection.sendmail(
                from_addr="someone",
                to_addrs="someone",
                msg="Subject:ISS!\n\nGo outside!"
            )
