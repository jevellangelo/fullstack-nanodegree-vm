# Database code for the Logs Analysis Project

import psycopg2
DB_NAME = "news"

# Logs Analysis Questions
question_1 = ("What are the most popular three articles of all time?")
question_2 = ("Who are the most popular article authors of all time?")
question_3 = ("On which days did more than 1 percent of requests lead to errors?")

# Database queries
top_articles = """select articles.title, count(*) as views
			from log join articles
			on substring(log.path,10) = articles.slug
			where log.status = '200 OK'
			group by title
			order by views desc
			limit 3;"""

top_authors = """select authors.name, count(*) as views
			from articles
			join authors on articles.author = authors.id
			join log on substring(log.path,10) = articles.slug
			and log.status = '200 OK'
			group by authors.name
			order by views desc
			limit 3;"""

error_requests = """select * from (
			select all_requests.day,
			round((100*failed_requests.requests / all_requests.requests),2)
			as percentage from (
				(select to_char(log.time, 'FMMonth DD, YYYY') as day,
				count(*) as requests
				from log
				group by day) as all_requests
				join
				(select to_char(log.time, 'FMMonth DD, YYYY') as day,
				count(*) as requests
				from log
				where status = '404 NOT FOUND'
				group by day) as failed_requests
			on all_requests.day = failed_requests.day))
			as t where percentage > 1.0;"""

# Database sql request
def query_db(sql_request):
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute(sql_request)
    results = c.fetchall()
    db.close()
    return results

# Question 1
def top_three_articles():
    top_three_articles = query_db(top_articles)
    print("\n 1. " + question_1 + "\n")
    for title, views in top_three_articles:
    	print("   \"{t}\" -- {v} views". format(t=title,v=views))
top_three_articles()

#Question 2
def top_three_authors():
	top_three_authors = query_db(top_authors)
	print("\n 2. " + question_2 + "\n")
	for name, views in top_three_authors:
		print("   {n} -- {v} views". format(n=name,v=views))
top_three_authors()

#Question #3
def more_errors():
	more_errors = query_db(error_requests)
	print("\n 3. " + question_3 + "\n")
	for day, percentage in more_errors:
		print("   {d} -- {p} views \n". format(d=day,p=percentage))
more_errors()