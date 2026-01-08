CREATE TABLE `Estudiante` (
  `id` serial PRIMARY KEY,
  `matricula` int UNIQUE,
  `nombre` varchar(255),
  `apellido_paterno` varchar(255),
  `apellido_materno` varchar(255),
  `usuario` varchar(255),
  `fecha_creacion` timestamp,
  `direccion` text,
  `grupo_id` int
);

CREATE TABLE `Tutor` (
  `id` serial PRIMARY KEY,
  `nombre` varchar(255),
  `apellido_paterno` varchar(255),
  `apellido_materno` varchar(255),
  `telefono` varchar(15),
  `email` varchar(255),
  `fecha_creacion` timestamp
);

CREATE TABLE `Estudiante_Tutor` (
  `id` serial PRIMARY KEY,
  `estudiante_id` int,
  `tutor_id` int,
  `parentesco` varchar(255),
  `es_responsable_pago` boolean,
  `recibe_notificaciones` boolean,
  `fecha_asignacion` timestamp
);

CREATE TABLE `Grado` (
  `id` serial PRIMARY KEY,
  `nombre` varchar(255),
  `nivel` varchar(255)
);

CREATE TABLE `Grupo` (
  `id` serial PRIMARY KEY,
  `nombre` varchar(255),
  `generacion` varchar(255),
  `descripcion` varchar(255),
  `fecha_creacion` timestamp,
  `grado_id` int
);

CREATE TABLE `Estado_Estudiante` (
  `id` serial PRIMARY KEY,
  `nombre` varchar(255),
  `descripcion` text
);

CREATE TABLE `Estado_Estudiante_Historial` (
  `id` serial PRIMARY KEY,
  `estudiante_id` int,
  `estado_id` int,
  `fecha` timestamp,
  `justificacion` text
);

CREATE TABLE `Estrato` (
  `id` serial PRIMARY KEY,
  `nombre` varchar(255),
  `descripcion` text,
  `porcentaje_descuento` decimal(10,2),
  `activo` boolean
);

CREATE TABLE `Evaluacion_Socioeconomica` (
  `id` serial PRIMARY KEY,
  `estudiante_id` int,
  `ingreso_mensual` decimal(10,2),
  `tipo_vivienda` varchar(255),
  `num_integrantes` int,
  `documentos` text,
  `estrato_sugerido_id` int,
  `fecha` timestamp
);

CREATE TABLE `Estrato_Historial` (
  `id` serial PRIMARY KEY,
  `estudiante_id` int,
  `estrato_id` int,
  `fecha` timestamp,
  `comentarios` text
);

CREATE TABLE `Concepto_Pagos` (
  `id` serial PRIMARY KEY,
  `nombre` varchar(255),
  `descripcion` text,
  `monto_base` decimal(10,2),
  `nivel_educativo` varchar(255)
);

CREATE TABLE `Adeudo` (
  `id` serial PRIMARY KEY,
  `estudiante_id` int,
  `concepto_id` int,
  `monto` decimal(10,2),
  `fecha_generacion` date,
  `fecha_vencimiento` date,
  `recargo_aplicado` decimal(10,2),
  `pagado` boolean
);

CREATE TABLE `Pago` (
  `id` serial PRIMARY KEY,
  `adeudo_id` int,
  `monto` decimal(10,2),
  `fecha` timestamp,
  `metodo` varchar(255),
  `comprobante` text
);

CREATE TABLE `Asistencia_Comedor` (
  `id` serial PRIMARY KEY,
  `estudiante_id` int,
  `fecha` date,
  `tipo_comida` varchar(255),
  `precio_aplicado` decimal(10,2)
);

ALTER TABLE `Estudiante` ADD FOREIGN KEY (`grupo_id`) REFERENCES `Grupo` (`id`);

ALTER TABLE `Estudiante_Tutor` ADD FOREIGN KEY (`estudiante_id`) REFERENCES `Estudiante` (`id`);

ALTER TABLE `Estudiante_Tutor` ADD FOREIGN KEY (`tutor_id`) REFERENCES `Tutor` (`id`);

ALTER TABLE `Grupo` ADD FOREIGN KEY (`grado_id`) REFERENCES `Grado` (`id`);

ALTER TABLE `Estado_Estudiante_Historial` ADD FOREIGN KEY (`estudiante_id`) REFERENCES `Estudiante` (`id`);

ALTER TABLE `Estado_Estudiante_Historial` ADD FOREIGN KEY (`estado_id`) REFERENCES `Estado_Estudiante` (`id`);

ALTER TABLE `Evaluacion_Socioeconomica` ADD FOREIGN KEY (`estudiante_id`) REFERENCES `Estudiante` (`id`);

ALTER TABLE `Evaluacion_Socioeconomica` ADD FOREIGN KEY (`estrato_sugerido_id`) REFERENCES `Estrato` (`id`);

ALTER TABLE `Estrato_Historial` ADD FOREIGN KEY (`estudiante_id`) REFERENCES `Estudiante` (`id`);

ALTER TABLE `Estrato_Historial` ADD FOREIGN KEY (`estrato_id`) REFERENCES `Estrato` (`id`);

ALTER TABLE `Adeudo` ADD FOREIGN KEY (`estudiante_id`) REFERENCES `Estudiante` (`id`);

ALTER TABLE `Adeudo` ADD FOREIGN KEY (`concepto_id`) REFERENCES `Concepto_Pagos` (`id`);

ALTER TABLE `Pago` ADD FOREIGN KEY (`adeudo_id`) REFERENCES `Adeudo` (`id`);

ALTER TABLE `Asistencia_Comedor` ADD FOREIGN KEY (`estudiante_id`) REFERENCES `Estudiante` (`id`);
