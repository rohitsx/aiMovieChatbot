import requests
from bs4 import BeautifulSoup
import re
import psycopg2

# Initialize PostgreSQL connection
conn = psycopg2.connect(
            database="mydatabase",
            user="myuser",
            password="mypassword",
            host="127.0.0.1",
            port=5432,
        )
cursor = conn.cursor()

def scrape():
    url = "https://imsdb.com/all-scripts.html"
    headers = {"User-Agent": "Mozilla/5.0"}  # Prevents blocking
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        p_tags = soup.find_all("a")
        script_urls = []

        for tag in p_tags:
            movie_name = tag.text.strip()
            if movie_name and " " in movie_name:  # Ensure it's a valid movie title
                formatted_name = movie_name.replace(" ", "-") + ".html"
                full_url = f"https://imsdb.com/scripts/{formatted_name}"
                script_urls.append((movie_name, full_url))

        for movie_name, script_url in script_urls:
            res = requests.get(script_url, headers=headers)
            socup = BeautifulSoup(res.text, "html.parser")
            pre_tags = socup.find_all("pre")

            for pre in pre_tags:
                script_text = pre.get_text()  # Extract text
                cleaned_text = re.sub(r"\n{2,}", "\n", script_text).strip()  # Remove extra newlines
                
                # Insert into PostgreSQL safely
                try:
                    cursor.execute(
                        "INSERT INTO movie_scripts (movie_name, script_url, script_text) VALUES (%s, %s, %s)",
                        (movie_name, script_url, cleaned_text)
                    )
                    conn.commit()
                except Exception as e:
                    print(f"Error inserting {movie_name}: {e}")
            
# Run the scraper
scrape()

# Close database connection
cursor.close()
conn.close()
