create table testa (
  key char(16) primary key,
  val1 integer not null,
  val2 integer unique,
  val3 integer default 0 not null
);

create table testb (
  key char(16) primary key,
  val1 integer not null,
  val2 integer unique,
  val3 integer default 0 not null
);