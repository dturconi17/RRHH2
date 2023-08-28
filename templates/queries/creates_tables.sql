CREATE TABLE IF NOT EXISTS `sitio`.`aprobaciones` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`descripcion` varchar(100) NOT NULL COMMENT 'Descripcion', 
`id_aprobacion` int(9) NOT NULL COMMENT 'Id de Aprobacion', 
PRIMARY KEY (`id`) );


CREATE TABLE IF NOT EXISTS `sitio`.`empleados` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria traida de usuario', 
`id_empleado` varchar(100) NOT NULL COMMENT 'Id Empleado',
`formacion` varchar(100) NOT NULL COMMENT 'formacion', 
`nacimiento` datetime not null comment 'fecha de nacimiento',
`estado_civil` varchar(50) not null comment 'fecha de nacimiento', 
`hijos` varchar(50) NOT NULL COMMENT 'hijos',
`calle` varchar(100) NOT NULL COMMENT 'calle',
`nro` varchar(10) NOT NULL COMMENT 'Nro',
`piso` varchar(5) NOT NULL COMMENT 'Piso',
`depto` varchar(5) NOT NULL COMMENT 'Departamento',
`cp` varchar(8) NOT NULL COMMENT 'cp',
`localidad` varchar(100) NOT NULL COMMENT 'Localidad',
`provincia` varchar(100) NOT NULL COMMENT 'Provincia',
`foto` varchar(100) NULL COMMENT 'Foto',
PRIMARY KEY (`id`) );


CREATE TABLE IF NOT EXISTS `sitio`.`empresas` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`empresa` varchar(100) NOT NULL COMMENT 'Empresa', 
`creado_por` varchar(50) NOT NULL COMMENT 'Usuario Creador', 
`fecha` DATETIME NOT NULL COMMENT 'Fecha Creacion', 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`gerencias` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`gerencia` varchar(100) NOT NULL COMMENT 'Gerencia', 
`creado_por` varchar(50) NOT NULL COMMENT 'Usuario Creador', 
`fecha` DATETIME NOT NULL COMMENT 'Fecha', 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`jefaturas` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`jefatura` varchar(50) NOT NULL COMMENT 'Jefatura', 
`gerencia` varchar(50) NOT NULL COMMENT 'Gerencia', 
`creado_por` varchar(50) NOT NULL COMMENT 'Usuario Creador', 
`fecha` DATETIME NOT NULL, 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`niveles` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`nivel` varchar(50) NOT NULL, 
`aprobacion` int(1) NOT NULL, 
`creado_por` varchar(50) NOT NULL, 
`fecha` DATETIME NOT NULL, 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`noticias` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`titulo` varchar(100) NOT NULL, 
`noticia` varchar(100) NOT NULL, 
`mas_noticia` varchar(250) , 
`link` varchar(50) , 
`imagen` varchar(50) NOT NULL, 
`apagar` int(1) NOT NULL, 
`creado_por` varchar(50) NOT NULL, 
`fecha` DATETIME NOT NULL, 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`periodos_activos` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`periodo` varchar(50) NOT NULL, 
`tipo_licencia` varchar(100) NOT NULL, 
`activo` int(1) NOT NULL, 
`creado_por` varchar(50) NOT NULL, 
`fecha` DATETIME NOT NULL, 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`periodo_nuevo` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`nombre_usuario` varchar(50) NOT NULL COMMENT 'Usuario', 
`periodo` varchar(100), 
`dias` int(2) NOT NULL, 
`antiguedad` int(2) NOT NULL, 
`creado_por` varchar(50) NOT NULL, 
`fecha` DATETIME NOT NULL, 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`reglas_vacaciones` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`desde` int(2) NOT NULL COMMENT 'Usuario', 
`hasta` int(2) NOT NULL COMMENT 'Clave', 
`dias` int(2) NOT NULL COMMENT 'Nombre', 
`creado_por` varchar(50) NOT NULL COMMENT 'Apellido', 
`fecha` DATETIME NOT NULL COMMENT 'documento', 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`setup` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`caracteristica` varchar(100) NOT NULL COMMENT 'Usuario', 
`valor` varchar(100) NOT NULL COMMENT 'Clave', 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`stock_vacaciones` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`id_empleado` varchar(50) NOT NULL COMMENT 'Usuario', 
`periodo` varchar(50) NOT NULL COMMENT 'Clave', 
`dias_totales` int(2) NOT NULL COMMENT 'Nombre', 
`dias_tomados` int(2) NOT NULL COMMENT 'Apellido', 
`dias_pendientes` int(2) NOT NULL COMMENT 'documento', 
`dias_por_aprobarse` int(2) NOT NULL, 
`dias_aprobados` int(2) NOT NULL, 
`usuario_modifica` varchar(50) NOT NULL, 
`fecha_modifica` DATETIME NOT NULL, 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`usuario` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`nombre_usuario` varchar(50) NOT NULL, 
`clave_usuario` varchar(100) NOT NULL, 
`nombre` varchar(50) NOT NULL, 
`apellidos` varchar(100) NOT NULL, 
`documento` int(9) NOT NULL, 
`sexo` varchar(15) NOT NULL, 
`mail` varchar(50) NOT NULL,
`empresa` int(2) NOT NULL, 
`gerencia` int(2) NOT NULL,
`jefatura` int(2) NOT NULL,
`funcion` int(2) NOT NULL,
`fecha_incorporacion` datetime NOT NULL,
`fecha_baja` datetime,
`creador` varchar(50) NOT NULL,
`fecha_alta` datetime NOT NULL,
PRIMARY KEY (`id`) );


