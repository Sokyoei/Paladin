create database if not exists paladin_fastapi_learn;

use paladin_fastapi_learn;

create table if not exists genshin_roles (
    name varchar(255) primary key,
    level enum('four', 'five'),
    birthday date,
)

insert into genshin_roles (name, level, birthday) values
('Albedo', 'five', '1995-01-01'),
('Amber', 'four', '1996-02-02'),
('Barbara', 'four', '1997-03-03'),
('Beidou', 'five', '1998-04-04'),
('Bennett', 'four', '1999-05-05');
