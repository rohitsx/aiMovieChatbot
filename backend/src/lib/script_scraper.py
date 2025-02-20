from bs4 import BeautifulSoup
from ..lib.db.psql import create_table, get_connection 
import aiohttp
import re
import asyncio

class MovieScript:
    def __init__(self, db):
        self.base_url = "https://imsdb.com"
        self.db = db
        self.pages_url = []

    @classmethod
    async def get_db(cls):
        db = await get_connection()
        return cls(db)

    async def check_if_user_exits(self):
        if not self.db:
            return
        try:
            result = await self.db.fetchval("SELECT COUNT(*) FROM movie_scripts")
            return result == 0
        except Exception as e:
            print(f"Error checking if user exists: {e}")
            return True

    async def fetch_page_urls(self, session):
        url = self.base_url + "/all-scripts.html"
        async with session.get(url) as response:
            html = await response.text(encoding='latin-1')

        soup = BeautifulSoup(html, "html.parser")
        a_tags = soup.find_all("a", href=re.compile(r"^/Movie Scripts/.*"))

        for tag in a_tags:
            movie_name = tag.text.strip()
            if movie_name and " " in movie_name:  
                formatted_name = movie_name.replace(" ", "-") + ".html"
                full_url = f"{self.base_url}/scripts/{formatted_name}"
                self.pages_url.append((movie_name, full_url))

        print("Total number of movies found:", len(self.pages_url))

    async def fetch_movie_script(self, session, movie_name, page_url):
        async with session.get(page_url) as response:
            html = await response.text(encoding='latin-1')

        soup = BeautifulSoup(html, "html.parser")
        pre_tags = soup.find("pre")
        if pre_tags and pre_tags.text:
            dialogues = pre_tags.text.split('.')
            cleaned_dialogues = [re.sub(r"\s+", " ", line).strip() for line in dialogues if len(line.split()) > 4]
            print("added", movie_name)
            return [(movie_name, page_url, dialogue) for dialogue in cleaned_dialogues]
        return []

    async def get_movie_scripts(self, session):
        print("Fetching scripts...")
        tasks = [self.fetch_movie_script(session, movie_name, page_url) for movie_name, page_url in self.pages_url]
        results = await asyncio.gather(*tasks)
        movie_scripts = [script for sublist in results for script in sublist]
        return movie_scripts

    async def insert_scripts(self, movie_scripts):
        try:
            await self.db.executemany(
                """
                INSERT INTO movie_scripts (movie_name, script_url, script_text)
                VALUES ($1, $2, $3);
                """,
                movie_scripts
            )
            print(f"Inserted {len(movie_scripts)} scripts successfully.")
        except Exception as e:
            print(f"Error inserting scripts: {e}")
        finally:
            await self.db.close()

    async def start(self):
        if not await self.check_if_user_exits():
            print("Data already exists. Exiting...")
            return

        print("Starting script...")
        async with aiohttp.ClientSession() as session:
            await self.fetch_page_urls(session)
            movie_scripts = await self.get_movie_scripts(session)
            await self.insert_scripts(movie_scripts)

async def main():
    db = await MovieScript.get_db()
    await db.start()

if __name__ == "__main__":
    asyncio.run(main())
