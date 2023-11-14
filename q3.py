#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... print list of rules for a program or stream

import sys
import psycopg2
import re
from helpers import getProgram, getStream, getCourseName, getStreamName

# define any local helper functions here
def stream_print_format(results):
  for tup in results:
    if not tup[1] and not tup[2]:
       print(f"all streams from {tup[0]}")
       if tup[3]:
         print("-", tup[3])
    elif tup[1] and not tup[2]:
      print(f"at least {tup[1]} streams from {tup[0]}")
      if tup[3]:
        print("-", tup[3])
    elif not tup[1] and tup[2]:
      print(f"up to {tup[2]} streams from {tup[0]}")
      if tup[3]:
        print("-", tup[3])
    elif tup[1] < tup[2]:
      print(f"between {tup[1]} and {tup[2]} streams from {tup[0]}")
      if tup[3]:
        print("-", tup[3])
    elif tup[1] == tup[2]:
      print(f"{tup[1]} stream from {tup[0]}")
      if tup[3]:
        streams = tup[3].split(",")
        for stream in streams:
          print("-", stream, getStreamName(db,stream)[0])
    else:
      print("Unsure what to print...")

def course_print_format(results):
  for tup in results:
    if not tup[1] and not tup[2]:
      print(f"all courses from {tup[0]}")
      if tup[3]:
        courses = tup[3].split(",")
        for course in courses:
          # for each course code in course listing display with their course name
          specialChar = re.compile('[^0-9a-zA-Z]+')
          if specialChar.search(course):
            # for the case when courses are in the format e.g. {MATH1131;MATH1141}
            course = course[1:]
            course = course[:-1]
            alternative = course.split(";")
            print("-", alternative[0], getCourseName(db,alternative[0])[0])
            print(" ", "or", alternative[1], getCourseName(db,alternative[1])[0])
          else:
            print("-", course, getCourseName(db,course)[0])
  
    elif tup[1] and not tup[2]:
      print(f"at least {tup[1]} UOC courses from {tup[0]}")
      if tup[3]:
        print("-", tup[3])
      
    elif not tup[1] and tup[2]:
      print(f"up to {tup[2]} UOC courses from {tup[0]}")
      if tup[3]:
        print("-", tup[3])
      
    elif tup[1] < tup[2]:
      print(f"between {tup[1]} and {tup[2]} UOC courses from {tup[0]}")
      if tup[3]:
        print("-", tup[3])
    
    elif tup[1] == tup[2]:
      print(f"{tup[1]} UOC courses of {tup[0]}")
      if tup[3]:
        print("-", tup[3])
    else:
      print("Unsure what to print...")

def total_uoc_print_format(results):
  for tup in results:
    if not tup[1] and not tup[2]:
      break
    elif tup[1] and not tup[2]:
      print(f"{tup[0]} at least {tup[1]} UOC")
    elif not tup[1] and tup[2]:
      print(f"{tup[0]} up to {tup[2]} UOC")
    elif tup[1] < tup[2]:
      print(f"{tup[0]} between {tup[1]} and {tup[2]} UOC")
    elif tup[1] == tup[2]:
      print(f"{tup[0]} {tup[1]} UOC")
    else:
      print("Unsure what to print...")

def gened_free_print_format(results):
  for tup in results:
    if not tup[1] and not tup[2]:
       print(f"all UOC of {tup[0]}")

    elif tup[1] and not tup[2]:
      print(f"at least {tup[1]} UOC of {tup[0]}")

    elif not tup[1] and tup[2]:
      print(f"up to {tup[2]} UOC of {tup[0]}")

    elif tup[1] < tup[2]:
      print(f"between {tup[1]} and {tup[2]} UOC of {tup[0]}")

    elif tup[1] == tup[2]:
      print(f"{tup[1]} UOC of {tup[0]}")

    else:
      print("Unsure what to print...")

usage = f"Usage: {sys.argv[0]} (ProgramCode|StreamCode)"
db = None

### process command-line args

argc = len(sys.argv)
if argc < 2:
  print(usage)
  exit(1)
code = sys.argv[1]
if len(code) == 4:
  codeOf = "program"
elif len(code) == 6:
  codeOf = "stream"
else:
  print("Invalid code")
  exit(1)

try:
  db = psycopg2.connect("dbname=ass2")
  if codeOf == "program":
    progInfo = getProgram(db,code)
    if not progInfo:
      print(f"Invalid program code {code}")
      exit(1)
    print(code, progInfo[2])
  
    print("Academic Requirements:")
    cur = db.cursor()
    # List the rules for Program

    q = """
    select * from get_program_req_by_type('uoc', %s);
    """
    cur.execute(q, [code])
    results = cur.fetchall()
    total_uoc_print_format(results)
    
    q = """
    select * from get_program_req_by_type('stream', %s);
    """
    cur.execute(q, [code])
    results = cur.fetchall()
    stream_print_format(results)
    

    q = """
    select * from get_program_req_by_type('core', %s);
    """
    cur.execute(q, [code])
    results = cur.fetchall()
    course_print_format(results)

    q = """
    select * from get_program_req_by_type('elective', %s);
    """
    cur.execute(q, [code])
    results = cur.fetchall()
    course_print_format(results)
  

    q = """
    select * from get_program_req_by_type('gened', %s);
    """
    cur.execute(q, [code])
    results = cur.fetchall()
    gened_free_print_format(results)


    q = """
    select * from get_program_req_by_type('free', %s);
    """
    cur.execute(q, [code])
    results = cur.fetchall()
    gened_free_print_format(results)
    

  elif codeOf == "stream":
    strmInfo = getStream(db,code)
    if not strmInfo:
      print(f"Invalid stream code {code}")
      exit(1)
    print(code, strmInfo[2])  #debug

    print("Academic Requirements:")
    cur = db.cursor()

    # List the rules for Stream
    q = """
    select * from get_stream_req_by_type('uoc', %s);
    """
    cur.execute(q, [code])
    results = cur.fetchall()
    total_uoc_print_format(results)
    
    q = """
    select * from get_stream_req_by_type('stream', %s);
    """
    cur.execute(q, [code])
    results = cur.fetchall()
    stream_print_format(results)

    q = """
    select * from get_stream_req_by_type('core', %s);
    """
    cur.execute(q, [code])
    results = cur.fetchall()
    course_print_format(results)

    q = """
    select * from get_stream_req_by_type('elective', %s);
    """
    cur.execute(q, [code])
    results = cur.fetchall()
    course_print_format(results)

    q = """
    select * from get_stream_req_by_type('gened', %s);
    """
    cur.execute(q, [code])
    results = cur.fetchall()
    gened_free_print_format(results)


    q = """
    select * from get_stream_req_by_type('free', %s);
    """
    cur.execute(q, [code])
    results = cur.fetchall()
    gened_free_print_format(results)
    

except Exception as err:
  print(err)
finally:
  if db:
    db.close()
