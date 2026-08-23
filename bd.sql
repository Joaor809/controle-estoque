create database mercearia;
use mercearia;

create table produtos(
    id int auto_increment primary key,
    nome varchar(60) not null,
    marcar varchar(30) not null,
    preco decimal(6, 2) not null,
    quantidade int not null
);