CREATE TABLE IF NOT EXISTS `sitio`.`vacaciones` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`periodo` varchar(50) NOT NULL COMMENT 'Periodo',
`desde` datetime NOT NULL, 
`hasta` datetime NOT NULL, 
`dias_totales` int(2) NOT NULL, 
`empleado` varchar(50) NOT NULL, 
`estado` varchar(50) NOT NULL, 
`fecha_solicitud` datetime NOT NULL, 
`aprobador` varchar(50) NOT NULL COMMENT 'Usuario que aprobo',
`fecha_aprobacion` datetime NOT NULL, 
PRIMARY KEY (`id`) );


CREATE TABLE IF NOT EXISTS `sitio`.`logueo` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`fecha` datetime NOT NULL COMMENT 'Periodo',
`sitio` varchar(100) NOT NULL,
`usuario` varchar(50) NOT NULL, 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`datos_contacto` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`id_empleado` varchar(50) NOT NULL COMMENT 'Empresa', 
`telefono_fijo` varchar(50) NOT NULL COMMENT 'Telefono Fijo',
`interno` varchar(50) NOT NULL COMMENT 'Interno',
`celular` varchar(50) NOT NULL COMMENT 'Celular',
`domicilio_laboral` varchar(50) NOT NULL COMMENT 'Domicilio Laboral', 
`mail_laboral` varchar(100) NOT NULL COMMENT 'Mail Laboral', 
`fecha` DATETIME NOT NULL COMMENT 'Fecha Creacion', 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`saludos` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria',
`id_reply` int(11) NULL COMMENT 'Clave reply', 
`id_empleado` varchar(50) NOT NULL COMMENT 'Empleado que envia', 
`id_recibe` varchar(50) NOT NULL COMMENT 'Empleado que recibe',
`mensaje` text NOT NULL COMMENT 'Mensaje',
`creador` varchar(50) NOT NULL,
`fecha_alta` datetime NOT NULL,
`visto` int NOT NULL,
PRIMARY KEY (`id`) );

INSERT INTO `sitio`.`usuario`(`nombre_usuario`, `clave_usuario`, `nombre`, `apellidos`, `documento`, `sexo`, `mail`, `empresa`, `gerencia`, `jefatura`, `funcion`, `fecha_incorporacion`,`creador`, `fecha_alta`) VALUES ('dturconi','Santi1703','Diego','Turconi','28032766','Hombre','dturconi@gmail.com',0,0,0,99,now(),'dturconi',now());
INSERT INTO `sitio`.`usuario`(`nombre_usuario`, `clave_usuario`, `nombre`, `apellidos`, `documento`, `sexo`, `mail`, `empresa`, `gerencia`, `jefatura`, `funcion`, `fecha_incorporacion`,`creador`, `fecha_alta`) VALUES ('gfasanella','Santi1703','Gabriela','Fasanella','25477457','Mujer','gaby.fasane@gmail.com',0,0,0,99,now(),'dturconi',now());

INSERT INTO `sitio`.`niveles`(`id`, `nivel`, `aprobacion`, `creado_por`, `fecha`) VALUES (99,'Admin',0,'dturconi',now());
INSERT INTO `sitio`.`niveles`(`id`, `nivel`, `aprobacion`, `creado_por`, `fecha`) VALUES (103,'Gerente',5,'dturconi',now());
INSERT INTO `sitio`.`niveles`(`id`, `nivel`, `aprobacion`, `creado_por`, `fecha`) VALUES (104,'Jefe',4,'dturconi',now());
INSERT INTO `sitio`.`niveles`(`id`, `nivel`, `aprobacion`, `creado_por`, `fecha`) VALUES (108,'CEO',6,'dturconi',now());

insert into `sitio`.aprobaciones values (1, 'Nivel 0 - No Aprueba', 1);
insert into `sitio`.aprobaciones values (2, 'Nivel 1 - Aprueba Nivel 0', 2);
insert into `sitio`.aprobaciones values (3, 'Nivel 2 - Aprueba Nivel 0 y 1', 3);
insert into `sitio`.aprobaciones values (4, 'Nivel 3 - Aprueba Nivel 0, 1 y 2', 4);
insert into `sitio`.aprobaciones values (5, 'Nivel 4 - Aprueba Nivel 0, 1, 2 y 3', 5);
insert into `sitio`.aprobaciones values (6, 'Nivel 5 - Aprueba Todo', 6);

