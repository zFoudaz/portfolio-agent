from github_ai_agent.config import settings, DB_CONN_DICT
from langchain_core.tools import tool
from contextlib import contextmanager
import psycopg2

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

@tool
def get_repo_info(repo_id:int)->str:
    """get all the content about a github repo by the repo id
        Args:
            - repo_id:int = "the id of the repo requested by use"
        Returns:
            str: name and tree structure of the repo
    """
    with get_crsr() as crsr:
        crsr.execute(
            """
            SELECT id, name, summary, tree FROM REPO
            WHERE id = %s;
            """,(repo_id,)
        )
        data = crsr.fetchone()

        return f"repo_id: {data[0]} \n\n repo_name: {data[1]} \n\n repo_summary: {data[2]} \n\n repo_tree: \n {data[3]} \n\n"

@tool
def get_repo_file(repo_id:int, file_name:str):
    """
    get the data in a specific file in the repo with repo_id and file_name
    Args:
         - repo_id:int = "the id of the repo requested by use"
         - file_name:str = "The file_name with relative path to the main root. ex: src/app.ts"
    Returns: 
         - str = File Content
    """
    with get_crsr() as crsr:
            crsr.execute(
                """
                SELECT data FROM FILE
                WHERE repo_id = %s AND name = %s;
                """,(repo_id,file_name)
            )
            data = crsr.fetchone()
            return data[0]
