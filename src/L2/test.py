async def start_scrape():
    url = "https://imsdb.com/all-scripts.html"
    headers = {"User-Agent": "Mozilla/5.0"}  
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        p_tags = soup.find_all("a")
        script_urls = []

        for tag in p_tags:
            movie_name = tag.text.strip()
            if movie_name and " " in movie_name:  
                formatted_name = movie_name.replace(" ", "-") + ".html"
                full_url = f"https://imsdb.com/scripts/{formatted_name}"
                script_urls.append((movie_name, full_url))

        print("total number of movies found", len(script_urls))
        await create_table()
        get_movie_scripts(script_urls, headers) 
        await insert_scripts()
        print("completed")

            

def get_movie_scripts(script_urls, headers):
    for movie_name, script_url in script_urls:
        print("adding", movie_name)
        res = requests.get(script_url, headers=headers)
        socp = BeautifulSoup(res.text, "html.parser")
        pre_tags = socp.find_all("pre")
        get_dialogues(pre_tags, movie_name, script_url)

def get_dialogues(pre_tags, movie_name, script_url):
    for pre in pre_tags:
        dialogues = pre.find_all("b")
        for t in dialogues:
            cleaned_text = t.get_text().strip()
            script_lines = cleaned_text.split('\r')

            for line in script_lines:
                movie_data.append((movie_name, script_url, line.strip()))

async def insert_scripts():
    conn = await get_connection()
    if conn:
        try:
            await conn.executemany(
                """
                INSERT INTO movie_scripts (movie_name, script_url, script_text)
                VALUES ($1, $2, $3);
                """,
                movie_data
            )
            print(f"Inserted {len(movie_data)} scripts successfully.")
        except Exception as e:
            print(f"Error inserting scripts: {e}")
        finally:
            await conn.close()
    else:
        print("Failed to connect to PostgreSQL.")

asyncio.run(start_scrape())
