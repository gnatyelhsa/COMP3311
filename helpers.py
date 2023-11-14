# COMP3311 21T3 Ass2 ... Python helper functions
# add here any functions to share between Python scripts 
# you must submit this even if you add nothing

def getSubject(db,subject):
  cur = db.cursor()
  cur.execute("select * from Subjects where code = %s",[subject])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getProgram(db,code):
  cur = db.cursor()
  cur.execute("select * from Programs where code = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getStream(db,code):
  cur = db.cursor()
  cur.execute("select * from Streams where code = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getStudent(db,zid):
  cur = db.cursor()
  qry = """
  select p.*
  from   People p
         join Students s on s.id = p.id
  where  p.id = %s
  """
  cur.execute(qry,[zid])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getCourseName(db, code):
  cur = db.cursor()
  qry = """
  select title
  from subjects
  where code = %s;
  """
  cur.execute(qry,[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getStreamName(db, code):
  cur = db.cursor()
  qry = """
  select name
  from streams
  where code = %s;
  """
  cur.execute(qry,[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info


