#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... track proportion of overseas students

import sys
import psycopg2
import re

db = None

try:
  db = psycopg2.connect("dbname=ass2")
  cur = db.cursor()

  q = """
  select i.term, l.num_locl, i.num_intl
  from intl_term i
  join locl_term l on i.term = l.term
  group by i.term, l.num_locl, i.num_intl;
  """

  cur.execute(q)

  print("Term  #Locl  #Intl  Proportion")
  results = cur.fetchall()

  for tup in results:
    print(f"{tup[0]} {tup[1]:6d} {tup[2]:6d} {tup[1]/tup[2]:6.1f}")

except Exception as err:
  print(err)
finally:
  if db:
    db.close()
