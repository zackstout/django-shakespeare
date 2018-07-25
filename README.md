
# Shakespeare Thoughts
An app to let users post comments, questions, and connections about and among the lines of text in Shakespeare's corpus of plays. The hope is to create a system wherein users can add comments that appear to the side of the main text, and then other users can upvote, downvote, or comment upon that thought/question/connection to start a thread.

## Built With:
- Django
- Python
- Node.js (for web-scraping)
- PostgreSQL

## Features
- Pinging 'localhost:8000/plays/16' returns the text of King Lear, the play with id 16 in our database.

## Notes:
- Look into adding aliases for migrations and running server.
- We did [https://github.com/zackstout/shakespeare-to-database](scraping and database cleaning/prep) with Node, then gave this app access to the db.
  - (The query is ugly, but the basic idea is this: currently the database is a group of Play tables, and we want it to become a table of lines and a table of play names. We loop through the plays tables, grab all the data from each one, use another query to find the new ID of that play, and then update the new lines table accordingly.)
  - We messed up the execution, so plays 19, 20 and 21 have all rows duplicated.
