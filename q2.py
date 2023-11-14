#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... track satisfaction in a given subject

import sys
import psycopg2
import re
from helpers import *

usage = f"Usage: {sys.argv[0]} SubjectCode"
db = None

### process command-line args

argc = len(sys.argv)
if argc < 2:
  print(usage)
  exit(1)
subject = sys.argv[1]
check = re.compile("^[A-Z]{4}[0-9]{4}$")
if not check.match(subject):
  print("Invalid subject code")
  exit(1)

try:
  db = psycopg2.connect("dbname=ass2")
  subjectInfo = getSubject(db,subject)
  if not subjectInfo:
    print(f"Invalid subject code {subject}")
    exit(1)

  subjectName = subjectInfo[2]
  print(subject, subjectName) 
  cur = db.cursor()
  # List satisfaction for subject over time
  q = """
  select d.code, max(b.satisfact), max(b.nresponses), count(c.student), f.full_name
  from Subjects a
  left join Courses b on a.id = b.subject
  left join Course_enrolments c on b.id = c.course
  left join Terms d on b.term = d.id
  left join Staff e on b.convenor = e.id
  left join People f on e.id = f.id
  where a.code = %s
  group by d.code, a.code, f.full_name
  order by d.code;
  """
  
  cur.execute(q, [subject])

  print("Term  Satis  #resp  #stu  Convenor")
  results = cur.fetchall()

  for tup in results:
    if not all(tup):
      changed = list(tup)

      if not changed[1]:
        changed[1] = "?".rjust(6)
      elif changed[1]:
        changed[1] = f"{tup[1]:6d}"

      if not changed[2]:
        changed[2] = "?".rjust(6)
      elif changed[2]:
        changed[2] = f"{tup[2]:6d}"

      if not changed[3]:
        changed[3] = 0
        changed[3] = f"{changed[3]:6d}"
      elif changed[3]:
        changed[3] = f"{tup[3]:6d}"

      if not changed[4]:
        changed[4] = "?"

      tup = tuple(changed)
      print(f"{tup[0]} {tup[1]} {tup[2]} {tup[3]}  {tup[4]}")

    else:
      print(f"{tup[0]} {tup[1]:6d} {tup[2]:6d} {tup[3]:6d}  {tup[4]}")

except Exception as err:
  print(err)
finally:
  if db:
    db.close()
