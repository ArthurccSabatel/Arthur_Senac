CREATE DATABASE mercado;
USE mercado;

CREATE TABLE cliente(
	cpf VARCHAR(11) NOT NULL,
    cliente VARCHAR (255),
    rg VARCHAR(245) ,
    datan VARCHAR(10),
    ocupacao VARCHAR(255),
    fone VARCHAR(255),
    email VARCHAR (255),
    cidade VARCHAR (255),
	PRIMARY KEY(cpf)
);

SELECT * FROM cliente; 

