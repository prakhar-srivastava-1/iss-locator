import smtplib
import time

import requests
from datetime import datetime
from secrets import email, password, recipient

MY_LAT = 22.171841
MY_LONG = 76.065422


def is_over_head():
    """
    Gives a call to ISS API to get its current location.
    :return: True if ISS is over my location (+5/-5 deg) (bool)
    """
    # call ISS API
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    # extract the ISS latitude and longitude
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 \
            and MY_LONG - 5 <= iss_latitude <= MY_LONG + 5:
        return True
    return False

def is_night():
    """
    Checks the time of sunrise-sunset using API.
    Compares the time to see if its night at your location.
    :return: True if it is night
    """
    # Set params to get sunrise and sunset timings
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    # make a call to sunrise-sunset api
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    # Extract Sunrise and Sunset timings in 24-hour (UTC) format
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # current time
    time_now = datetime.now()

    # If it is currently dark
    if sunrise >= time_now.hour >= sunset:
        return True
    return False


# BONUS: run the code every 60 seconds.
while True:
    if is_over_head() and is_night():
        # Then send me an email to tell me to look up.
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(
                from_addr=email,
                to_addrs=recipient,
                msg=f"Subject: ISS is Passing Over Head!\n\n"
                    f"Hi,\nThe International Space Station is passing above you. "
                    f"Look up and catch a glimpse of it.\nHave Fun!\nThanks."
            )
    elif not is_night() and not is_over_head():
        print("ISS will not be in your location and will not be visible due to excessive sunlight")
    elif not is_night():
        print("ISS will not be visible due to excessive sunlight")
    elif not is_over_head():
        print("ISS is not near your location")
    time.sleep(60)



