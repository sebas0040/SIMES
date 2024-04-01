create table if not exists usuarios
(
	nomusuario varchar(35) not null ,
	apelliusuario varchar(35) not null,
	ccusuario varchar(11) primary key,
	correo varchar(85) unique,
	contrasena varchar(255) not null,
	foto varchar(250)
)
