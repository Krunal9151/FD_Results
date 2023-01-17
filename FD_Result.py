
import re
import requests
from bs4 import BeautifulSoup
import psycopg2

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="root",
    database="Events"
)
cursor = conn.cursor()

# Define the table schema
cursor.execute("""
        id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
		date_time character varying(1000),
		location character varying(1000),
		title character varying(1000),
		artists character varying(1000),
		works character varying(1000),
		image_link bytea, 
		createdOn date default CURRENT_DATE,
		PRIMARY KEY (id)
    )
""")
conn.commit()

# Make a GET request to the website
url = 'https://www.lucernefestival.ch/en/program/summer-festival-23'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Use BeautifulSoup to parse the HTML
events = soup.find_all('div', class_='event-content')
  

# Extract the relevant information from each event
for event in events:
    
    date_time_location = event.find('div', class_='cell xlarge-6 body-small').get_text()
    date_time_location_list = date_time_location.split("\n")
    date_time = date_time_location_list[2].strip()
    location = date_time_location_list[3].strip()

    title_name = event.find('p', class_='event-title h3').get_text()
    artists= title_name.split("|")[-1].strip()
    title= title_name.split("|")[0].strip()
    
    works = event.find ('div', class_='body-small').get_text()

    image_link = event.find("img")["src"]


    # Insert the event information into the database
    cursor.execute ("""  INSERT INTO events ( date_time, location, title, artists, works, image_link) VALUES (%s,  %s,  %s, %s ,%s,%s )""", ( date_time, location, title, artists , works, image_link))
    conn.commit()

# Close the database connection
cursor.close()
conn.close()
