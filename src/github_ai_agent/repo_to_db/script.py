"""
python script to create the db tables and retrieve data from your github repos 
and structure it in 2 database tables
1- repo with repo id, name, summary ,tree(Directory structure)
2- files with file id, repo_id, name, content of the file
"""

from github_ai_agent.config import settings, DB_CONN_DICT
import psycopg2
from contextlib import contextmanager
from gitingest import ingest
import re

repos = {
    'genlearn':'https://github.com/Gen-Learn/GenLearn-Ai-Code',
    'popchoice':'https://github.com/zFoudaz/popChoice-api',
    'research_agent':'https://github.com/zFoudaz/Research-agent-with-LangGraph',
    'study_tracker':'https://github.com/zFoudaz/Study-Tracker-App'
}


@contextmanager
def get_crsr():
    conn = psycopg2.connect(**DB_CONN_DICT)
    try:
        with conn.cursor() as crsr:
            yield crsr
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()

def create_tables():
    
    with get_crsr() as crsr:
        # repos table
        crsr.execute(
            """
            CREATE TABLE IF NOT EXISTS REPO(
            id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name text NOT NULL,
            summary text,
            tree text
            )
            """
        )
        # files table
        crsr.execute(
            """
            CREATE TABLE IF NOT EXISTS FILE(
            id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            repo_id integer NOT NULL REFERENCES REPO (id),
            name text NOT NULL,
            data text
            )
            """
        )

def split_content(content):
    pattern = r"^={48}\r?\nFILE:\s*(.+?)\r?\n={48}\r?\n"
    parts = re.split(pattern, content, flags=re.MULTILINE)
    files = []
    for i in range(1, len(parts), 2):
        filename = parts[i].strip()
        content = parts[i + 1].strip()
        
        files.append({
            "name": filename,
            "content": content
        })
    return files

def add_data(repo_name,repo_url):

    summary, tree, content = ingest(repo_url)
    files = split_content(content)
    with get_crsr() as crsr:
        crsr.execute(
            """
            INSERT INTO REPO (name, summary, tree)
            VALUES (%s, %s, %s) RETURNING id; 
            """
            ,(repo_name, summary, tree)
        )
        repo_id = crsr.fetchone()[0]
        for file in files:
            crsr.execute(
                """
                INSERT INTO FILE (repo_id, name, data)
                VALUES (%s, %s, %s) RETURNING id; 
                """
                ,(repo_id, file['name'], file['content'])
            )
        

if __name__ == "__main__":
    create_tables()
    for repo_name, repo_url in repos.items():
        add_data(repo_name, repo_url)