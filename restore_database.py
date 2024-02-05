import subprocess

subprocess.run(["C:\\Program Files\\PostgreSQL\\16\\bin\\psql.exe", "-d", "salesdata", "-U", "postgres", "-f", "C:\\Users\\mike_\\Downloads\\salesdata.sql"])
