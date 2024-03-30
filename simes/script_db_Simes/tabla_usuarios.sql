create table if not exists usuarios
(
	nomusuario varchar(35) not null ,
	apelliusuaruio varchar(35) not null,
	ccusuarion varchar(11) primary key,
	correo varchar(85) unique,
	contraseña varchar(255) not null
)
drop table usuarios