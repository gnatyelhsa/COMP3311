#!/usr/bin/python3
# COMP3311 22T3 Ass2 ... print a transcript for a given student

import sys
import psycopg2
import re
from helpers import getStudent

# define any local helper functions here

### set up some globals

usage = f"Usage: {sys.argv[0]} zID"
db = None

### process command-line args

argc = len(sys.argv)
if argc < 2:
  print(usage)
  exit(1)
zid = sys.argv[1]
if zid[0] == 'z':
  zid = zid[1:8]
digits = re.compile("^\d{7}$")
if not digits.match(zid):
  print(f"Invalid student ID {zid}")
  exit(1)

# manipulate database

try:
  db = psycopg2.connect("dbname=ass2")
  stuInfo = getStudent(db,zid)
  if not stuInfo:
    print(f"Invalid student ID {zid}")
    exit()

  print(f"{stuInfo[1]} {stuInfo[2]}, {stuInfo[3]}") # debug
  cur = db.cursor()

  q= """
  select a.zid, e.code, d.code, d.name, g.code
  from people a
  join students b on a.id = b.id
  join program_enrolments c on b.id = c.student
  join programs d on c.program = d.id
  join terms e on c.term = e.id
  join stream_enrolments f on c.id = f.part_of
  join streams g on f.stream = g.id
  where a.zid = %s and e.code = (
    select max(a.code)
    from terms a 
    join program_enrolments b on a.id = b.term
    join students c on b.student = c.id
    join people d on c.id = d.id
    where d.zid = %s
  )
  group by a.zid, e.code, d.code, d.name, g.code;
  """
  
  cur.execute(q, [zid, zid])
  results = cur.fetchone()
  print(results[2], results[4], results[3])

  q = """
  select a.zid, e.code, f.code, left(e.title, 31), c.mark, c.grade, e.uoc
  from people a
  join students b on a.id = b.id
  join course_enrolments c on b.id = c.student
  join courses d on c.course = d.id
  join subjects e on d.subject = e.id
  join terms f on d.term = f.id
  where a.zid = %s
  group by a.zid, e.code, f.code, e.title, c.mark, c.grade, e.uoc
  order by f.code, e.code;
  """
  cur.execute(q, [zid])
  results = cur.fetchall()
  # print(results)
  total_achieved_uoc = 0
  total_attempted_uoc = 0
  weighted_mark_sum = 0
  # Print transcript for Student
  for tup in results:
    changed = list(tup)
    # update to text for special grades
    if tup[5] in ("AF", "FL", "UF", "E", "F"):
      changed[6] = "fail"
    
    elif tup[5] in ("AS", "AW", "PW", "NA", "RD", "NF", "NC", "LE", "PE", "WD", "WJ"):
      changed[6] = "unrs"
    else:
      changed[6] = f"{tup[6]}uoc"
      total_achieved_uoc += tup[6]
    
    # for calculating the total attempted uoc and weighted mark sum
    if tup[5] in ("HD", "DN", "CR", "PS", "AF", "FL", "UF", "E", "F"):
      total_attempted_uoc += tup[6]
      if tup[4]:
        weighted_mark_sum += tup[6] * tup[4]

    # update to text if no mark or grade
    if not tup[4]:
      changed[4] = "-"
    if not tup[5]:
      changed[5] = "-"

    # ensure mark is stored as string now to help with printing
    changed[4] = str(changed[4])
    
    print(f"{changed[1]} {changed[2]} {changed[3]:<32s}{changed[4]:>3s} {changed[5]:>2s}  {changed[6]:2s}")

  # print("DEBUG", weighted_mark_sum, total_attempted_uoc, total_achieved_uoc)
  weighted_avg_mark = weighted_mark_sum / total_attempted_uoc
  print(f"UOC = {total_achieved_uoc}, WAM = {weighted_avg_mark:.1f}")

except Exception as err:
  print("DB error: ", err)
finally:
  if db:
    db.close()

