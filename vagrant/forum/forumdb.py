# "Database code" for the DB Forum.

import datetime
import psycopg2, bleach

POSTS = [("This is the first post.", datetime.datetime.now())]

DBNAME = "forum"

def get_posts():
  """Return all posts from the 'database', most recent first."""
  conn = psycopg2.connect(database=DBNAME)
  c = conn.cursor()
  c.execute("select content, time from posts order by time desc")
  return c.fetchall()
  conn.close()

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  conn = psycopg2.connect(database=DBNAME)
  c = conn.cursor()
  c.execute("insert into posts values (%s)", (bleach.clean(content,))
  conn.commit()
  conn.close()


