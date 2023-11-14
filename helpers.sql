-- COMP3311 23T3 Ass2 ... extra database definitions
-- add any views or functions you need into this file
-- note: it must load without error into a freshly created MyMyUNSW database
-- you must submit this even if you add nothing to it
create or replace view terms_unique(term_id, student_id)
as 
select distinct term, student
from program_enrolments;

create or replace view intl_term(term, num_intl)
as
select t.code, count(s.id)
from students s
join terms_unique u on s.id = u.student_id
join terms t on u.term_id = t.id
where s.status = 'INTL' 
group by t.code
order by t.code;

create or replace view locl_term(term, num_locl)
as
select t.code, count(s.id)
from students s
join terms_unique u on s.id = u.student_id
join terms t on u.term_id = t.id
where s.status != 'INTL'
group by t.code
order by t.code;

create or replace function 
  get_program_req_by_type(req_type text, program text) returns table (name text, min_req int, max_req int, acadobjs text)
as $$
select a.name, a.min_req, a.max_req, a.acadobjs
from requirements a
join programs b on a.for_program = b.id
where a.rtype::text = req_type and b.code = program
order by a.id;
$$ language sql;

create or replace function 
  get_stream_req_by_type(req_type text, stream text) returns table (name text, min_req int, max_req int, acadobjs text)
as $$
select a.name, a.min_req, a.max_req, a.acadobjs
from requirements a
join streams b on a.for_stream = b.id
where a.rtype::text = req_type and b.code = stream
order by a.id;
$$ language sql;