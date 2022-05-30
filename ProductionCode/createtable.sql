DROP TABLE death_data;
CREATE TABLE death_data (
  state_name text,
  age int,
  gender char,
  cause text,
  deaths int
);

DROP TABLE misc_data;
CREATE TABLE misc_data (
  age text,
  gender char,
  cause text,
  deaths int
)