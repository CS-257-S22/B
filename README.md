# Team B
team-project-team-b created by GitHub Classroom

## Team Members
+ Jonas Bartels
+ Lazuli Kleinhans
+ Tin Nguyen
+ Kai Weiner

Copy Commands to Load Tables:

psql -U teamb -h localhost -d teamb < createtable.sql
psql -U teamb -h localhost -d teamb

\copy death_data FROM 'data_smaller.csv' DELIMITER ',' CSV;
\copy misc_data FROM 'all_states_misc.csv' DELIMITER ',' CSV;