import smtplib
import time

import requests
from datetime import datetime
from secrets import email, password, recipient

MY_LAT = 22.171841
MY_LONG = 76.065422

def check_ISS():
    # call ISS API
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    # extract the ISS latitude and longitude
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    my_lat_rel = (MY_LAT + 5, MY_LAT - 5)
    my_long_rel = (MY_LONG + 5, MY_LONG - 5)

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

    time_now = datetime.now()

    # If the ISS is close to my current position
    # and it is currently dark
    if my_lat_rel[0] <= iss_latitude <= my_lat_rel[1] \
            and my_long_rel[0] <= iss_longitude <= my_long_rel[1] \
            and sunrise >= time_now.hour >= sunset:
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

    print(iss_longitude, iss_latitude)
    print(my_lat_rel, my_long_rel)
    print(time_now.hour)
    print(sunrise, sunset)


# BONUS: run the code every 60 seconds.
while True:
    check_ISS()
    time.sleep(60)



