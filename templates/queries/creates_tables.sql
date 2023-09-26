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
`domicilio` varchar(100) NOT NULL COMMENT 'Domicilio', 
`cuit` varchar(11) NOT NULL COMMENT 'Cuit', 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`gerencias` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`jefatura` varchar(50) NOT NULL COMMENT 'Jefatura', 
`aprobacion` int(11) NOT NULL COMMENT 'Aprobacion',
`creado_por` varchar(50) NOT NULL COMMENT 'Usuario Creador', 
`fecha` DATETIME NOT NULL, 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`jefaturas` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`jefatura` varchar(50) NOT NULL COMMENT 'Jefatura', 
`aprobacion` int(11) NOT NULL COMMENT 'Aprobacion',
`creado_por` varchar(50) NOT NULL COMMENT 'Usuario Creador', 
`fecha` DATETIME NOT NULL, 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`estructuras` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`area` varchar(50) NOT NULL COMMENT 'Nombre Area', 
`tipo_area` int(11) NOT NULL COMMENT 'Tipo Area',
`nivel_area` int(11) NOT NULL COMMENT 'Nivel Area',
`reporta_a` int(11) NOT NULL COMMENT 'Reporta Area',
`creado_por` varchar(50) NOT NULL COMMENT 'Usuario Creador', 
`fecha` DATETIME NOT NULL, 
PRIMARY KEY (`id`) );

insert into sitio.area (area, id_dependencia, id_estructura, creado_por, fecha) values ('Gerencia General',1,1,'dturconi',now());

CREATE TABLE IF NOT EXISTS `sitio`.`niveles` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`nivel` varchar(50) NOT NULL, 
`orden` int(1) NOT NULL, 
`creado_por` varchar(50) NOT NULL, 
`fecha` DATETIME NOT NULL, 
PRIMARY KEY (`id`) );

INSERT INTO `sitio`.`niveles` VALUES (0,'Admin',35,'dturconi',now());

CREATE TABLE IF NOT EXISTS `sitio`.`estructuras` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`estructura` varchar(50) NOT NULL, 
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
`orden` int(2) NOT NULL,
`funcion` int(2) NOT NULL,
`aprobacion` int(2) NOT NULL,
`fecha_incorporacion` datetime NOT NULL,
`fecha_baja` datetime,
`creador` varchar(50) NOT NULL,
`fecha_alta` datetime NOT NULL,
PRIMARY KEY (`id`) );

INSERT INTO `sitio`.`usuario`(`nombre_usuario`, `clave_usuario`, `nombre`, `apellidos`, `documento`, `sexo`, `mail`, `empresa`, `orden`, `funcion`, `aprobacion`, `fecha_incorporacion`,`creador`, `fecha_alta`) VALUES ('dturconi','Santi1703','Diego','Turconi','28032766','Hombre','dturconi@gmail.com',0,30,35,99,now(),'dturconi',now());
INSERT INTO `sitio`.`usuario`(`nombre_usuario`, `clave_usuario`, `nombre`, `apellidos`, `documento`, `sexo`, `mail`, `empresa`, `orden`, `funcion`, `aprobacion`, `fecha_incorporacion`,`creador`, `fecha_alta`) VALUES ('gfasanella','Santi1703','Gabriela','Fasanella','25477457','Mujer','gaby.fasane@gmail.com',0,30,35,99,now(),'dturconi',now());



CREATE TABLE IF NOT EXISTS `sitio`.`vacaciones` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`periodo` varchar(50) NOT NULL COMMENT 'Periodo',
`desde` datetime NOT NULL, 
`hasta` datetime NOT NULL, 
`dias_totales` int(2) NOT NULL, 
`empleado` varchar(50) NOT NULL, 
`estado` varchar(50) NOT NULL, 
`fecha_solicitud` datetime NOT NULL, 
`aprobador` varchar(50) NULL COMMENT 'Usuario que aprobo',
`fecha_aprobacion` datetime NULL, 
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


CREATE TABLE IF NOT EXISTS `sitio`.`aprobaciones` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`descripcion` varchar(100) NOT NULL COMMENT 'Descripcion', 
`id_aprobacion` int(9) NOT NULL COMMENT 'Id de Aprobacion', 
PRIMARY KEY (`id`) );

insert into `sitio`.aprobaciones values (1, 'Nivel 1 - No Aprueba', 1);
insert into `sitio`.aprobaciones values (2, 'Nivel 2 - Aprueba Nivel 1', 2);
insert into `sitio`.aprobaciones values (3, 'Nivel 3 - Aprueba Nivel 1 y 2', 3);
insert into `sitio`.aprobaciones values (4, 'Nivel 4 - Aprueba Nivel 1, 2 y 3', 4);
insert into `sitio`.aprobaciones values (5, 'Nivel 5 - Aprueba Nivel 1, 2, 3 y 4', 5);
insert into `sitio`.aprobaciones values (99, 'Nivel 99 - Aprueba Todo', 99);


CREATE TABLE IF NOT EXISTS `sitio`.`orden` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`descripcion` varchar(100) NOT NULL COMMENT 'Descripcion', 
`id_orden` int(9) NOT NULL COMMENT 'Id de Aprobacion', 
PRIMARY KEY (`id`) );

CREATE TABLE IF NOT EXISTS `sitio`.`cargos` 
( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clave primaria', 
`cargo_general` varchar(100) NOT NULL COMMENT 'Cargo General',
`cargo_sub` varchar(100) NOT NULL COMMENT 'Sub Cargo', 
`creador` varchar(50) NOT NULL,
`fecha_alta` datetime NOT NULL,
PRIMARY KEY (`id`) );

insert into `sitio`.orden values (5, 'Orden 5 (Sexta Linea)', 5);
insert into `sitio`.orden values (10, 'Orden 4 (Quinta Linea)', 10);
insert into `sitio`.orden values (15, 'Orden 3 (Cuarta Linea)', 15);
insert into `sitio`.orden values (20, 'Orden 2 (Tercer Linea)', 20);
insert into `sitio`.orden values (25, 'Orden 1 (Segunda Linea)', 25);
insert into `sitio`.orden values (30, 'Orden 0 (Primer Linea)', 30);
insert into `sitio`.orden values (35, 'Orden Admin (Primer Linea)', 35);