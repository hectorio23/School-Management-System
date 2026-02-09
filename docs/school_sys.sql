/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-12.1.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: school_sys
-- ------------------------------------------------------
-- Server version	12.1.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `Menu`
--

DROP TABLE IF EXISTS `Menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Menu` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(160) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `desactivar` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Menu`
--

LOCK TABLES `Menu` WRITE;
/*!40000 ALTER TABLE `Menu` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Menu` VALUES
(1,'Chilaquiles Rojos',45.00,0),
(2,'Molletes con Chorizo',40.00,0),
(3,'Comida Corrida del Dia',65.00,0),
(4,'Sandwich de Pollo',35.00,0),
(5,'Jugo de Naranja',20.00,0);
/*!40000 ALTER TABLE `Menu` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `adeudos`
--

DROP TABLE IF EXISTS `adeudos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `adeudos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `monto_base` decimal(10,2) NOT NULL,
  `descuento_aplicado` decimal(10,2) NOT NULL,
  `recargo_aplicado` decimal(10,2) NOT NULL,
  `monto_total` decimal(10,2) NOT NULL,
  `fecha_generacion` date NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `estatus` varchar(50) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `concepto_id` bigint(20) NOT NULL,
  `monto_pagado` decimal(10,2) NOT NULL,
  `generado_automaticamente` tinyint(1) NOT NULL,
  `justificacion_exencion` longtext DEFAULT NULL,
  `justificacion_manual` longtext DEFAULT NULL,
  `mes_correspondiente` date DEFAULT NULL,
  `recargo_exento` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_adeudo_estudiante` (`estudiante_id`),
  KEY `idx_adeudo_concepto` (`concepto_id`),
  KEY `idx_adeudo_vencimiento` (`fecha_vencimiento`),
  KEY `idx_adeudo_estatus` (`estatus`),
  KEY `idx_adeudo_seguimiento` (`estudiante_id`,`concepto_id`,`fecha_generacion`),
  CONSTRAINT `adeudos_concepto_id_de3b7d87_fk_conceptos_pago_id` FOREIGN KEY (`concepto_id`) REFERENCES `conceptos_pago` (`id`),
  CONSTRAINT `adeudos_estudiante_id_83cfd3e8_fk_estudiantes_matricula` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiantes` (`matricula`)
) ENGINE=InnoDB AUTO_INCREMENT=312 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adeudos`
--

LOCK TABLES `adeudos` WRITE;
/*!40000 ALTER TABLE `adeudos` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `adeudos` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `asistencia_cafeteria`
--

DROP TABLE IF EXISTS `asistencia_cafeteria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `asistencia_cafeteria` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha_asistencia` date NOT NULL,
  `tipo_comida` varchar(100) NOT NULL,
  `precio_aplicado` decimal(10,2) NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `menu_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asistencia_cafeteria_estudiante_id_fecha_asis_ff254b5c_uniq` (`estudiante_id`,`fecha_asistencia`,`tipo_comida`),
  KEY `idx_cafeteria_estudiante` (`estudiante_id`),
  KEY `idx_cafeteria_fecha` (`fecha_asistencia`),
  KEY `asistencia_cafeteria_menu_id_c53b8e68_fk_Menu_id` (`menu_id`),
  CONSTRAINT `asistencia_cafeteria_estudiante_id_3911c454_fk_estudiant` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiantes` (`matricula`),
  CONSTRAINT `asistencia_cafeteria_menu_id_c53b8e68_fk_Menu_id` FOREIGN KEY (`menu_id`) REFERENCES `Menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asistencia_cafeteria`
--

LOCK TABLES `asistencia_cafeteria` WRITE;
/*!40000 ALTER TABLE `asistencia_cafeteria` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `asistencia_cafeteria` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `aspirante_tutor`
--

DROP TABLE IF EXISTS `aspirante_tutor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `aspirante_tutor` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `parentesco` varchar(100) NOT NULL,
  `fecha_asignacion` datetime(6) NOT NULL,
  `tutor_id` bigint(20) NOT NULL,
  `aspirante_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `aspirante_tutor_aspirante_folio_tutor_id_5b8ddfbb_uniq` (`aspirante_id`,`tutor_id`),
  KEY `aspirante_tutor_tutor_id_ebc83d4a` (`tutor_id`),
  CONSTRAINT `aspirante_tutor_aspirante_id_5eee16ab_fk_aspirantes_id` FOREIGN KEY (`aspirante_id`) REFERENCES `aspirantes` (`id`),
  CONSTRAINT `aspirante_tutor_tutor_id_ebc83d4a_fk_tutor_temp_id` FOREIGN KEY (`tutor_id`) REFERENCES `tutor_temp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aspirante_tutor`
--

LOCK TABLES `aspirante_tutor` WRITE;
/*!40000 ALTER TABLE `aspirante_tutor` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `aspirante_tutor` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `aspirantes`
--

DROP TABLE IF EXISTS `aspirantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `aspirantes` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido_paterno` varchar(100) DEFAULT NULL,
  `apellido_materno` varchar(100) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `fecha_pago` datetime(6) DEFAULT NULL,
  `metodo_pago` varchar(100) DEFAULT NULL,
  `monto` decimal(10,2) NOT NULL,
  `notas` longtext DEFAULT NULL,
  `numero_referencia` varchar(255) DEFAULT NULL,
  `recibido_por` varchar(255) DEFAULT NULL,
  `ruta_recibo` longtext DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `aceptacion_reglamento` tinyint(1) NOT NULL,
  `acta_nacimiento_check` tinyint(1) NOT NULL,
  `autorizacion_imagen` tinyint(1) NOT NULL,
  `comprobante_domicilio` varchar(255) DEFAULT NULL,
  `curp` varchar(18) NOT NULL,
  `curp_check` tinyint(1) NOT NULL,
  `direccion` longtext DEFAULT NULL,
  `escuela_procedencia` varchar(255) DEFAULT NULL,
  `fase_actual` int(11) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `sexo` varchar(1) DEFAULT NULL,
  `ingreso_mensual_familiar` decimal(10,2) DEFAULT NULL,
  `internet_encasa` tinyint(1) NOT NULL,
  `miembros_hogar` int(11) DEFAULT NULL,
  `ocupacion_madre` varchar(100) DEFAULT NULL,
  `ocupacion_padre` varchar(100) DEFAULT NULL,
  `pagado_status` tinyint(1) NOT NULL,
  `promedio_anterior` decimal(4,2) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `tipo_vivienda` varchar(50) DEFAULT NULL,
  `vehiculos` int(11) DEFAULT NULL,
  `acta_nacimiento_estudiante` varchar(255) DEFAULT NULL,
  `acta_nacimiento_tutor` varchar(255) DEFAULT NULL,
  `curp_pdf` varchar(255) DEFAULT NULL,
  `curp_tutor_pdf` varchar(255) DEFAULT NULL,
  `acta_nacimiento` varchar(255) DEFAULT NULL,
  `boleta_ciclo_actual` varchar(255) DEFAULT NULL,
  `boleta_ciclo_anterior` varchar(255) DEFAULT NULL,
  `foto_credencial` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `curp` (`curp`),
  KEY `idx_aspirante_curp` (`curp`),
  KEY `idx_aspirante_fase` (`fase_actual`),
  CONSTRAINT `aspirantes_user_id_7887eb14_fk_usuarios_aspirantes_folio` FOREIGN KEY (`user_id`) REFERENCES `usuarios_aspirantes` (`folio`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aspirantes`
--

LOCK TABLES `aspirantes` WRITE;
/*!40000 ALTER TABLE `aspirantes` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `aspirantes` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_permission` VALUES
(1,'Can add user',1,'add_user'),
(2,'Can change user',1,'change_user'),
(3,'Can delete user',1,'delete_user'),
(4,'Can view user',1,'view_user'),
(5,'Can add log entry',2,'add_logentry'),
(6,'Can change log entry',2,'change_logentry'),
(7,'Can delete log entry',2,'delete_logentry'),
(8,'Can view log entry',2,'view_logentry'),
(9,'Can add permission',4,'add_permission'),
(10,'Can change permission',4,'change_permission'),
(11,'Can delete permission',4,'delete_permission'),
(12,'Can view permission',4,'view_permission'),
(13,'Can add group',3,'add_group'),
(14,'Can change group',3,'change_group'),
(15,'Can delete group',3,'delete_group'),
(16,'Can view group',3,'view_group'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add Estado de Estudiante',7,'add_estadoestudiante'),
(26,'Can change Estado de Estudiante',7,'change_estadoestudiante'),
(27,'Can delete Estado de Estudiante',7,'delete_estadoestudiante'),
(28,'Can view Estado de Estudiante',7,'view_estadoestudiante'),
(29,'Can add Estudiante',9,'add_estudiante'),
(30,'Can change Estudiante',9,'change_estudiante'),
(31,'Can delete Estudiante',9,'delete_estudiante'),
(32,'Can view Estudiante',9,'view_estudiante'),
(33,'Can add Estudiante-Tutor',10,'add_estudiantetutor'),
(34,'Can change Estudiante-Tutor',10,'change_estudiantetutor'),
(35,'Can delete Estudiante-Tutor',10,'delete_estudiantetutor'),
(36,'Can view Estudiante-Tutor',10,'view_estudiantetutor'),
(37,'Can add Evaluación Socioeconómica',11,'add_evaluacionsocioeconomica'),
(38,'Can change Evaluación Socioeconómica',11,'change_evaluacionsocioeconomica'),
(39,'Can delete Evaluación Socioeconómica',11,'delete_evaluacionsocioeconomica'),
(40,'Can view Evaluación Socioeconómica',11,'view_evaluacionsocioeconomica'),
(41,'Can add Grado',12,'add_grado'),
(42,'Can change Grado',12,'change_grado'),
(43,'Can delete Grado',12,'delete_grado'),
(44,'Can view Grado',12,'view_grado'),
(45,'Can add Grupo',13,'add_grupo'),
(46,'Can change Grupo',13,'change_grupo'),
(47,'Can delete Grupo',13,'delete_grupo'),
(48,'Can view Grupo',13,'view_grupo'),
(49,'Can add Historial de Estado',14,'add_historialestadosestudiante'),
(50,'Can change Historial de Estado',14,'change_historialestadosestudiante'),
(51,'Can delete Historial de Estado',14,'delete_historialestadosestudiante'),
(52,'Can view Historial de Estado',14,'view_historialestadosestudiante'),
(53,'Can add Tutor',15,'add_tutor'),
(54,'Can change Tutor',15,'change_tutor'),
(55,'Can delete Tutor',15,'delete_tutor'),
(56,'Can view Tutor',15,'view_tutor'),
(57,'Can add Estrato',8,'add_estrato'),
(58,'Can change Estrato',8,'change_estrato'),
(59,'Can delete Estrato',8,'delete_estrato'),
(60,'Can view Estrato',8,'view_estrato'),
(61,'Can add Asistencia de Cafetería',16,'add_asistenciacafeteria'),
(62,'Can change Asistencia de Cafetería',16,'change_asistenciacafeteria'),
(63,'Can delete Asistencia de Cafetería',16,'delete_asistenciacafeteria'),
(64,'Can view Asistencia de Cafetería',16,'view_asistenciacafeteria'),
(65,'Can add Concepto de Pago',18,'add_conceptopago'),
(66,'Can change Concepto de Pago',18,'change_conceptopago'),
(67,'Can delete Concepto de Pago',18,'delete_conceptopago'),
(68,'Can view Concepto de Pago',18,'view_conceptopago'),
(69,'Can add Adeudo',17,'add_adeudo'),
(70,'Can change Adeudo',17,'change_adeudo'),
(71,'Can delete Adeudo',17,'delete_adeudo'),
(72,'Can view Adeudo',17,'view_adeudo'),
(73,'Can add Pago',19,'add_pago'),
(74,'Can change Pago',19,'change_pago'),
(75,'Can delete Pago',19,'delete_pago'),
(76,'Can view Pago',19,'view_pago'),
(77,'Can add Menú',20,'add_menu'),
(78,'Can change Menú',20,'change_menu'),
(79,'Can delete Menú',20,'delete_menu'),
(80,'Can view Menú',20,'view_menu'),
(81,'Can add Menu Semanal',21,'add_menusemanal'),
(82,'Can change Menu Semanal',21,'change_menusemanal'),
(83,'Can delete Menu Semanal',21,'delete_menusemanal'),
(84,'Can view Menu Semanal',21,'view_menusemanal'),
(85,'Can add Configuracion de Pago',22,'add_configuracionpago'),
(86,'Can change Configuracion de Pago',22,'change_configuracionpago'),
(87,'Can delete Configuracion de Pago',22,'delete_configuracionpago'),
(88,'Can view Configuracion de Pago',22,'view_configuracionpago'),
(89,'Can add Dia No Habil',23,'add_dianohabil'),
(90,'Can change Dia No Habil',23,'change_dianohabil'),
(91,'Can delete Dia No Habil',23,'delete_dianohabil'),
(92,'Can view Dia No Habil',23,'view_dianohabil'),
(93,'Can add Beca',24,'add_beca'),
(94,'Can change Beca',24,'change_beca'),
(95,'Can delete Beca',24,'delete_beca'),
(96,'Can view Beca',24,'view_beca'),
(97,'Can add Beca-Estudiante',25,'add_becaestudiante'),
(98,'Can change Beca-Estudiante',25,'change_becaestudiante'),
(99,'Can delete Beca-Estudiante',25,'delete_becaestudiante'),
(100,'Can view Beca-Estudiante',25,'view_becaestudiante'),
(101,'Can add Tutor',26,'add_admissiontutor'),
(102,'Can change Tutor',26,'change_admissiontutor'),
(103,'Can delete Tutor',26,'delete_admissiontutor'),
(104,'Can view Tutor',26,'view_admissiontutor'),
(105,'Can add usuario',28,'add_admissionuser'),
(106,'Can change usuario',28,'change_admissionuser'),
(107,'Can delete usuario',28,'delete_admissionuser'),
(108,'Can view usuario',28,'view_admissionuser'),
(109,'Can add Aspirante',29,'add_aspirante'),
(110,'Can change Aspirante',29,'change_aspirante'),
(111,'Can delete Aspirante',29,'delete_aspirante'),
(112,'Can view Aspirante',29,'view_aspirante'),
(113,'Can add Tutor',27,'add_admissiontutoraspirante'),
(114,'Can change Tutor',27,'change_admissiontutoraspirante'),
(115,'Can delete Tutor',27,'delete_admissiontutoraspirante'),
(116,'Can view Tutor',27,'view_admissiontutoraspirante'),
(117,'Can add verification code',30,'add_verificationcode'),
(118,'Can change verification code',30,'change_verificationcode'),
(119,'Can delete verification code',30,'delete_verificationcode'),
(120,'Can view verification code',30,'view_verificationcode'),
(121,'Can add Ciclo Escolar',31,'add_cicloescolar'),
(122,'Can change Ciclo Escolar',31,'change_cicloescolar'),
(123,'Can delete Ciclo Escolar',31,'delete_cicloescolar'),
(124,'Can view Ciclo Escolar',31,'view_cicloescolar'),
(125,'Can add Inscripción',32,'add_inscripcion'),
(126,'Can change Inscripción',32,'change_inscripcion'),
(127,'Can delete Inscripción',32,'delete_inscripcion'),
(128,'Can view Inscripción',32,'view_inscripcion'),
(129,'Can add Nivel Educativo',33,'add_niveleducativo'),
(130,'Can change Nivel Educativo',33,'change_niveleducativo'),
(131,'Can delete Nivel Educativo',33,'delete_niveleducativo'),
(132,'Can view Nivel Educativo',33,'view_niveleducativo');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `becas`
--

DROP TABLE IF EXISTS `becas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `becas` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext DEFAULT NULL,
  `porcentaje` decimal(5,2) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `valida` tinyint(1) NOT NULL,
  `creado_en` datetime(6) NOT NULL,
  `actualizado_en` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_beca_valida` (`valida`),
  KEY `idx_beca_vencimiento` (`fecha_vencimiento`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `becas`
--

LOCK TABLES `becas` WRITE;
/*!40000 ALTER TABLE `becas` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `becas` VALUES
(1,'Beca 10%','Esta es una beca que corresponde al 10% del descuento para el estudiante en todos los adeudos que se generen a partir de que se e asigno la beca.',10.00,'2026-01-19','2026-01-31',1,'2026-01-19 19:53:58.474599','2026-01-19 19:53:58.474642');
/*!40000 ALTER TABLE `becas` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `becas_estudiantes`
--

DROP TABLE IF EXISTS `becas_estudiantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `becas_estudiantes` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha_asignacion` datetime(6) NOT NULL,
  `fecha_retiro` datetime(6) DEFAULT NULL,
  `activa` tinyint(1) NOT NULL,
  `motivo_retiro` longtext DEFAULT NULL,
  `asignado_por` varchar(255) DEFAULT NULL,
  `beca_id` bigint(20) NOT NULL,
  `estudiante_matricula` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_becaestudiante_beca` (`beca_id`),
  KEY `idx_becaestudiante_estudiante` (`estudiante_matricula`),
  KEY `idx_becaestudiante_activa` (`activa`),
  CONSTRAINT `becas_estudiantes_beca_id_2a0ca692_fk_becas_id` FOREIGN KEY (`beca_id`) REFERENCES `becas` (`id`),
  CONSTRAINT `becas_estudiantes_estudiante_matricula_f6515dcd_fk_estudiant` FOREIGN KEY (`estudiante_matricula`) REFERENCES `estudiantes` (`matricula`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `becas_estudiantes`
--

LOCK TABLES `becas_estudiantes` WRITE;
/*!40000 ALTER TABLE `becas_estudiantes` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `becas_estudiantes` VALUES
(11,'2026-01-27 20:22:47.144100',NULL,1,'',NULL,1,1000),
(12,'2026-01-27 22:51:05.279926',NULL,1,'',NULL,1,1001);
/*!40000 ALTER TABLE `becas_estudiantes` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `ciclos_escolares`
--

DROP TABLE IF EXISTS `ciclos_escolares`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ciclos_escolares` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ciclos_escolares`
--

LOCK TABLES `ciclos_escolares` WRITE;
/*!40000 ALTER TABLE `ciclos_escolares` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `ciclos_escolares` VALUES
(1,'2024-2025','2024-08-20','2025-07-15',1,'2026-01-27 16:54:17.343505','2026-01-27 23:50:15.108012');
/*!40000 ALTER TABLE `ciclos_escolares` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `conceptos_pago`
--

DROP TABLE IF EXISTS `conceptos_pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `conceptos_pago` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `monto_base` decimal(10,2) NOT NULL,
  `nivel_educativo` varchar(100) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `tipo_concepto` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `conceptos_pago_nombre_nivel_educativo_8f94b81a_uniq` (`nombre`,`nivel_educativo`),
  KEY `idx_concepto_activo` (`activo`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conceptos_pago`
--

LOCK TABLES `conceptos_pago` WRITE;
/*!40000 ALTER TABLE `conceptos_pago` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `conceptos_pago` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `configuracion_pago`
--

DROP TABLE IF EXISTS `configuracion_pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `configuracion_pago` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `dia_inicio_ordinario` int(11) NOT NULL,
  `dia_fin_ordinario` int(11) NOT NULL,
  `porcentaje_recargo` decimal(5,2) NOT NULL,
  `monto_fijo_recargo` decimal(10,2) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configuracion_pago`
--

LOCK TABLES `configuracion_pago` WRITE;
/*!40000 ALTER TABLE `configuracion_pago` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `configuracion_pago` VALUES
(1,1,10,10.00,125.00,1);
/*!40000 ALTER TABLE `configuracion_pago` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `dias_no_habiles`
--

DROP TABLE IF EXISTS `dias_no_habiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `dias_no_habiles` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fecha` (`fecha`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dias_no_habiles`
--

LOCK TABLES `dias_no_habiles` WRITE;
/*!40000 ALTER TABLE `dias_no_habiles` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `dias_no_habiles` VALUES
(1,'2025-02-05','Dia de la Constitucion'),
(2,'2025-03-17','Natalicio de Benito Juarez'),
(3,'2025-05-01','Dia del Trabajo');
/*!40000 ALTER TABLE `dias_no_habiles` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=670 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_admin_log` VALUES
(6,'2026-01-14 21:43:47.386261','2','DSGM - 2022-2026',1,'[{\"added\": {}}]',13,6),
(7,'2026-01-14 21:44:24.556167','3','ROBERTA OLED JARAMILLO',1,'[{\"added\": {}}]',15,6),
(8,'2026-01-14 21:45:02.978444','4','JASSIEL NUÑEZ PEDROZA',1,'[{\"added\": {}}]',15,6),
(9,'2026-01-14 21:46:54.128029','1','B (20.00%)',2,'[]',8,6),
(10,'2026-01-19 15:47:36.228580','220550','220550 - Maria Hernandez',2,'[{\"added\": {\"name\": \"Estudiante-Tutor\", \"object\": \"220550 - Maria Hernandez -> ROBERTA OLED JARAMILLO (Madre)\"}}, {\"added\": {\"name\": \"Estudiante-Tutor\", \"object\": \"220550 - Maria Hernandez -> JASSIEL NU\\u00d1EZ PEDROZA (Padre)\"}}]',9,6),
(11,'2026-01-19 19:39:58.848070','7','Colegiatura ENERO - Todos',2,'[{\"changed\": {\"fields\": [\"Nombre\", \"Descripcion\"]}}]',18,6),
(12,'2026-01-19 19:40:29.958642','193','220330 - MAURICER PANDILLA - Colegiatura ENERO - Todos ($500.00)',3,'',17,6),
(13,'2026-01-19 19:40:29.958695','192','220330 - MAURICER PANDILLA - Colegiatura ENERO - Todos ($500.00)',3,'',17,6),
(14,'2026-01-19 19:40:29.958719','191','220330 - MAURICER PANDILLA - Colegiatura ENERO - Todos ($500.00)',3,'',17,6),
(15,'2026-01-19 19:40:29.958743','190','220330 - MAURICER PANDILLA - Colegiatura ENERO - Todos ($500.00)',3,'',17,6),
(16,'2026-01-19 19:40:29.958765','189','220330 - MAURICER PANDILLA - Colegiatura ENERO - Todos ($500.00)',3,'',17,6),
(17,'2026-01-19 19:40:29.958787','188','220609 - Luis Martinez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(18,'2026-01-19 19:40:29.958809','187','220609 - Luis Martinez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(19,'2026-01-19 19:40:29.958830','186','220609 - Luis Martinez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(20,'2026-01-19 19:40:29.958850','185','220608 - Lucia Sanchez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(21,'2026-01-19 19:40:29.958870','184','220608 - Lucia Sanchez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(22,'2026-01-19 19:40:29.958890','183','220608 - Lucia Sanchez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(23,'2026-01-19 19:40:29.958911','182','220607 - Jorge Sanchez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(24,'2026-01-19 19:40:29.958947','181','220607 - Jorge Sanchez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(25,'2026-01-19 19:40:29.958967','180','220607 - Jorge Sanchez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(26,'2026-01-19 19:40:29.958987','179','220606 - Maria Garcia - COLEGIATURA - General ($2240.00)',3,'',17,6),
(27,'2026-01-19 19:40:29.959007','178','220606 - Maria Garcia - COLEGIATURA - General ($2240.00)',3,'',17,6),
(28,'2026-01-19 19:40:29.959027','177','220606 - Maria Garcia - COLEGIATURA - General ($2240.00)',3,'',17,6),
(29,'2026-01-19 19:40:29.959047','176','220605 - Lucia Lopez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(30,'2026-01-19 19:40:29.959067','175','220605 - Lucia Lopez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(31,'2026-01-19 19:40:29.959087','174','220605 - Lucia Lopez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(32,'2026-01-19 19:40:29.959107','173','220604 - Miguel Hernandez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(33,'2026-01-19 19:40:29.959126','172','220604 - Miguel Hernandez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(34,'2026-01-19 19:40:29.959147','171','220604 - Miguel Hernandez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(35,'2026-01-19 19:40:29.959166','170','220603 - Pedro Hernandez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(36,'2026-01-19 19:40:29.959185','169','220603 - Pedro Hernandez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(37,'2026-01-19 19:40:29.959206','168','220603 - Pedro Hernandez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(38,'2026-01-19 19:40:29.959226','167','220602 - Sofia Perez - COLEGIATURA - General ($700.00)',3,'',17,6),
(39,'2026-01-19 19:40:29.959245','166','220602 - Sofia Perez - COLEGIATURA - General ($700.00)',3,'',17,6),
(40,'2026-01-19 19:40:29.959265','165','220602 - Sofia Perez - COLEGIATURA - General ($700.00)',3,'',17,6),
(41,'2026-01-19 19:40:29.959285','164','220601 - Maria Hernandez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(42,'2026-01-19 19:40:29.959304','163','220601 - Maria Hernandez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(43,'2026-01-19 19:40:29.959324','162','220601 - Maria Hernandez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(44,'2026-01-19 19:40:29.959343','161','220600 - Elena Perez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(45,'2026-01-19 19:40:29.959364','160','220600 - Elena Perez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(46,'2026-01-19 19:40:29.959383','159','220600 - Elena Perez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(47,'2026-01-19 19:40:29.959402','158','220599 - Carlos Martinez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(48,'2026-01-19 19:40:29.959422','157','220599 - Carlos Martinez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(49,'2026-01-19 19:40:29.959442','156','220599 - Carlos Martinez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(50,'2026-01-19 19:40:29.959462','155','220598 - Maria Sanchez - COLEGIATURA - General ($700.00)',3,'',17,6),
(51,'2026-01-19 19:40:29.959481','154','220598 - Maria Sanchez - COLEGIATURA - General ($700.00)',3,'',17,6),
(52,'2026-01-19 19:40:29.959501','153','220598 - Maria Sanchez - COLEGIATURA - General ($700.00)',3,'',17,6),
(53,'2026-01-19 19:40:29.959521','152','220597 - Jorge Gonzalez - COLEGIATURA - General ($700.00)',3,'',17,6),
(54,'2026-01-19 19:40:29.959540','151','220597 - Jorge Gonzalez - COLEGIATURA - General ($700.00)',3,'',17,6),
(55,'2026-01-19 19:40:29.959560','150','220597 - Jorge Gonzalez - COLEGIATURA - General ($700.00)',3,'',17,6),
(56,'2026-01-19 19:40:29.959580','149','220596 - Elena Martinez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(57,'2026-01-19 19:40:29.959600','148','220596 - Elena Martinez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(58,'2026-01-19 19:40:29.959620','147','220596 - Elena Martinez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(59,'2026-01-19 19:40:29.959639','146','220595 - Miguel Perez - COLEGIATURA - General ($700.00)',3,'',17,6),
(60,'2026-01-19 19:40:29.959658','145','220595 - Miguel Perez - COLEGIATURA - General ($700.00)',3,'',17,6),
(61,'2026-01-19 19:40:29.959677','144','220595 - Miguel Perez - COLEGIATURA - General ($700.00)',3,'',17,6),
(62,'2026-01-19 19:40:29.959697','143','220594 - Miguel Gonzalez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(63,'2026-01-19 19:40:29.959717','142','220594 - Miguel Gonzalez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(64,'2026-01-19 19:40:29.959738','141','220594 - Miguel Gonzalez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(65,'2026-01-19 19:40:29.959758','140','220593 - Lucia Sanchez - COLEGIATURA - General ($700.00)',3,'',17,6),
(66,'2026-01-19 19:40:29.959777','139','220593 - Lucia Sanchez - COLEGIATURA - General ($700.00)',3,'',17,6),
(67,'2026-01-19 19:40:29.959797','138','220593 - Lucia Sanchez - COLEGIATURA - General ($700.00)',3,'',17,6),
(68,'2026-01-19 19:40:29.959816','137','220592 - Carlos Perez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(69,'2026-01-19 19:40:29.959835','136','220592 - Carlos Perez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(70,'2026-01-19 19:40:29.959853','135','220592 - Carlos Perez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(71,'2026-01-19 19:40:29.959873','134','220591 - Elena Martinez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(72,'2026-01-19 19:40:29.959892','133','220591 - Elena Martinez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(73,'2026-01-19 19:40:29.959910','132','220591 - Elena Martinez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(74,'2026-01-19 19:40:29.959943','131','220590 - Sofia Lopez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(75,'2026-01-19 19:40:29.959962','130','220590 - Sofia Lopez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(76,'2026-01-19 19:40:29.959981','129','220590 - Sofia Lopez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(77,'2026-01-19 19:40:29.960000','128','220589 - Pedro Hernandez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(78,'2026-01-19 19:40:29.960019','127','220589 - Pedro Hernandez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(79,'2026-01-19 19:40:29.960038','126','220589 - Pedro Hernandez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(80,'2026-01-19 19:40:29.960059','125','220588 - Maria Perez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(81,'2026-01-19 19:40:29.960079','124','220588 - Maria Perez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(82,'2026-01-19 19:40:29.960097','123','220588 - Maria Perez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(83,'2026-01-19 19:40:29.960116','122','220587 - Lucia Gonzalez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(84,'2026-01-19 19:40:29.960134','121','220587 - Lucia Gonzalez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(85,'2026-01-19 19:40:29.960153','120','220587 - Lucia Gonzalez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(86,'2026-01-19 19:40:29.960172','119','220586 - Sofia Sanchez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(87,'2026-01-19 19:40:29.960191','118','220586 - Sofia Sanchez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(88,'2026-01-19 19:40:29.960209','117','220586 - Sofia Sanchez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(89,'2026-01-19 19:40:29.960229','116','220585 - Ana Perez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(90,'2026-01-19 19:40:29.960248','115','220585 - Ana Perez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(91,'2026-01-19 19:40:29.960266','114','220585 - Ana Perez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(92,'2026-01-19 19:40:29.960284','113','220584 - Jorge Rodriguez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(93,'2026-01-19 19:40:29.960304','112','220584 - Jorge Rodriguez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(94,'2026-01-19 19:40:29.960330','111','220584 - Jorge Rodriguez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(95,'2026-01-19 19:40:29.960349','110','220583 - Carlos Hernandez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(96,'2026-01-19 19:40:29.960368','109','220583 - Carlos Hernandez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(97,'2026-01-19 19:40:29.960386','108','220583 - Carlos Hernandez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(98,'2026-01-19 19:40:29.960404','107','220582 - Elena Rodriguez - COLEGIATURA - General ($700.00)',3,'',17,6),
(99,'2026-01-19 19:40:29.960423','106','220582 - Elena Rodriguez - COLEGIATURA - General ($700.00)',3,'',17,6),
(100,'2026-01-19 19:40:29.960442','105','220582 - Elena Rodriguez - COLEGIATURA - General ($700.00)',3,'',17,6),
(101,'2026-01-19 19:40:29.960460','104','220581 - Luis Hernandez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(102,'2026-01-19 19:40:29.960479','103','220581 - Luis Hernandez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(103,'2026-01-19 19:40:29.960497','102','220581 - Luis Hernandez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(104,'2026-01-19 19:40:29.960516','101','220580 - Jorge Lopez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(105,'2026-01-19 19:40:29.960535','100','220580 - Jorge Lopez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(106,'2026-01-19 19:40:29.960555','99','220580 - Jorge Lopez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(107,'2026-01-19 19:40:29.960574','98','220579 - Ana Rodriguez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(108,'2026-01-19 19:40:29.960593','97','220579 - Ana Rodriguez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(109,'2026-01-19 19:40:29.960612','96','220579 - Ana Rodriguez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(110,'2026-01-19 19:40:29.960631','95','220578 - Luis Martinez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(111,'2026-01-19 19:40:29.960650','94','220578 - Luis Martinez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(112,'2026-01-19 19:40:50.000186','93','220578 - Luis Martinez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(113,'2026-01-19 19:40:50.000260','92','220577 - Luis Sanchez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(114,'2026-01-19 19:40:50.000303','91','220577 - Luis Sanchez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(115,'2026-01-19 19:40:50.000344','90','220577 - Luis Sanchez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(116,'2026-01-19 19:40:50.000383','89','220576 - Jorge Perez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(117,'2026-01-19 19:40:50.000420','88','220576 - Jorge Perez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(118,'2026-01-19 19:40:50.000456','87','220576 - Jorge Perez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(119,'2026-01-19 19:40:50.000490','86','220575 - Maria Gonzalez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(120,'2026-01-19 19:40:50.000524','85','220575 - Maria Gonzalez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(121,'2026-01-19 19:40:50.000558','84','220575 - Maria Gonzalez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(122,'2026-01-19 19:40:50.000593','83','220574 - Pedro Perez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(123,'2026-01-19 19:40:50.000629','82','220574 - Pedro Perez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(124,'2026-01-19 19:40:50.000662','81','220574 - Pedro Perez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(125,'2026-01-19 19:40:50.000698','80','220573 - Miguel Martinez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(126,'2026-01-19 19:40:50.000733','79','220573 - Miguel Martinez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(127,'2026-01-19 19:40:50.000768','78','220573 - Miguel Martinez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(128,'2026-01-19 19:40:50.000801','77','220572 - Lucia Perez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(129,'2026-01-19 19:40:50.000835','76','220572 - Lucia Perez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(130,'2026-01-19 19:40:50.000871','75','220572 - Lucia Perez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(131,'2026-01-19 19:40:50.000908','74','220571 - Lucia Perez - COLEGIATURA - General ($700.00)',3,'',17,6),
(132,'2026-01-19 19:40:50.000963','73','220571 - Lucia Perez - COLEGIATURA - General ($700.00)',3,'',17,6),
(133,'2026-01-19 19:40:50.000999','72','220571 - Lucia Perez - COLEGIATURA - General ($700.00)',3,'',17,6),
(134,'2026-01-19 19:40:50.001032','71','220570 - Pedro Lopez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(135,'2026-01-19 19:40:50.001066','70','220570 - Pedro Lopez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(136,'2026-01-19 19:40:50.001098','69','220570 - Pedro Lopez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(137,'2026-01-19 19:40:50.001131','68','220569 - Luis Garcia - COLEGIATURA - General ($700.00)',3,'',17,6),
(138,'2026-01-19 19:40:50.001166','67','220569 - Luis Garcia - COLEGIATURA - General ($700.00)',3,'',17,6),
(139,'2026-01-19 19:40:50.001199','66','220569 - Luis Garcia - COLEGIATURA - General ($700.00)',3,'',17,6),
(140,'2026-01-19 19:40:50.001231','65','220568 - Carlos Sanchez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(141,'2026-01-19 19:40:50.001263','64','220568 - Carlos Sanchez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(142,'2026-01-19 19:40:50.001296','63','220568 - Carlos Sanchez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(143,'2026-01-19 19:40:50.001328','62','220567 - Lucia Perez - COLEGIATURA - General ($700.00)',3,'',17,6),
(144,'2026-01-19 19:40:50.001364','61','220567 - Lucia Perez - COLEGIATURA - General ($700.00)',3,'',17,6),
(145,'2026-01-19 19:40:50.001398','60','220567 - Lucia Perez - COLEGIATURA - General ($700.00)',3,'',17,6),
(146,'2026-01-19 19:40:50.001432','59','220566 - Luis Gonzalez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(147,'2026-01-19 19:40:50.001467','58','220566 - Luis Gonzalez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(148,'2026-01-19 19:40:50.001500','57','220566 - Luis Gonzalez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(149,'2026-01-19 19:40:50.001532','56','220565 - Carlos Gonzalez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(150,'2026-01-19 19:40:50.001567','55','220565 - Carlos Gonzalez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(151,'2026-01-19 19:40:50.001602','54','220565 - Carlos Gonzalez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(152,'2026-01-19 19:40:50.001638','53','220564 - Lucia Lopez - COLEGIATURA - General ($700.00)',3,'',17,6),
(153,'2026-01-19 19:40:50.001674','52','220564 - Lucia Lopez - COLEGIATURA - General ($700.00)',3,'',17,6),
(154,'2026-01-19 19:40:50.001720','51','220564 - Lucia Lopez - COLEGIATURA - General ($700.00)',3,'',17,6),
(155,'2026-01-19 19:40:50.001757','50','220563 - Maria Sanchez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(156,'2026-01-19 19:40:50.001793','49','220563 - Maria Sanchez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(157,'2026-01-19 19:40:50.001829','48','220563 - Maria Sanchez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(158,'2026-01-19 19:40:50.001862','47','220562 - Maria Gonzalez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(159,'2026-01-19 19:40:50.001898','46','220562 - Maria Gonzalez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(160,'2026-01-19 19:40:50.001948','45','220562 - Maria Gonzalez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(161,'2026-01-19 19:40:50.001983','44','220561 - Luis Garcia - COLEGIATURA - General ($2520.00)',3,'',17,6),
(162,'2026-01-19 19:40:50.002017','43','220561 - Luis Garcia - COLEGIATURA - General ($2520.00)',3,'',17,6),
(163,'2026-01-19 19:40:50.002051','42','220561 - Luis Garcia - COLEGIATURA - General ($2520.00)',3,'',17,6),
(164,'2026-01-19 19:40:50.002086','41','220560 - Pedro Gonzalez - COLEGIATURA - General ($700.00)',3,'',17,6),
(165,'2026-01-19 19:40:50.002119','40','220560 - Pedro Gonzalez - COLEGIATURA - General ($700.00)',3,'',17,6),
(166,'2026-01-19 19:40:50.002154','39','220560 - Pedro Gonzalez - COLEGIATURA - General ($700.00)',3,'',17,6),
(167,'2026-01-19 19:40:50.002188','38','220559 - Carlos Gonzalez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(168,'2026-01-19 19:40:50.002223','37','220559 - Carlos Gonzalez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(169,'2026-01-19 19:40:50.002257','36','220559 - Carlos Gonzalez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(170,'2026-01-19 19:40:50.002291','35','220558 - Jorge Rodriguez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(171,'2026-01-19 19:40:50.002326','34','220558 - Jorge Rodriguez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(172,'2026-01-19 19:40:50.002360','33','220558 - Jorge Rodriguez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(173,'2026-01-19 19:40:50.002395','32','220557 - Carlos Gonzalez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(174,'2026-01-19 19:40:50.002430','31','220557 - Carlos Gonzalez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(175,'2026-01-19 19:40:50.002465','30','220557 - Carlos Gonzalez - COLEGIATURA - General ($2240.00)',3,'',17,6),
(176,'2026-01-19 19:40:50.002500','29','220556 - Sofia Hernandez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(177,'2026-01-19 19:40:50.002538','28','220556 - Sofia Hernandez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(178,'2026-01-19 19:40:50.002574','27','220556 - Sofia Hernandez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(179,'2026-01-19 19:40:50.002609','26','220555 - Carlos Garcia - COLEGIATURA - General ($2100.00)',3,'',17,6),
(180,'2026-01-19 19:40:50.002644','25','220555 - Carlos Garcia - COLEGIATURA - General ($2100.00)',3,'',17,6),
(181,'2026-01-19 19:40:50.002679','24','220555 - Carlos Garcia - COLEGIATURA - General ($2100.00)',3,'',17,6),
(182,'2026-01-19 19:40:50.002714','23','220554 - Miguel Martinez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(183,'2026-01-19 19:40:50.002747','22','220554 - Miguel Martinez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(184,'2026-01-19 19:40:50.002780','21','220554 - Miguel Martinez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(185,'2026-01-19 19:40:50.002813','20','220553 - Sofia Sanchez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(186,'2026-01-19 19:40:50.002845','19','220553 - Sofia Sanchez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(187,'2026-01-19 19:40:50.002879','18','220553 - Sofia Sanchez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(188,'2026-01-19 19:40:50.002913','17','220552 - Jorge Rodriguez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(189,'2026-01-19 19:40:50.002970','16','220552 - Jorge Rodriguez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(190,'2026-01-19 19:40:50.003007','15','220552 - Jorge Rodriguez - COLEGIATURA - General ($1400.00)',3,'',17,6),
(191,'2026-01-19 19:40:50.003040','14','220551 - Maria Rodriguez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(192,'2026-01-19 19:40:50.003075','13','220551 - Maria Rodriguez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(193,'2026-01-19 19:40:50.003117','12','220551 - Maria Rodriguez - COLEGIATURA - General ($2100.00)',3,'',17,6),
(194,'2026-01-19 19:40:50.003153','11','220550 - Maria Hernandez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(195,'2026-01-19 19:40:50.003188','10','220550 - Maria Hernandez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(196,'2026-01-19 19:40:50.003220','9','220550 - Maria Hernandez - COLEGIATURA - General ($2520.00)',3,'',17,6),
(197,'2026-01-19 19:40:50.003255','8','220549 - Estudiante Prueba - Inscripción - General ($1000.00)',3,'',17,6),
(198,'2026-01-19 19:40:50.003289','1','220548 - MARIANA FLOWERS - Colegiatura Enero - Universidad ($4000.00)',3,'',17,6),
(199,'2026-01-19 19:41:15.339137','7','Colegiatura ENERO - Todos',3,'',18,6),
(200,'2026-01-19 19:41:15.339181','6','COMEDOR - General',3,'',18,6),
(201,'2026-01-19 19:41:15.339203','5','UNIFORME - General',3,'',18,6),
(202,'2026-01-19 19:41:15.339222','4','LIBROS - General',3,'',18,6),
(203,'2026-01-19 19:41:15.339240','3','COLEGIATURA - General',3,'',18,6),
(204,'2026-01-19 19:41:15.339258','1','Colegiatura Enero - Universidad',3,'',18,6),
(205,'2026-01-19 19:42:30.594536','2','Inscripción - Primaria',2,'[{\"changed\": {\"fields\": [\"Descripcion\", \"Nivel educativo\", \"Generar por Escolaridad (Nivel)\"]}}]',18,6),
(206,'2026-01-19 19:42:51.787449','2','Inscripción - Primaria',2,'[{\"changed\": {\"fields\": [\"Generar por Escolaridad (Nivel)\"]}}]',18,6),
(207,'2026-01-19 19:43:50.002319','194','220548 - MARIANA FLOWERS - Inscripción - Primaria ($1000)',1,'[{\"added\": {}}]',17,6),
(208,'2026-01-19 19:44:31.137874','65','Pago $1000 - 2026-01-19',1,'[{\"added\": {}}]',19,6),
(209,'2026-01-19 19:53:58.478731','1','Beca 10% (10%) - Vigente',1,'[{\"added\": {}}, {\"added\": {\"name\": \"Beca-Estudiante\", \"object\": \"220548 - MARIANA FLOWERS - Beca 10% (Activa)\"}}]',24,6),
(210,'2026-01-19 19:58:41.160371','8','Colegiatura Enero 2026 - Secundaria',1,'[{\"added\": {}}]',18,6),
(211,'2026-01-19 19:59:50.919437','195','220548 - MARIANA FLOWERS - Colegiatura Enero 2026 - Secundaria ($500)',1,'[{\"added\": {}}]',17,6),
(212,'2026-01-19 21:34:50.730332','194','220548 - MARIANA FLOWERS - Inscripción - Primaria ($1000.00)',3,'',17,6),
(213,'2026-01-19 21:36:08.542767','196','220548 - MARIANA FLOWERS - Colegiatura Enero 2026 - Secundaria ($350.000)',1,'[{\"added\": {}}]',17,6),
(214,'2026-01-19 21:36:29.571752','195','220548 - MARIANA FLOWERS - Colegiatura Enero 2026 - Secundaria ($500.00)',3,'',17,6),
(215,'2026-01-19 21:47:05.231802','197','220548 - MARIANA FLOWERS - Colegiatura Enero 2026 - Secundaria ($350.000)',1,'[{\"added\": {}}]',17,6),
(216,'2026-01-19 21:50:24.756777','197','220548 - MARIANA FLOWERS - Colegiatura Enero 2026 - Secundaria ($350.00)',3,'',17,6),
(217,'2026-01-19 21:50:35.176877','196','220548 - MARIANA FLOWERS - Colegiatura Enero 2026 - Secundaria ($350.00)',3,'',17,6),
(218,'2026-01-19 21:50:53.067091','198','220548 - MARIANA FLOWERS - Colegiatura Enero 2026 - Secundaria ($350.000)',1,'[{\"added\": {}}]',17,6),
(219,'2026-01-19 21:53:24.241232','220548','220548 - MARIANA FLOWERS',2,'[{\"added\": {\"name\": \"Evaluaci\\u00f3n Socioecon\\u00f3mica\", \"object\": \"[+] Evaluaci\\u00f3n 220548 - MARIANA FLOWERS - Aprobada\"}}]',9,6),
(220,'2026-01-19 21:53:50.478739','199','220548 - MARIANA FLOWERS - Colegiatura Enero 2026 - Secundaria ($400.000)',1,'[{\"added\": {}}]',17,6),
(221,'2026-01-19 21:56:04.865949','66','Pago $500 - 2026-01-19',1,'[{\"added\": {}}]',19,6),
(222,'2026-01-20 17:21:34.002202','67','Pago $400.00 - 2026-01-20',1,'[{\"added\": {}}]',19,6),
(223,'2026-01-20 17:23:31.486075','9','Colegiatura Febrero 2026 - Primaria',1,'[{\"added\": {}}]',18,6),
(224,'2026-01-20 17:24:37.877195','9','Colegiatura Febrero 2026 - Primaria',2,'[{\"changed\": {\"fields\": [\"Generar por Escolaridad (Nivel)\", \"Generar para Grado\"]}}]',18,6),
(225,'2026-01-20 17:25:46.639200','200','220569 - Luis Garcia - Colegiatura Febrero 2026 - Primaria ($125.0000)',1,'[{\"added\": {}}]',17,6),
(226,'2026-01-20 17:28:02.299315','220569','220569 - Luis Garcia',2,'[{\"added\": {\"name\": \"Beca-Estudiante\", \"object\": \"220569 - Luis Garcia - Beca 10% (Activa)\"}}]',9,6),
(227,'2026-01-20 17:28:33.461071','201','220569 - Luis Garcia - Colegiatura Febrero 2026 - Primaria ($75.0000)',1,'[{\"added\": {}}]',17,6),
(228,'2026-01-20 17:30:29.091347','68','Pago $125.00 - 2026-01-20',1,'[{\"added\": {}}]',19,6),
(229,'2026-01-20 17:39:22.142831','69','Pago $75.00 - 2026-01-20',1,'[{\"added\": {}}]',19,6),
(230,'2026-01-20 17:42:24.980038','2','Inscripción - Primaria',2,'[{\"changed\": {\"fields\": [\"Generar por Escolaridad (Nivel)\"]}}]',18,6),
(231,'2026-01-20 17:43:03.081445','2','Inscripción - Primaria',2,'[{\"changed\": {\"fields\": [\"Generar para Grado\", \"Generar para Grupo\"]}}]',18,6),
(232,'2026-01-20 17:46:55.236150','2','Inscripción - Primaria',2,'[{\"changed\": {\"fields\": [\"Generar para Grado\"]}}]',18,6),
(233,'2026-01-20 17:47:21.293101','9','Colegiatura Febrero 2026 - Primaria',2,'[{\"changed\": {\"fields\": [\"Generar para Grupo\"]}}]',18,6),
(234,'2026-01-20 17:48:08.630965','2','Inscripción - Primaria',2,'[{\"changed\": {\"fields\": [\"Generar para Grado\"]}}]',18,6),
(235,'2026-01-20 17:50:26.363785','2','Inscripción - Primaria',2,'[{\"changed\": {\"fields\": [\"Generar por Escolaridad (Nivel)\"]}}]',18,6),
(236,'2026-01-20 17:50:56.270623','8','Colegiatura Enero 2026 - Secundaria',2,'[{\"changed\": {\"fields\": [\"Generar para Grado\"]}}]',18,6),
(237,'2026-01-20 17:51:45.550247','10','Colegiatura Marzo - Todos',1,'[{\"added\": {}}]',18,6),
(238,'2026-01-20 18:01:25.605826','2','Inscripción - Primaria',2,'[{\"changed\": {\"fields\": [\"Generar para Grado\"]}}]',18,6),
(239,'2026-01-20 19:08:42.361696','69','Pago $75.00 - 2026-01-20',3,'',19,6),
(240,'2026-01-20 19:08:42.361749','68','Pago $125.00 - 2026-01-20',3,'',19,6),
(241,'2026-01-20 19:08:42.361774','67','Pago $400.00 - 2026-01-20',3,'',19,6),
(242,'2026-01-20 19:08:42.361796','66','Pago $500.00 - 2026-01-19',3,'',19,6),
(243,'2026-01-20 19:08:55.643450','262','220606 - Maria Garcia - Inscripción - Primaria ($800.00)',3,'',17,6),
(244,'2026-01-20 19:08:55.643505','261','220605 - Lucia Lopez - Inscripción - Primaria ($900.00)',3,'',17,6),
(245,'2026-01-20 19:08:55.643532','260','220603 - Pedro Hernandez - Inscripción - Primaria ($800.00)',3,'',17,6),
(246,'2026-01-20 19:08:55.643556','259','220602 - Sofia Perez - Inscripción - Primaria ($250.00)',3,'',17,6),
(247,'2026-01-20 19:08:55.643578','258','220599 - Carlos Martinez - Inscripción - Primaria ($800.00)',3,'',17,6),
(248,'2026-01-20 19:08:55.643600','257','220598 - Maria Sanchez - Inscripción - Primaria ($250.00)',3,'',17,6),
(249,'2026-01-20 19:08:55.643622','256','220596 - Elena Martinez - Inscripción - Primaria ($800.00)',3,'',17,6),
(250,'2026-01-20 19:08:55.643645','255','220595 - Miguel Perez - Inscripción - Primaria ($250.00)',3,'',17,6),
(251,'2026-01-20 19:08:55.643667','254','220594 - Miguel Gonzalez - Inscripción - Primaria ($800.00)',3,'',17,6),
(252,'2026-01-20 19:08:55.643703','253','220593 - Lucia Sanchez - Inscripción - Primaria ($250.00)',3,'',17,6),
(253,'2026-01-20 19:08:55.643725','252','220592 - Carlos Perez - Inscripción - Primaria ($500.00)',3,'',17,6),
(254,'2026-01-20 19:08:55.643747','251','220591 - Elena Martinez - Inscripción - Primaria ($500.00)',3,'',17,6),
(255,'2026-01-20 19:08:55.643769','250','220590 - Sofia Lopez - Inscripción - Primaria ($900.00)',3,'',17,6),
(256,'2026-01-20 19:08:55.643789','249','220589 - Pedro Hernandez - Inscripción - Primaria ($750.00)',3,'',17,6),
(257,'2026-01-20 19:08:55.643809','248','220585 - Ana Perez - Inscripción - Primaria ($800.00)',3,'',17,6),
(258,'2026-01-20 19:08:55.643830','247','220583 - Carlos Hernandez - Inscripción - Primaria ($500.00)',3,'',17,6),
(259,'2026-01-20 19:08:55.643851','246','220582 - Elena Rodriguez - Inscripción - Primaria ($250.00)',3,'',17,6),
(260,'2026-01-20 19:08:55.643891','245','220580 - Jorge Lopez - Inscripción - Primaria ($500.00)',3,'',17,6),
(261,'2026-01-20 19:08:55.643914','244','220578 - Luis Martinez - Inscripción - Primaria ($800.00)',3,'',17,6),
(262,'2026-01-20 19:08:55.643935','243','220576 - Jorge Perez - Inscripción - Primaria ($750.00)',3,'',17,6),
(263,'2026-01-20 19:08:55.643955','242','220573 - Miguel Martinez - Inscripción - Primaria ($500.00)',3,'',17,6),
(264,'2026-01-20 19:08:55.643975','241','220572 - Lucia Perez - Inscripción - Primaria ($750.00)',3,'',17,6),
(265,'2026-01-20 19:08:55.643997','240','220571 - Lucia Perez - Inscripción - Primaria ($250.00)',3,'',17,6),
(266,'2026-01-20 19:08:55.644018','239','220568 - Carlos Sanchez - Inscripción - Primaria ($750.00)',3,'',17,6),
(267,'2026-01-20 19:08:55.644039','238','220566 - Luis Gonzalez - Inscripción - Primaria ($800.00)',3,'',17,6),
(268,'2026-01-20 19:08:55.644059','237','220559 - Carlos Gonzalez - Inscripción - Primaria ($900.00)',3,'',17,6),
(269,'2026-01-20 19:08:55.644079','236','220558 - Jorge Rodriguez - Inscripción - Primaria ($800.00)',3,'',17,6),
(270,'2026-01-20 19:08:55.644099','235','220557 - Carlos Gonzalez - Inscripción - Primaria ($800.00)',3,'',17,6),
(271,'2026-01-20 19:08:55.644119','234','220554 - Miguel Martinez - Inscripción - Primaria ($500.00)',3,'',17,6),
(272,'2026-01-20 19:08:55.644140','233','220553 - Sofia Sanchez - Inscripción - Primaria ($900.00)',3,'',17,6),
(273,'2026-01-20 19:08:55.644160','232','220609 - Luis Martinez - Inscripción - Primaria ($500.00)',3,'',17,6),
(274,'2026-01-20 19:08:55.644180','231','220608 - Lucia Sanchez - Inscripción - Primaria ($750.00)',3,'',17,6),
(275,'2026-01-20 19:08:55.644200','230','220607 - Jorge Sanchez - Inscripción - Primaria ($900.00)',3,'',17,6),
(276,'2026-01-20 19:08:55.644222','229','220604 - Miguel Hernandez - Inscripción - Primaria ($900.00)',3,'',17,6),
(277,'2026-01-20 19:08:55.644242','228','220601 - Maria Hernandez - Inscripción - Primaria ($500.00)',3,'',17,6),
(278,'2026-01-20 19:08:55.644264','227','220600 - Elena Perez - Inscripción - Primaria ($750.00)',3,'',17,6),
(279,'2026-01-20 19:08:55.644284','226','220597 - Jorge Gonzalez - Inscripción - Primaria ($250.00)',3,'',17,6),
(280,'2026-01-20 19:08:55.644304','225','220588 - Maria Perez - Inscripción - Primaria ($800.00)',3,'',17,6),
(281,'2026-01-20 19:08:55.644323','224','220587 - Lucia Gonzalez - Inscripción - Primaria ($500.00)',3,'',17,6),
(282,'2026-01-20 19:08:55.644344','223','220586 - Sofia Sanchez - Inscripción - Primaria ($750.00)',3,'',17,6),
(283,'2026-01-20 19:08:55.644365','222','220584 - Jorge Rodriguez - Inscripción - Primaria ($500.00)',3,'',17,6),
(284,'2026-01-20 19:08:55.644386','221','220581 - Luis Hernandez - Inscripción - Primaria ($750.00)',3,'',17,6),
(285,'2026-01-20 19:08:55.644407','220','220579 - Ana Rodriguez - Inscripción - Primaria ($800.00)',3,'',17,6),
(286,'2026-01-20 19:08:55.644429','219','220577 - Luis Sanchez - Inscripción - Primaria ($900.00)',3,'',17,6),
(287,'2026-01-20 19:08:55.644450','218','220575 - Maria Gonzalez - Inscripción - Primaria ($900.00)',3,'',17,6),
(288,'2026-01-20 19:08:55.644471','217','220574 - Pedro Perez - Inscripción - Primaria ($750.00)',3,'',17,6),
(289,'2026-01-20 19:08:55.644492','216','220570 - Pedro Lopez - Inscripción - Primaria ($500.00)',3,'',17,6),
(290,'2026-01-20 19:08:55.644513','215','220569 - Luis Garcia - Inscripción - Primaria ($150.00)',3,'',17,6),
(291,'2026-01-20 19:08:55.644534','214','220567 - Lucia Perez - Inscripción - Primaria ($250.00)',3,'',17,6),
(292,'2026-01-20 19:08:55.644565','213','220565 - Carlos Gonzalez - Inscripción - Primaria ($500.00)',3,'',17,6),
(293,'2026-01-20 19:08:55.644587','212','220564 - Lucia Lopez - Inscripción - Primaria ($250.00)',3,'',17,6),
(294,'2026-01-20 19:08:55.644607','211','220563 - Maria Sanchez - Inscripción - Primaria ($900.00)',3,'',17,6),
(295,'2026-01-20 19:08:55.644630','210','220562 - Maria Gonzalez - Inscripción - Primaria ($800.00)',3,'',17,6),
(296,'2026-01-20 19:08:55.644652','209','220561 - Luis Garcia - Inscripción - Primaria ($900.00)',3,'',17,6),
(297,'2026-01-20 19:08:55.644672','208','220560 - Pedro Gonzalez - Inscripción - Primaria ($250.00)',3,'',17,6),
(298,'2026-01-20 19:08:55.644693','207','220556 - Sofia Hernandez - Inscripción - Primaria ($500.00)',3,'',17,6),
(299,'2026-01-20 19:08:55.644715','206','220555 - Carlos Garcia - Inscripción - Primaria ($750.00)',3,'',17,6),
(300,'2026-01-20 19:08:55.644736','205','220552 - Jorge Rodriguez - Inscripción - Primaria ($500.00)',3,'',17,6),
(301,'2026-01-20 19:08:55.644756','204','220551 - Maria Rodriguez - Inscripción - Primaria ($750.00)',3,'',17,6),
(302,'2026-01-20 19:08:55.644776','203','220550 - Maria Hernandez - Inscripción - Primaria ($900.00)',3,'',17,6),
(303,'2026-01-20 19:08:55.644796','202','220548 - MARIANA FLOWERS - Inscripción - Primaria ($800.00)',3,'',17,6),
(304,'2026-01-20 19:08:55.644815','201','220569 - Luis Garcia - Colegiatura Febrero 2026 - Primaria ($75.00)',3,'',17,6),
(305,'2026-01-20 19:08:55.644837','200','220569 - Luis Garcia - Colegiatura Febrero 2026 - Primaria ($125.00)',3,'',17,6),
(306,'2026-01-20 19:08:55.644856','199','220548 - MARIANA FLOWERS - Colegiatura Enero 2026 - Secundaria ($400.00)',3,'',17,6),
(307,'2026-01-20 19:08:55.644889','198','220548 - MARIANA FLOWERS - Colegiatura Enero 2026 - Secundaria ($350.00)',3,'',17,6),
(308,'2026-01-20 19:11:45.225901','8','Colegiatura Enero 2026 - Secundaria',2,'[{\"changed\": {\"fields\": [\"Generar para Grupo\"]}}]',18,6),
(309,'2026-01-20 19:12:08.887284','70','Pago $250.00 - 2026-01-20',1,'[{\"added\": {}}]',19,6),
(310,'2026-01-20 22:27:20.010689','2','BAJA',2,'[{\"changed\": {\"fields\": [\"Nombre\"]}}]',7,6),
(311,'2026-01-20 22:27:28.710074','1','ACTIVO',2,'[{\"changed\": {\"fields\": [\"Nombre\"]}}]',7,6),
(312,'2026-01-20 23:25:52.167196','299','729293 - GEN ONE - C2_1768951485 - TEST ($1000.00)',3,'',17,6),
(313,'2026-01-20 23:25:52.167286','298','716821 - GEN ONE - C2_1768951264 - TEST ($1000.00)',3,'',17,6),
(314,'2026-01-20 23:25:52.167334','297','829740 - TEST PRO - C_1768950793 - TEST_NIVEL ($650.00)',3,'',17,6),
(315,'2026-01-20 23:25:52.167374','296','828974 - TEST PRO - C_1768950617 - TEST_NIVEL ($650.00)',3,'',17,6),
(316,'2026-01-20 23:25:52.167412','295','923666 - TEST_PRO SMOKE - TEST_CONCEPTO_1768950179 - Universidad ($700.00)',3,'',17,6),
(317,'2026-01-20 23:25:52.167448','294','906028 - TEST_PRO SMOKE - TEST_CONCEPTO_1768950113 - Universidad ($700.00)',3,'',17,6),
(318,'2026-01-20 23:25:52.167484','293','220609 - Luis Martinez - Colegiatura Enero 2026 - Secundaria ($250.00)',3,'',17,6),
(319,'2026-01-20 23:25:52.167519','292','220608 - Lucia Sanchez - Colegiatura Enero 2026 - Secundaria ($375.00)',3,'',17,6),
(320,'2026-01-20 23:25:52.167553','291','220607 - Jorge Sanchez - Colegiatura Enero 2026 - Secundaria ($450.00)',3,'',17,6),
(321,'2026-01-20 23:25:52.167589','290','220604 - Miguel Hernandez - Colegiatura Enero 2026 - Secundaria ($450.00)',3,'',17,6),
(322,'2026-01-20 23:25:52.167625','289','220601 - Maria Hernandez - Colegiatura Enero 2026 - Secundaria ($250.00)',3,'',17,6),
(323,'2026-01-20 23:25:52.167662','288','220600 - Elena Perez - Colegiatura Enero 2026 - Secundaria ($375.00)',3,'',17,6),
(324,'2026-01-20 23:25:52.167698','287','220597 - Jorge Gonzalez - Colegiatura Enero 2026 - Secundaria ($125.00)',3,'',17,6),
(325,'2026-01-20 23:25:52.167733','286','220588 - Maria Perez - Colegiatura Enero 2026 - Secundaria ($400.00)',3,'',17,6),
(326,'2026-01-20 23:25:52.167769','285','220587 - Lucia Gonzalez - Colegiatura Enero 2026 - Secundaria ($250.00)',3,'',17,6),
(327,'2026-01-20 23:25:52.167804','284','220586 - Sofia Sanchez - Colegiatura Enero 2026 - Secundaria ($375.00)',3,'',17,6),
(328,'2026-01-20 23:25:52.167839','283','220584 - Jorge Rodriguez - Colegiatura Enero 2026 - Secundaria ($250.00)',3,'',17,6),
(329,'2026-01-20 23:25:52.167874','282','220581 - Luis Hernandez - Colegiatura Enero 2026 - Secundaria ($375.00)',3,'',17,6),
(330,'2026-01-20 23:25:52.167909','281','220579 - Ana Rodriguez - Colegiatura Enero 2026 - Secundaria ($400.00)',3,'',17,6),
(331,'2026-01-20 23:25:52.167944','280','220577 - Luis Sanchez - Colegiatura Enero 2026 - Secundaria ($450.00)',3,'',17,6),
(332,'2026-01-20 23:25:52.167978','279','220575 - Maria Gonzalez - Colegiatura Enero 2026 - Secundaria ($450.00)',3,'',17,6),
(333,'2026-01-20 23:25:52.168012','278','220574 - Pedro Perez - Colegiatura Enero 2026 - Secundaria ($375.00)',3,'',17,6),
(334,'2026-01-20 23:25:52.168071','277','220570 - Pedro Lopez - Colegiatura Enero 2026 - Secundaria ($250.00)',3,'',17,6),
(335,'2026-01-20 23:25:52.168106','276','220569 - Luis Garcia - Colegiatura Enero 2026 - Secundaria ($75.00)',3,'',17,6),
(336,'2026-01-20 23:25:52.168140','275','220567 - Lucia Perez - Colegiatura Enero 2026 - Secundaria ($125.00)',3,'',17,6),
(337,'2026-01-20 23:25:52.168175','274','220565 - Carlos Gonzalez - Colegiatura Enero 2026 - Secundaria ($250.00)',3,'',17,6),
(338,'2026-01-20 23:25:52.168209','273','220564 - Lucia Lopez - Colegiatura Enero 2026 - Secundaria ($125.00)',3,'',17,6),
(339,'2026-01-20 23:25:52.168242','272','220563 - Maria Sanchez - Colegiatura Enero 2026 - Secundaria ($450.00)',3,'',17,6),
(340,'2026-01-20 23:25:52.168277','271','220562 - Maria Gonzalez - Colegiatura Enero 2026 - Secundaria ($400.00)',3,'',17,6),
(341,'2026-01-20 23:25:52.168311','270','220561 - Luis Garcia - Colegiatura Enero 2026 - Secundaria ($450.00)',3,'',17,6),
(342,'2026-01-20 23:25:52.168343','269','220560 - Pedro Gonzalez - Colegiatura Enero 2026 - Secundaria ($125.00)',3,'',17,6),
(343,'2026-01-20 23:25:52.168377','268','220556 - Sofia Hernandez - Colegiatura Enero 2026 - Secundaria ($250.00)',3,'',17,6),
(344,'2026-01-20 23:25:52.168410','267','220555 - Carlos Garcia - Colegiatura Enero 2026 - Secundaria ($375.00)',3,'',17,6),
(345,'2026-01-20 23:25:52.168443','266','220552 - Jorge Rodriguez - Colegiatura Enero 2026 - Secundaria ($250.00)',3,'',17,6),
(346,'2026-01-20 23:25:52.168476','265','220551 - Maria Rodriguez - Colegiatura Enero 2026 - Secundaria ($375.00)',3,'',17,6),
(347,'2026-01-20 23:25:52.168510','264','220550 - Maria Hernandez - Colegiatura Enero 2026 - Secundaria ($450.00)',3,'',17,6),
(348,'2026-01-20 23:25:52.168545','263','220548 - MARIANA FLOWERS - Colegiatura Enero 2026 - Secundaria ($400.00)',3,'',17,6),
(349,'2026-01-20 23:26:16.576067','18','C2_1768951485 - TEST',3,'',18,6),
(350,'2026-01-20 23:26:16.576168','16','C2_1768951264 - TEST',3,'',18,6),
(351,'2026-01-20 23:26:16.576219','14','C_1768950793 - TEST_NIVEL',3,'',18,6),
(352,'2026-01-20 23:26:16.576261','13','C_1768950617 - TEST_NIVEL',3,'',18,6),
(353,'2026-01-20 23:26:16.576307','12','TEST_CONCEPTO_1768950179 - Universidad',3,'',18,6),
(354,'2026-01-20 23:26:16.576351','11','TEST_CONCEPTO_1768950113 - Universidad',3,'',18,6),
(355,'2026-01-21 22:49:56.577583','2000','AdmissionUser object (2000)',1,'[{\"added\": {}}]',28,6),
(356,'2026-01-21 22:50:39.750611','1','ROQUE SALAZ ARTURO PADILLA',1,'[{\"added\": {}}]',26,6),
(357,'2026-01-21 22:56:33.615866','2','2000 - NAZARIO RAMIREZ RONALDO',1,'[{\"added\": {}}, {\"added\": {\"name\": \"Tutor\", \"object\": \"2000 - NAZARIO RAMIREZ RONALDO -> ROQUE SALAZ ARTURO PADILLA (Padre)\"}}]',29,6),
(358,'2026-01-22 17:19:55.877428','20','C2_1768951581 - TEST',3,'',18,6),
(359,'2026-01-22 17:20:08.755940','10','Colegiatura Marzo - Todos',3,'',18,6),
(360,'2026-01-22 17:20:08.756033','9','Colegiatura Febrero 2026 - Primaria',3,'',18,6),
(361,'2026-01-22 17:20:08.756090','8','Colegiatura Enero 2026 - Secundaria',3,'',18,6),
(362,'2026-01-22 17:20:08.756143','2','Inscripción - Primaria',3,'',18,6),
(363,'2026-01-26 19:32:23.402213','6','AdmissionTutorAspirante object (6)',2,'[{\"changed\": {\"fields\": [\"Aspirante\"]}}]',27,6),
(364,'2026-01-27 04:09:28.117850','32','2030 - ADMISSION FULL_TEST',3,'',29,6),
(365,'2026-01-27 04:09:28.117930','31','2029 - ADMISSION FULL_TEST',3,'',29,6),
(366,'2026-01-27 04:09:28.117972','30','2028 - ADMISSION FULL_TEST',3,'',29,6),
(367,'2026-01-27 04:09:28.118008','29','2027 - ADMISSION FULL_TEST',3,'',29,6),
(368,'2026-01-27 04:09:28.118044','28','2026 - ADMISSION FULL_TEST',3,'',29,6),
(369,'2026-01-27 04:09:28.118081','27','2025 - ADMISSION FULL_TEST',3,'',29,6),
(370,'2026-01-27 04:09:28.118115','26','2024 - ADMISSION FULL_TEST',3,'',29,6),
(371,'2026-01-27 04:09:28.118148','25','2023 - ADMISSION FULL_TEST',3,'',29,6),
(372,'2026-01-27 04:09:28.118182','24','2022 - ADMISSION FULL_TEST',3,'',29,6),
(373,'2026-01-27 04:09:28.118215','23','2021 - ADMISSION FULL_TEST',3,'',29,6),
(374,'2026-01-27 04:09:28.118247','22','2020 - ADMISSION FULL_TEST',3,'',29,6),
(375,'2026-01-27 04:09:28.118279','21','2019 - ADMISSION FULL_TEST',3,'',29,6),
(376,'2026-01-27 04:09:28.118310','20','2018 - ADMISSION FULL_TEST',3,'',29,6),
(377,'2026-01-27 04:09:28.118342','19','2017 - ADMISSION FULL_TEST',3,'',29,6),
(378,'2026-01-27 04:09:28.118374','18','2016 - ADMISSION FULL_TEST',3,'',29,6),
(379,'2026-01-27 04:09:28.118405','17','2015 - ADMISSION FULL_TEST',3,'',29,6),
(380,'2026-01-27 04:09:28.118436','16','2014 - ADMISSION FULL_TEST',3,'',29,6),
(381,'2026-01-27 04:09:28.118468','15','2013 - TEST VERIFY',3,'',29,6),
(382,'2026-01-27 04:09:28.118500','14','2012 - TEST VERIFY',3,'',29,6),
(383,'2026-01-27 04:09:28.118530','13','2011 - TEST VERIFY',3,'',29,6),
(384,'2026-01-27 04:09:28.118562','12','2010 - PEREZ JUAN',3,'',29,6),
(385,'2026-01-27 04:09:28.118595','11','2009 - MARIA Test',3,'',29,6),
(386,'2026-01-27 04:09:28.118627','10','2008 - Prueba Niño',3,'',29,6),
(387,'2026-01-27 04:09:28.118659','9','2007 - Prueba Niño',3,'',29,6),
(388,'2026-01-27 04:09:38.761017','20','TUPAT None TUTOR_TEST',3,'',26,6),
(389,'2026-01-27 04:09:38.761094','19','TUPAT None TUTOR_TEST',3,'',26,6),
(390,'2026-01-27 04:09:38.761141','18','TUPAT None TUTOR_TEST',3,'',26,6),
(391,'2026-01-27 04:09:38.761182','17','TUPAT None TUTOR_TEST',3,'',26,6),
(392,'2026-01-27 04:09:38.761222','16','TUPAT None TUTOR_TEST',3,'',26,6),
(393,'2026-01-27 04:09:38.761263','15','TUPAT None TUTOR_TEST',3,'',26,6),
(394,'2026-01-27 04:09:38.761304','14','TUPAT None TUTOR_TEST',3,'',26,6),
(395,'2026-01-27 04:09:38.761344','13','TUPAT None TUTOR_TEST',3,'',26,6),
(396,'2026-01-27 04:09:38.761384','12','TUPAT None TUTOR_TEST',3,'',26,6),
(397,'2026-01-27 04:09:38.761422','11','TUPAT None TUTOR_TEST',3,'',26,6),
(398,'2026-01-27 04:09:38.761460','10','TUPAT None TUTOR_TEST',3,'',26,6),
(399,'2026-01-27 04:09:38.761498','9','TUPAT None TUTOR_TEST',3,'',26,6),
(400,'2026-01-27 04:09:38.761535','8','TUPAT None TUTOR_TEST',3,'',26,6),
(401,'2026-01-27 04:09:38.761573','7','TUPAT None TUTOR_TEST',3,'',26,6),
(402,'2026-01-27 04:09:38.761611','6','TUPAT None TUTOR_TEST',3,'',26,6),
(403,'2026-01-27 04:09:38.761650','5','Prueba None Padre',3,'',26,6),
(404,'2026-01-27 04:09:38.761689','4','Prueba None Padre',3,'',26,6),
(405,'2026-01-27 04:09:38.761727','3','Paterno None Tutor1',3,'',26,6),
(406,'2026-01-27 04:09:38.761764','2','Paterno None Tutor1',3,'',26,6),
(407,'2026-01-27 04:09:38.761802','1','ROQUE SALAZ ARTURO PADILLA',3,'',26,6),
(408,'2026-01-27 04:10:17.608861','33','2031 - ADMISSION FULL_TEST',2,'[{\"changed\": {\"fields\": [\"Status\", \"Pagado status\", \"Fecha nacimiento\", \"Sexo\"]}}]',29,6),
(409,'2026-01-27 16:52:02.908232','2031','Folio 2031 - adancito_test1040@aspirante.com',3,'',28,6),
(410,'2026-01-27 16:52:02.908315','2030','Folio 2030 - adancito_test7221@aspirante.com',3,'',28,6),
(411,'2026-01-27 16:52:02.908354','2029','Folio 2029 - adancito_test7960@aspirante.com',3,'',28,6),
(412,'2026-01-27 16:52:02.908387','2028','Folio 2028 - adancito_test7818@aspirante.com',3,'',28,6),
(413,'2026-01-27 16:52:02.908421','2027','Folio 2027 - test_full_8723@aspirante.com',3,'',28,6),
(414,'2026-01-27 16:52:02.908453','2026','Folio 2026 - test_full_7665@aspirante.com',3,'',28,6),
(415,'2026-01-27 16:52:02.908484','2025','Folio 2025 - test_full_8420@aspirante.com',3,'',28,6),
(416,'2026-01-27 16:52:02.908514','2024','Folio 2024 - test_full_7662@aspirante.com',3,'',28,6),
(417,'2026-01-27 16:52:02.908544','2023','Folio 2023 - test_full_6738@aspirante.com',3,'',28,6),
(418,'2026-01-27 16:52:02.908572','2022','Folio 2022 - test_full_5373@aspirante.com',3,'',28,6),
(419,'2026-01-27 16:52:02.908602','2021','Folio 2021 - test_full_5176@aspirante.com',3,'',28,6),
(420,'2026-01-27 16:52:02.908632','2020','Folio 2020 - test_full_7318@aspirante.com',3,'',28,6),
(421,'2026-01-27 16:52:02.908662','2019','Folio 2019 - test_full_7907@aspirante.com',3,'',28,6),
(422,'2026-01-27 16:52:02.908692','2018','Folio 2018 - test_full_1928@aspirante.com',3,'',28,6),
(423,'2026-01-27 16:52:02.908720','2017','Folio 2017 - test_full_6635@aspirante.com',3,'',28,6),
(424,'2026-01-27 16:52:02.908769','2016','Folio 2016 - test_full_4771@aspirante.com',3,'',28,6),
(425,'2026-01-27 16:52:02.908798','2015','Folio 2015 - test_full_4413@aspirante.com',3,'',28,6),
(426,'2026-01-27 16:52:02.908828','2014','Folio 2014 - test_full_0878@aspirante.com',3,'',28,6),
(427,'2026-01-27 16:52:02.908857','2013','Folio 2013 - test_verify_949@aspirante.com',3,'',28,6),
(428,'2026-01-27 16:52:02.908886','2012','Folio 2012 - test_verify_226@aspirante.com',3,'',28,6),
(429,'2026-01-27 16:52:02.908915','2011','Folio 2011 - test_verify_584@aspirante.com',3,'',28,6),
(430,'2026-01-27 16:52:02.908944','2010','Folio 2010 - aspirante@ejemplo.com',3,'',28,6),
(431,'2026-01-27 16:52:02.908973','2009','Folio 2009 - testpass@aspirante.com',3,'',28,6),
(432,'2026-01-27 16:52:02.909003','2008','Folio 2008 - revamp_test_1324@example.com',3,'',28,6),
(433,'2026-01-27 16:52:02.909031','2007','Folio 2007 - revamp_test_6219@example.com',3,'',28,6),
(434,'2026-01-27 16:52:02.909061','2006','Folio 2006 - full_test_10075@example.com',3,'',28,6),
(435,'2026-01-27 16:52:02.909091','2005','Folio 2005 - full_test_1350@example.com',3,'',28,6),
(436,'2026-01-27 16:52:02.909120','2004','Folio 2004 - full_test_6171@example.com',3,'',28,6),
(437,'2026-01-27 16:52:02.909147','2003','Folio 2003 - test_asp_3436@example.com',3,'',28,6),
(438,'2026-01-27 16:52:02.909176','2002','Folio 2002 - test_asp_8524@example.com',3,'',28,6),
(439,'2026-01-27 16:52:02.909205','2001','Folio 2001 - test_asp_9400@example.com',3,'',28,6),
(440,'2026-01-27 16:52:02.909232','2000','Folio 2000 - prueba@prueba.com',3,'',28,6),
(441,'2026-01-27 19:10:57.744655','22','Colegiatura Enero 2026 - Primaria',1,'[{\"added\": {}}]',18,6),
(442,'2026-01-27 19:11:18.761363','301','220330 - MAURICER PANDILLA - Colegiatura Test - Todos ($1000.00)',2,'[]',17,6),
(443,'2026-01-27 19:11:42.181737','302','220569 - Luis Garcia - Colegiatura Enero 2026 - Primaria ($75.0000)',1,'[{\"added\": {}}]',17,6),
(444,'2026-01-27 19:23:16.027903','220569','220569 - Luis Garcia',2,'[]',9,6),
(445,'2026-01-27 19:27:25.115531','220548','220548 - MARIANA FLOWERS',3,'',9,6),
(446,'2026-01-27 19:27:25.115584','220606','220606 - Maria Garcia',3,'',9,6),
(447,'2026-01-27 19:27:25.115607','220569','220569 - Luis Garcia',3,'',9,6),
(448,'2026-01-27 19:27:25.115627','220555','220555 - Carlos Garcia',3,'',9,6),
(449,'2026-01-27 19:27:25.115647','220561','220561 - Luis Garcia',3,'',9,6),
(450,'2026-01-27 19:27:25.115667','220575','220575 - Maria Gonzalez',3,'',9,6),
(451,'2026-01-27 19:27:25.115686','220566','220566 - Luis Gonzalez',3,'',9,6),
(452,'2026-01-27 19:27:25.115707','220565','220565 - Carlos Gonzalez',3,'',9,6),
(453,'2026-01-27 19:27:25.115727','220557','220557 - Carlos Gonzalez',3,'',9,6),
(454,'2026-01-27 19:27:25.115747','220597','220597 - Jorge Gonzalez',3,'',9,6),
(455,'2026-01-27 19:27:25.115766','220562','220562 - Maria Gonzalez',3,'',9,6),
(456,'2026-01-27 19:27:25.115786','220560','220560 - Pedro Gonzalez',3,'',9,6),
(457,'2026-01-27 19:27:25.115805','220559','220559 - Carlos Gonzalez',3,'',9,6),
(458,'2026-01-27 19:27:25.115824','220594','220594 - Miguel Gonzalez',3,'',9,6),
(459,'2026-01-27 19:27:25.115843','220587','220587 - Lucia Gonzalez',3,'',9,6),
(460,'2026-01-27 19:27:25.115863','220601','220601 - Maria Hernandez',3,'',9,6),
(461,'2026-01-27 19:27:25.115882','220583','220583 - Carlos Hernandez',3,'',9,6),
(462,'2026-01-27 19:27:25.115902','220589','220589 - Pedro Hernandez',3,'',9,6),
(463,'2026-01-27 19:27:25.115921','220556','220556 - Sofia Hernandez',3,'',9,6),
(464,'2026-01-27 19:27:25.115939','220581','220581 - Luis Hernandez',3,'',9,6),
(465,'2026-01-27 19:27:25.115959','220603','220603 - Pedro Hernandez',3,'',9,6),
(466,'2026-01-27 19:27:25.115978','220604','220604 - Miguel Hernandez',3,'',9,6),
(467,'2026-01-27 19:27:25.115998','220550','220550 - Maria Hernandez',3,'',9,6),
(468,'2026-01-27 19:27:25.116017','220570','220570 - Pedro Lopez',3,'',9,6),
(469,'2026-01-27 19:27:25.116037','220605','220605 - Lucia Lopez',3,'',9,6),
(470,'2026-01-27 19:27:25.116056','220580','220580 - Jorge Lopez',3,'',9,6),
(471,'2026-01-27 19:27:25.116075','220564','220564 - Lucia Lopez',3,'',9,6),
(472,'2026-01-27 19:27:25.116096','220590','220590 - Sofia Lopez',3,'',9,6),
(473,'2026-01-27 19:27:25.116116','220591','220591 - Elena Martinez',3,'',9,6),
(474,'2026-01-27 19:27:25.116135','220578','220578 - Luis Martinez',3,'',9,6),
(475,'2026-01-27 19:27:25.116154','220599','220599 - Carlos Martinez',3,'',9,6),
(476,'2026-01-27 19:27:25.116173','220596','220596 - Elena Martinez',3,'',9,6),
(477,'2026-01-27 19:27:25.116192','220573','220573 - Miguel Martinez',3,'',9,6),
(478,'2026-01-27 19:27:25.116211','220554','220554 - Miguel Martinez',3,'',9,6),
(479,'2026-01-27 19:27:25.116231','220609','220609 - Luis Martinez',3,'',9,6),
(480,'2026-01-27 19:27:25.116249','729293','729293 - GEN ONE',3,'',9,6),
(481,'2026-01-27 19:27:25.116268','716821','716821 - GEN ONE',3,'',9,6),
(482,'2026-01-27 19:27:25.116287','716081','716081 - GEN ONE',3,'',9,6),
(483,'2026-01-27 19:27:25.116305','220330','220330 - MAURICER PANDILLA',3,'',9,6),
(484,'2026-01-27 19:27:25.116323','220585','220585 - Ana Perez',3,'',9,6),
(485,'2026-01-27 19:27:25.116343','220574','220574 - Pedro Perez',3,'',9,6),
(486,'2026-01-27 19:27:25.116363','220600','220600 - Elena Perez',3,'',9,6),
(487,'2026-01-27 19:27:25.116381','220588','220588 - Maria Perez',3,'',9,6),
(488,'2026-01-27 19:27:25.116400','220567','220567 - Lucia Perez',3,'',9,6),
(489,'2026-01-27 19:27:25.116436','220602','220602 - Sofia Perez',3,'',9,6),
(490,'2026-01-27 19:27:25.116456','220595','220595 - Miguel Perez',3,'',9,6),
(491,'2026-01-27 19:27:25.116474','220576','220576 - Jorge Perez',3,'',9,6),
(492,'2026-01-27 19:27:25.116493','220571','220571 - Lucia Perez',3,'',9,6),
(493,'2026-01-27 19:27:25.116511','220592','220592 - Carlos Perez',3,'',9,6),
(494,'2026-01-27 19:27:25.116530','220572','220572 - Lucia Perez',3,'',9,6),
(495,'2026-01-27 19:27:25.116549','830259','830259 - TEST PRO',3,'',9,6),
(496,'2026-01-27 19:27:25.116568','829740','829740 - TEST PRO',3,'',9,6),
(497,'2026-01-27 19:27:25.116586','828974','828974 - TEST PRO',3,'',9,6),
(498,'2026-01-27 19:27:25.116606','220549','220549 - Estudiante Prueba',3,'',9,6),
(499,'2026-01-27 19:27:25.116625','220551','220551 - Maria Rodriguez',3,'',9,6),
(500,'2026-01-27 19:27:25.116643','220579','220579 - Ana Rodriguez',3,'',9,6),
(501,'2026-01-27 19:27:25.116661','220558','220558 - Jorge Rodriguez',3,'',9,6),
(502,'2026-01-27 19:27:25.116678','220552','220552 - Jorge Rodriguez',3,'',9,6),
(503,'2026-01-27 19:27:25.116696','220584','220584 - Jorge Rodriguez',3,'',9,6),
(504,'2026-01-27 19:27:25.116715','220582','220582 - Elena Rodriguez',3,'',9,6),
(505,'2026-01-27 19:27:25.116733','220563','220563 - Maria Sanchez',3,'',9,6),
(506,'2026-01-27 19:27:25.116751','220607','220607 - Jorge Sanchez',3,'',9,6),
(507,'2026-01-27 19:27:25.116769','220598','220598 - Maria Sanchez',3,'',9,6),
(508,'2026-01-27 19:27:25.116787','220593','220593 - Lucia Sanchez',3,'',9,6),
(509,'2026-01-27 19:27:25.116805','220568','220568 - Carlos Sanchez',3,'',9,6),
(510,'2026-01-27 19:27:25.116824','220608','220608 - Lucia Sanchez',3,'',9,6),
(511,'2026-01-27 19:27:25.116844','220586','220586 - Sofia Sanchez',3,'',9,6),
(512,'2026-01-27 19:27:25.116862','220553','220553 - Sofia Sanchez',3,'',9,6),
(513,'2026-01-27 19:27:25.116880','220577','220577 - Luis Sanchez',3,'',9,6),
(514,'2026-01-27 19:27:25.116899','923666','923666 - TEST_PRO SMOKE',3,'',9,6),
(515,'2026-01-27 19:27:25.116917','906028','906028 - TEST_PRO SMOKE',3,'',9,6),
(516,'2026-01-27 19:27:25.116936','220991','220991 - TEST SMOKE',3,'',9,6),
(517,'2026-01-27 19:27:25.116954','220990','220990 - BANDIT ROJELIO SOLIS',3,'',9,6),
(518,'2026-01-27 19:27:39.678283','15','E_1990 (12.00%)',3,'',8,6),
(519,'2026-01-27 19:27:39.678376','14','E_1388 (12.00%)',3,'',8,6),
(520,'2026-01-27 19:27:39.678453','13','E_1257 (12.00%)',3,'',8,6),
(521,'2026-01-27 19:27:39.678506','12','DBG_1095 (10.00%)',3,'',8,6),
(522,'2026-01-27 19:27:39.678553','11','DEBUG_E (10.00%)',3,'',8,6),
(523,'2026-01-27 19:27:39.678588','10','E_1969 (12.00%)',3,'',8,6),
(524,'2026-01-27 19:27:39.678622','9','E_1016 (12.00%)',3,'',8,6),
(525,'2026-01-27 19:27:39.678655','8','E_33 (15.00%)',3,'',8,6),
(526,'2026-01-27 19:27:39.678686','7','E_9 (15.00%)',3,'',8,6),
(527,'2026-01-27 19:27:39.678719','6','E_DEBUG (15.00%)',3,'',8,6),
(528,'2026-01-27 19:27:39.678752','5','E (75.00%)',3,'',8,6),
(529,'2026-01-27 19:27:39.678785','4','D (50.00%)',3,'',8,6),
(530,'2026-01-27 19:27:39.678817','3','C (25.00%)',3,'',8,6),
(531,'2026-01-27 19:27:39.678849','2','A (10.00%)',3,'',8,6),
(532,'2026-01-27 19:27:39.678893','1','B (20.00%)',3,'',8,6),
(533,'2026-01-27 19:27:55.533697','14','G_PERM_1768951581 - TEST',3,'',12,6),
(534,'2026-01-27 19:27:55.533767','12','G_PERM_1768951485 - TEST',3,'',12,6),
(535,'2026-01-27 19:27:55.533806','10','G_PERM_1768951264 - TEST',3,'',12,6),
(536,'2026-01-27 19:27:55.533840','8','G_PERM_1768951073 - TEST',3,'',12,6),
(537,'2026-01-27 19:27:55.533877','6','G_PERM_1768951028 - TEST',3,'',12,6),
(538,'2026-01-27 19:27:55.533912','4','G_TEST_1768950793_UPD - TEST_NIVEL',3,'',12,6),
(539,'2026-01-27 19:27:55.533948','3','G_TEST_1768950617_UPD - TEST_NIVEL',3,'',12,6),
(540,'2026-01-27 19:27:55.533984','2','G_TEST_1768950505_UPD - TEST_NIVEL',3,'',12,6),
(541,'2026-01-27 19:27:55.534017','1','10 - Universidad',3,'',12,6),
(542,'2026-01-27 19:27:55.534051','15','1° Preescolar',3,'',12,6),
(543,'2026-01-27 19:27:55.534085','16','2° Preescolar',3,'',12,6),
(544,'2026-01-27 19:27:55.534118','17','3° Preescolar',3,'',12,6),
(545,'2026-01-27 19:27:55.534153','18','1° Primaria',3,'',12,6),
(546,'2026-01-27 19:27:55.534186','19','2° Primaria',3,'',12,6),
(547,'2026-01-27 19:27:55.534219','20','3° Primaria',3,'',12,6),
(548,'2026-01-27 19:27:55.534250','21','4° Primaria',3,'',12,6),
(549,'2026-01-27 19:27:55.534282','22','5° Primaria',3,'',12,6),
(550,'2026-01-27 19:27:55.534314','23','6° Primaria',3,'',12,6),
(551,'2026-01-27 19:27:55.534347','24','1° Secundaria',3,'',12,6),
(552,'2026-01-27 19:27:55.534379','25','2° Secundaria',3,'',12,6),
(553,'2026-01-27 19:27:55.534410','26','3° Secundaria',3,'',12,6),
(554,'2026-01-27 19:28:34.765315','14','TUTOR TEST MADRE',3,'',15,6),
(555,'2026-01-27 19:28:34.765387','13','TUTOR TEST MADRE',3,'',15,6),
(556,'2026-01-27 19:36:09.245866','8','ESTADO_1768950793',3,'',7,6),
(557,'2026-01-27 19:36:09.245938','7','ESTADO_1768950617',3,'',7,6),
(558,'2026-01-27 19:36:09.245975','6','ESTADO_1768950505',3,'',7,6),
(559,'2026-01-27 19:38:46.253314','27','A Preescolar',1,'[{\"added\": {}}]',12,6),
(560,'2026-01-27 19:40:59.313835','27','A Preescolar',3,'',12,6),
(561,'2026-01-27 20:12:56.787423','1000','1000 - HECTOR ADAN HURTADO',1,'[{\"added\": {}}, {\"added\": {\"name\": \"Estudiante-Tutor\", \"object\": \"1000 - HECTOR ADAN HURTADO -> PEPE EL PIYO Sanchez Pedroza (Padre)\"}}, {\"added\": {\"name\": \"Estudiante-Tutor\", \"object\": \"1000 - HECTOR ADAN HURTADO -> Maria FERNANDA Garcia Lopez (Madre)\"}}]',9,6),
(562,'2026-01-27 20:22:47.146116','1000','1000 - HECTOR ADAN HURTADO',2,'[{\"added\": {\"name\": \"Beca-Estudiante\", \"object\": \"1000 - HECTOR ADAN HURTADO - Beca 10% (Activa)\"}}]',9,6),
(563,'2026-01-27 20:23:18.958891','303','1000 - HECTOR ADAN HURTADO - Colegiatura Enero 2026 - Primaria ($450.00)',1,'[{\"added\": {}}]',17,6),
(564,'2026-01-27 20:28:01.336074','16','A (0%)',1,'[{\"added\": {}}]',8,6),
(565,'2026-01-27 20:28:59.985967','17','B (60%)',1,'[{\"added\": {}}]',8,6),
(566,'2026-01-27 20:29:52.264482','18','C (80%)',1,'[{\"added\": {}}]',8,6),
(567,'2026-01-27 20:30:13.149312','1000','1000 - HECTOR ADAN HURTADO',2,'[{\"changed\": {\"name\": \"Beca-Estudiante\", \"object\": \"1000 - HECTOR ADAN HURTADO - Beca 10% (Retirada)\", \"fields\": [\"Activa\"]}}]',9,6),
(568,'2026-01-27 20:30:59.295412','304','1000 - HECTOR ADAN HURTADO - Colegiatura Enero 2026 - Primaria ($500.00)',1,'[{\"added\": {}}]',17,6),
(569,'2026-01-27 20:32:22.560251','1000','1000 - HECTOR ADAN HURTADO',2,'[{\"changed\": {\"name\": \"Beca-Estudiante\", \"object\": \"1000 - HECTOR ADAN HURTADO - Beca 10% (Activa)\", \"fields\": [\"Activa\"]}}]',9,6),
(570,'2026-01-27 20:33:26.490464','1000','1000 - HECTOR ADAN HURTADO',2,'[{\"added\": {\"name\": \"Evaluaci\\u00f3n Socioecon\\u00f3mica\", \"object\": \"[+] Evaluaci\\u00f3n 1000 - HECTOR ADAN HURTADO - Aprobada\"}}]',9,6),
(571,'2026-01-27 20:35:33.329330','305','1000 - HECTOR ADAN HURTADO - Colegiatura Enero 2026 - Primaria ($180.00)',1,'[{\"added\": {}}]',17,6),
(572,'2026-01-27 20:47:10.189777','78','Pago $450.00 - 2026-01-27',1,'[{\"added\": {}}]',19,6),
(573,'2026-01-27 20:48:30.828686','2','2025-2026 [ACTIVO]',1,'[{\"added\": {}}]',31,6),
(574,'2026-01-27 20:50:51.059878','79','Pago $540.00 - 2026-01-27',1,'[{\"added\": {}}]',19,6),
(575,'2026-01-27 22:41:23.139591','5','BECA_TEST_1768950179 (10.00%) - Vigente',3,'',24,6),
(576,'2026-01-27 22:41:23.139652','4','BECA_TEST_1768950113 (10.00%) - Vigente',3,'',24,6),
(577,'2026-01-27 22:41:23.139724','3','BECA_TEST_1768949919 (10.00%) - Vigente',3,'',24,6),
(578,'2026-01-27 22:41:23.139753','2','BECA_TEST_1768949870 (10.00%) - Vigente',3,'',24,6),
(579,'2026-01-27 22:41:23.139780','7','B_1768950793 (20.00%) - Vigente',3,'',24,6),
(580,'2026-01-27 22:41:23.139807','6','B_1768950617 (20.00%) - Vigente',3,'',24,6),
(581,'2026-01-27 22:42:33.618481','21','TUPAT None TUTOR_TEST',3,'',26,6),
(582,'2026-01-27 22:42:58.580414','45','VerificationCode object (45)',3,'',30,6),
(583,'2026-01-27 22:42:58.580490','44','VerificationCode object (44)',3,'',30,6),
(584,'2026-01-27 22:42:58.580526','43','VerificationCode object (43)',3,'',30,6),
(585,'2026-01-27 22:42:58.580559','42','VerificationCode object (42)',3,'',30,6),
(586,'2026-01-27 22:42:58.580592','41','VerificationCode object (41)',3,'',30,6),
(587,'2026-01-27 22:42:58.580624','40','VerificationCode object (40)',3,'',30,6),
(588,'2026-01-27 22:42:58.580657','39','VerificationCode object (39)',3,'',30,6),
(589,'2026-01-27 22:42:58.580716','38','VerificationCode object (38)',3,'',30,6),
(590,'2026-01-27 22:42:58.580742','37','VerificationCode object (37)',3,'',30,6),
(591,'2026-01-27 22:42:58.580765','36','VerificationCode object (36)',3,'',30,6),
(592,'2026-01-27 22:42:58.580790','35','VerificationCode object (35)',3,'',30,6),
(593,'2026-01-27 22:42:58.580813','34','VerificationCode object (34)',3,'',30,6),
(594,'2026-01-27 22:42:58.580837','33','VerificationCode object (33)',3,'',30,6),
(595,'2026-01-27 22:42:58.580861','32','VerificationCode object (32)',3,'',30,6),
(596,'2026-01-27 22:42:58.580884','31','VerificationCode object (31)',3,'',30,6),
(597,'2026-01-27 22:42:58.580908','30','VerificationCode object (30)',3,'',30,6),
(598,'2026-01-27 22:42:58.580932','29','VerificationCode object (29)',3,'',30,6),
(599,'2026-01-27 22:42:58.580956','28','VerificationCode object (28)',3,'',30,6),
(600,'2026-01-27 22:42:58.580980','27','VerificationCode object (27)',3,'',30,6),
(601,'2026-01-27 22:42:58.581004','26','VerificationCode object (26)',3,'',30,6),
(602,'2026-01-27 22:42:58.581026','25','VerificationCode object (25)',3,'',30,6),
(603,'2026-01-27 22:42:58.581049','24','VerificationCode object (24)',3,'',30,6),
(604,'2026-01-27 22:42:58.581073','23','VerificationCode object (23)',3,'',30,6),
(605,'2026-01-27 22:42:58.581097','21','VerificationCode object (21)',3,'',30,6),
(606,'2026-01-27 22:42:58.581120','18','VerificationCode object (18)',3,'',30,6),
(607,'2026-01-27 22:42:58.581142','17','VerificationCode object (17)',3,'',30,6),
(608,'2026-01-27 22:42:58.581166','15','VerificationCode object (15)',3,'',30,6),
(609,'2026-01-27 22:42:58.581189','14','VerificationCode object (14)',3,'',30,6),
(610,'2026-01-27 22:42:58.581220','13','VerificationCode object (13)',3,'',30,6),
(611,'2026-01-27 22:42:58.581243','11','VerificationCode object (11)',3,'',30,6),
(612,'2026-01-27 22:42:58.581266','10','VerificationCode object (10)',3,'',30,6),
(613,'2026-01-27 22:42:58.581290','4','VerificationCode object (4)',3,'',30,6),
(614,'2026-01-27 22:42:58.581313','3','VerificationCode object (3)',3,'',30,6),
(615,'2026-01-27 22:42:58.581337','2','VerificationCode object (2)',3,'',30,6),
(616,'2026-01-27 22:42:58.581360','1','VerificationCode object (1)',3,'',30,6),
(617,'2026-01-27 22:50:40.973317','1001','1001 - FLORENCIO MOHAMED',1,'[{\"added\": {}}, {\"added\": {\"name\": \"Estudiante-Tutor\", \"object\": \"1001 - FLORENCIO MOHAMED -> JASSIEL NU\\u00d1EZ PEDROZA (Padre)\"}}, {\"added\": {\"name\": \"Estudiante-Tutor\", \"object\": \"1001 - FLORENCIO MOHAMED -> ROBERTA OLED JARAMILLO (Madre)\"}}]',9,6),
(618,'2026-01-27 22:51:05.281115','1001','1001 - FLORENCIO MOHAMED',2,'[{\"added\": {\"name\": \"Beca-Estudiante\", \"object\": \"1001 - FLORENCIO MOHAMED - Beca 10% (Activa)\"}}]',9,6),
(619,'2026-01-27 22:55:38.653179','1000','1000 - ARRON ADRIAN SOMALI',2,'[{\"changed\": {\"fields\": [\"Nombre\", \"Apellido paterno\", \"Apellido materno\"]}}]',9,6),
(620,'2026-01-27 22:55:55.238571','1001','1001 - FLORENCIO MOHAMED',2,'[{\"changed\": {\"name\": \"Inscripci\\u00f3n\", \"object\": \"1001 - FLORENCIO MOHAMED - 3\\u00b0A - Preescolar (activo)\", \"fields\": [\"Grupo\"]}}]',9,6),
(621,'2026-01-27 22:57:00.214234','1000','1000 - ARRON ADRIAN SOMALI',2,'[{\"changed\": {\"name\": \"Inscripci\\u00f3n\", \"object\": \"1000 - ARRON ADRIAN SOMALI - 5\\u00b0A - Primaria (completado)\", \"fields\": [\"Grupo\"]}}, {\"changed\": {\"name\": \"Inscripci\\u00f3n\", \"object\": \"1000 - ARRON ADRIAN SOMALI - 6\\u00b0C - Primaria (activo)\", \"fields\": [\"Grupo\"]}}]',9,6),
(622,'2026-01-27 23:28:22.635303','3','2026-2027 [ACTIVO]',1,'[{\"added\": {}}]',31,6),
(623,'2026-01-27 23:36:02.104070','308','1001 - FLORENCIO MOHAMED - Reinscripción Primaria Automática - Primaria ($1350.00)',3,'',17,6),
(624,'2026-01-27 23:36:02.104144','307','1000 - ARRON ADRIAN SOMALI - Reinscripción Secundaria Automática - Secundaria ($720.00)',3,'',17,6),
(625,'2026-01-27 23:36:02.104188','305','1000 - ARRON ADRIAN SOMALI - Colegiatura Enero 2026 - Primaria ($180.00)',3,'',17,6),
(626,'2026-01-27 23:36:02.104227','304','1000 - ARRON ADRIAN SOMALI - Colegiatura Enero 2026 - Primaria ($500.00)',3,'',17,6),
(627,'2026-01-27 23:36:30.006946','3','2026-2027 ',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(628,'2026-01-27 23:36:30.081427','1','2024-2025 [ACTIVO]',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(629,'2026-01-27 23:36:56.867330','75','1000 - ARRON ADRIAN SOMALI - 6°C - Primaria (pendiente_pago)',3,'',32,6),
(630,'2026-01-27 23:37:37.232547','306','1000 - ARRON ADRIAN SOMALI - Reinscripción Primaria Automática - Primaria ($540.00)',3,'',17,6),
(631,'2026-01-27 23:37:37.232593','303','1000 - ARRON ADRIAN SOMALI - Colegiatura Enero 2026 - Primaria ($450.00)',3,'',17,6),
(632,'2026-01-27 23:37:53.454478','24','Reinscripción Secundaria Automática - Secundaria',3,'',18,6),
(633,'2026-01-27 23:37:53.454552','23','Reinscripción Primaria Automática - Primaria',3,'',18,6),
(634,'2026-01-27 23:37:53.454591','22','Colegiatura Enero 2026 - Primaria',3,'',18,6),
(635,'2026-01-27 23:37:53.454624','21','Colegiatura Test - Todos',3,'',18,6),
(636,'2026-01-27 23:38:16.726897','76','1001 - FLORENCIO MOHAMED - 3°A - Preescolar (pendiente_pago)',3,'',32,6),
(637,'2026-01-27 23:38:34.094489','3','2026-2027 ',3,'',31,6),
(638,'2026-01-27 23:38:34.094532','2','2025-2026 ',3,'',31,6),
(639,'2026-01-27 23:41:02.969957','4','2025-2024 [ACTIVO]',1,'[{\"added\": {}}]',31,6),
(640,'2026-01-27 23:41:52.402792','1001','1001 - FLORENCIO MOHAMED',2,'[{\"added\": {\"name\": \"Inscripci\\u00f3n\", \"object\": \"1001 - FLORENCIO MOHAMED - 3\\u00b0A - Preescolar (activo)\"}}]',9,6),
(641,'2026-01-27 23:42:07.862795','4','2025-2024 ',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(642,'2026-01-27 23:42:07.916642','1','2024-2025 [ACTIVO]',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(643,'2026-01-27 23:42:32.680091','4','2025-2024 [ACTIVO]',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(644,'2026-01-27 23:42:32.690774','1','2024-2025 ',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(645,'2026-01-27 23:42:54.499633','4','2025-2024 ',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(646,'2026-01-27 23:42:54.574242','1','2024-2025 [ACTIVO]',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(647,'2026-01-27 23:43:48.858967','1000','1000 - ARRON ADRIAN SOMALI',2,'[{\"changed\": {\"name\": \"Inscripci\\u00f3n\", \"object\": \"1000 - ARRON ADRIAN SOMALI - 5\\u00b0A - Primaria (activo)\", \"fields\": [\"Estatus\"]}}]',9,6),
(648,'2026-01-27 23:44:14.827274','74','1000 - ARRON ADRIAN SOMALI - 5°A - Primaria (pendiente_pago)',2,'[{\"changed\": {\"fields\": [\"Estatus\"]}}]',32,6),
(649,'2026-01-27 23:44:25.062417','4','2025-2024 [ACTIVO]',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(650,'2026-01-27 23:44:25.064903','1','2024-2025 ',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(651,'2026-01-27 23:44:42.852452','80','Pago $1350.00 - 2026-01-27',1,'[{\"added\": {}}]',19,6),
(652,'2026-01-27 23:46:29.171403','309','1001 - FLORENCIO MOHAMED - Reinscripción Primaria Automática - Primaria ($1350.00)',3,'',17,6),
(653,'2026-01-27 23:46:42.471504','4','2025-2024 ',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(654,'2026-01-27 23:46:42.563472','1','2024-2025 [ACTIVO]',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(655,'2026-01-27 23:47:05.259818','78','1001 - FLORENCIO MOHAMED - 1°A - Primaria (pendiente_pago)',3,'',32,6),
(656,'2026-01-27 23:47:15.073721','4','2025-2024 ',3,'',31,6),
(657,'2026-01-27 23:47:42.927467','1001','1001 - FLORENCIO MOHAMED',2,'[{\"changed\": {\"name\": \"Inscripci\\u00f3n\", \"object\": \"1001 - FLORENCIO MOHAMED - 3\\u00b0A - Preescolar (activo)\", \"fields\": [\"Estatus\"]}}]',9,6),
(658,'2026-01-27 23:47:57.384080','1000','1000 - ARRON ADRIAN SOMALI',2,'[{\"changed\": {\"name\": \"Inscripci\\u00f3n\", \"object\": \"1000 - ARRON ADRIAN SOMALI - 5\\u00b0A - Primaria (activo)\", \"fields\": [\"Estatus\"]}}]',9,6),
(659,'2026-01-27 23:48:17.971964','1001','1001 - FLORENCIO MOHAMED',2,'[]',9,6),
(660,'2026-01-27 23:48:51.648391','5','2025-2026 [ACTIVO]',1,'[{\"added\": {}}]',31,6),
(661,'2026-01-27 23:49:39.058222','311','1000 - ARRON ADRIAN SOMALI - Reinscripción Primaria Automática - Primaria ($540.00)',3,'',17,6),
(662,'2026-01-27 23:49:39.058318','310','1001 - FLORENCIO MOHAMED - Reinscripción Primaria Automática - Primaria ($1350.00)',3,'',17,6),
(663,'2026-01-27 23:49:52.828450','25','Reinscripción Primaria Automática - Primaria',3,'',18,6),
(664,'2026-01-27 23:50:15.104282','5','2025-2026 ',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(665,'2026-01-27 23:50:15.184192','1','2024-2025 [ACTIVO]',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(666,'2026-01-27 23:50:31.585647','5','2025-2026 ',3,'',31,6),
(667,'2026-01-27 23:50:58.987677','1001','1001 - FLORENCIO MOHAMED',2,'[]',9,6),
(668,'2026-01-27 23:51:10.755125','1000','1000 - ARRON ADRIAN SOMALI',2,'[{\"changed\": {\"name\": \"Inscripci\\u00f3n\", \"object\": \"1000 - ARRON ADRIAN SOMALI - 5\\u00b0A - Primaria (activo)\", \"fields\": [\"Estatus\"]}}]',9,6),
(669,'2026-01-27 23:51:19.591869','1001','1001 - FLORENCIO MOHAMED',2,'[]',9,6);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_content_type` VALUES
(2,'admin','logentry'),
(26,'admissions','admissiontutor'),
(27,'admissions','admissiontutoraspirante'),
(28,'admissions','admissionuser'),
(29,'admissions','aspirante'),
(30,'admissions','verificationcode'),
(3,'auth','group'),
(4,'auth','permission'),
(16,'comedor','asistenciacafeteria'),
(20,'comedor','menu'),
(21,'comedor','menusemanal'),
(5,'contenttypes','contenttype'),
(24,'estudiantes','beca'),
(25,'estudiantes','becaestudiante'),
(31,'estudiantes','cicloescolar'),
(7,'estudiantes','estadoestudiante'),
(8,'estudiantes','estrato'),
(9,'estudiantes','estudiante'),
(10,'estudiantes','estudiantetutor'),
(11,'estudiantes','evaluacionsocioeconomica'),
(12,'estudiantes','grado'),
(13,'estudiantes','grupo'),
(14,'estudiantes','historialestadosestudiante'),
(32,'estudiantes','inscripcion'),
(33,'estudiantes','niveleducativo'),
(15,'estudiantes','tutor'),
(17,'pagos','adeudo'),
(18,'pagos','conceptopago'),
(22,'pagos','configuracionpago'),
(23,'pagos','dianohabil'),
(19,'pagos','pago'),
(6,'sessions','session'),
(1,'users','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2026-01-11 06:31:38.012321'),
(2,'contenttypes','0002_remove_content_type_name','2026-01-11 06:31:38.067820'),
(3,'auth','0001_initial','2026-01-11 06:31:38.244800'),
(4,'auth','0002_alter_permission_name_max_length','2026-01-11 06:31:38.275675'),
(5,'auth','0003_alter_user_email_max_length','2026-01-11 06:31:38.284648'),
(6,'auth','0004_alter_user_username_opts','2026-01-11 06:31:38.293590'),
(7,'auth','0005_alter_user_last_login_null','2026-01-11 06:31:38.302557'),
(8,'auth','0006_require_contenttypes_0002','2026-01-11 06:31:38.304716'),
(9,'auth','0007_alter_validators_add_error_messages','2026-01-11 06:31:38.312680'),
(10,'auth','0008_alter_user_username_max_length','2026-01-11 06:31:38.329190'),
(11,'auth','0009_alter_user_last_name_max_length','2026-01-11 06:31:38.338225'),
(12,'auth','0010_alter_group_name_max_length','2026-01-11 06:31:38.358387'),
(13,'auth','0011_update_proxy_permissions','2026-01-11 06:31:38.365725'),
(14,'auth','0012_alter_user_first_name_max_length','2026-01-11 06:31:38.371716'),
(15,'users','0001_initial','2026-01-11 06:31:38.573076'),
(16,'admin','0001_initial','2026-01-11 06:31:38.647859'),
(17,'admin','0002_logentry_remove_auto_add','2026-01-11 06:31:38.660216'),
(18,'admin','0003_logentry_add_action_flag_choices','2026-01-11 06:31:38.674610'),
(19,'estudiantes','0001_initial','2026-01-11 06:31:38.819226'),
(20,'comedor','0001_initial','2026-01-11 06:31:38.833860'),
(21,'comedor','0002_initial','2026-01-11 06:31:38.950261'),
(22,'estudiantes','0002_initial','2026-01-11 06:31:39.857478'),
(23,'pagos','0001_initial','2026-01-11 06:31:40.331232'),
(24,'sessions','0001_initial','2026-01-11 06:31:40.366696'),
(25,'users','0002_user_username','2026-01-11 07:17:46.103324'),
(26,'estudiantes','0003_remove_tutor_idx_tutor_ultima_actualizacion_and_more','2026-01-11 08:05:11.228459'),
(27,'users','0003_remove_user_is_staff_user_mfa_code_and_more','2026-01-12 22:46:24.219020'),
(28,'users','0004_user_is_staff_alter_user_is_superuser','2026-01-13 00:06:05.637001'),
(29,'estudiantes','0004_estudiante_updateable','2026-01-14 16:32:09.008926'),
(30,'pagos','0002_remove_adeudo_fecha_actualizacion_and_more','2026-01-14 16:51:35.256256'),
(31,'comedor','0003_menu_asistenciacafeteria_menu','2026-01-16 00:29:29.612798'),
(32,'pagos','0003_alter_adeudo_fecha_vencimiento_alter_pago_adeudo','2026-01-16 00:29:29.742615'),
(33,'pagos','0004_alter_adeudo_fecha_vencimiento_alter_pago_adeudo','2026-01-17 04:13:06.373231'),
(34,'pagos','0005_adeudo_monto_pagado_alter_adeudo_fecha_vencimiento','2026-01-17 04:14:25.644623'),
(35,'comedor','0004_menusemanal','2026-01-18 02:22:21.512618'),
(36,'estudiantes','0005_estrato_color_estrato_ingreso_maximo_and_more','2026-01-18 02:22:21.945796'),
(37,'pagos','0006_configuracionpago_dianohabil_and_more','2026-01-18 02:22:22.211118'),
(38,'estudiantes','0006_estudiante_porcentaje_beca','2026-01-19 04:09:43.296503'),
(39,'estudiantes','0007_beca_becaestudiante','2026-01-19 18:59:48.402566'),
(40,'pagos','0007_alter_adeudo_fecha_vencimiento','2026-01-19 18:59:48.422625'),
(41,'pagos','0008_alter_adeudo_fecha_vencimiento','2026-01-19 18:59:48.449041'),
(42,'admissions','0001_initial','2026-01-21 22:31:31.188669'),
(43,'admissions','0002_rename_idx_tutoradmision_nombre_completo_idx_tutoradm_nombre_completo','2026-01-21 22:31:31.209518'),
(44,'pagos','0009_alter_adeudo_fecha_vencimiento','2026-01-21 22:31:31.226630'),
(45,'pagos','0010_alter_adeudo_fecha_vencimiento','2026-01-21 22:31:31.256405'),
(46,'pagos','0011_alter_adeudo_fecha_vencimiento','2026-01-21 22:31:31.276232'),
(47,'admissions','0003_aspirante_fecha_pago_aspirante_metodo_pago_and_more','2026-01-22 17:30:39.800314'),
(48,'pagos','0012_alter_adeudo_fecha_vencimiento','2026-01-22 17:30:39.825800'),
(49,'admissions','0004_verificationcode_and_more','2026-01-22 17:56:44.249725'),
(50,'admissions','0005_alter_admissionuser_folio','2026-01-22 18:04:16.095790'),
(51,'admissions','0006_rename_genero_aspirante_sexo_and_more','2026-01-23 20:09:53.366180'),
(52,'admissions','0007_alter_admissionuser_options_admissionuser_last_login_and_more','2026-01-26 16:26:55.831425'),
(53,'admissions','0008_admissiontutor_acta_nacimiento_and_more','2026-01-27 02:05:10.043327'),
(54,'admissions','0009_alter_admissiontutor_acta_nacimiento_and_more','2026-01-27 02:07:02.800867'),
(55,'admissions','0010_admissiontutor_carta_bajo_protesta_and_more','2026-01-27 04:00:05.346631'),
(56,'estudiantes','0008_cicloescolar_inscripcion_niveleducativo_and_more','2026-01-27 16:54:05.599348'),
(57,'pagos','0013_conceptopago_tipo_concepto_and_more','2026-01-27 16:54:05.657226');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_session` VALUES
('0opmbuz29n0jft98il06t8t0hu7wx5bh','.eJxVjDsOwjAQBe_iGln-rZ1Q0nMGa9dr4wBypDipEHeHSCmgfTPzXiLitta49bzEicVZeHH63QjTI7cd8B3bbZZpbusykdwVedAurzPn5-Vw_w4q9vqtIZfCLoHRqIPTiiyz8UgjKlJoDQckp4LSNoEOACpZBsfDAOxpLCTeH-wMN-M:1vfXIo:ShoYv1l-QtWKsSdrPv1fu6JYTwqFeHDP4SWeETb_FGM','2026-01-27 05:50:50.978570'),
('dwpvx1fqoclttjn0k7ahwp144boxpr9o','.eJxVjDsOwjAQBe_iGln-rZ1Q0nMGa9dr4wBypDipEHeHSCmgfTPzXiLitta49bzEicVZeHH63QjTI7cd8B3bbZZpbusykdwVedAurzPn5-Vw_w4q9vqtIZfCLoHRqIPTiiyz8UgjKlJoDQckp4LSNoEOACpZBsfDAOxpLCTeH-wMN-M:1vkS8p:VG6Nxqk4DJ4F5CuMwa1yt7h_T0_6hV2Kip5NpTCfiDA','2026-02-09 19:20:51.879519'),
('fu7jhpatze0b6q2kesnfmq6agu62ticv','.eJxVjDsOwjAQBe_iGln-rZ1Q0nMGa9dr4wBypDipEHeHSCmgfTPzXiLitta49bzEicVZeHH63QjTI7cd8B3bbZZpbusykdwVedAurzPn5-Vw_w4q9vqtIZfCLoHRqIPTiiyz8UgjKlJoDQckp4LSNoEOACpZBsfDAOxpLCTeH-wMN-M:1vg8dI:lA6MIU3c_Ec4JWvYKciojmoiQp3QXMPDSImkbmF714A','2026-01-28 21:42:28.928797'),
('ma4zf92ag8wz6y27a8ku0n4ycf8yuhi6','.eJxVjMsOwiAQRf-FtSGFysule7-BzDCDVA0kpV0Z_92QdKHbe865bxFh30rcO69xIXERszj9bgjpyXUAekC9N5la3dYF5VDkQbu8NeLX9XD_Dgr0MmoNQSUINin03jsCnRGVYzRmziYrjZQsJRPIoIaJ2ejJzs568O6MLD5fBhs4lQ:1verBc:WrN3QPx-lk7alNXi8Aeka5qT-moC742T18lVWw3KsbY','2026-01-25 08:52:36.278559'),
('oqvo9kptxvxsiisuq13nn41wsgntft0p','.eJxVjDsOwjAQBe_iGln-rZ1Q0nMGa9dr4wBypDipEHeHSCmgfTPzXiLitta49bzEicVZeHH63QjTI7cd8B3bbZZpbusykdwVedAurzPn5-Vw_w4q9vqtIZfCLoHRqIPTiiyz8UgjKlJoDQckp4LSNoEOACpZBsfDAOxpLCTeH-wMN-M:1vhJEf:NgY9F1pXKnpyM69aUeypBCoBDZUuJdYEV8KTzf-9AB4','2026-02-01 03:13:53.559281'),
('twoh2h80gw2863j5hg5oeharge9qvgla','.eJxVjDsOwjAQRO_iGll2_Fso6TmDtV5vcADZUpxUiLuTSCmgG817M28RcV1KXDvPccriIpw4_XYJ6cl1B_mB9d4ktbrMU5K7Ig_a5a1lfl0P9--gYC_b2toBIXDShrLzW8wKWEFipQfS5NiP3ngeLQKb7AgDJSAInqxV5qzF5wvszjgI:1vfSNb:Xqjy_B7NUDIHvh7R9NXYFdxY8EnR8msf9uBEuTg96DE','2026-01-27 00:35:27.355781');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `estados_estudiante`
--

DROP TABLE IF EXISTS `estados_estudiante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `estados_estudiante` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `es_estado_activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estados_estudiante`
--

LOCK TABLES `estados_estudiante` WRITE;
/*!40000 ALTER TABLE `estados_estudiante` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `estados_estudiante` VALUES
(1,'ACTIVO','Estudiante inscrito y activo',1),
(2,'BAJA','Baja temporal',1),
(3,'BAJA TEMPORAL','Estado BAJA TEMPORAL',0),
(4,'BAJA DEFINITIVA','Estado BAJA DEFINITIVA',0),
(5,'EGRESADO','Estado EGRESADO',0);
/*!40000 ALTER TABLE `estados_estudiante` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `estratos`
--

DROP TABLE IF EXISTS `estratos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `estratos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(10) NOT NULL,
  `descripcion` longtext NOT NULL,
  `porcentaje_descuento` decimal(5,2) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `color` varchar(7) NOT NULL,
  `ingreso_maximo` decimal(10,2) DEFAULT NULL,
  `ingreso_minimo` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `idx_estrato_activo` (`activo`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estratos`
--

LOCK TABLES `estratos` WRITE;
/*!40000 ALTER TABLE `estratos` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `estratos` VALUES
(16,'A','Mesualidad $500',0.00,1,'#6B7280',8000.00,8000.00),
(17,'B','Descuento del 60%',60.00,1,'#6B7280',10394.00,50000.00),
(18,'C','Descuento del 80%',80.00,1,'#6B7280',30494.00,20394.00);
/*!40000 ALTER TABLE `estratos` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `estudiantes`
--

DROP TABLE IF EXISTS `estudiantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `estudiantes` (
  `matricula` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `apellido_paterno` varchar(255) NOT NULL,
  `apellido_materno` varchar(255) NOT NULL,
  `direccion` longtext NOT NULL,
  `usuario_id` bigint(20) NOT NULL,
  `grupo_id` bigint(20) DEFAULT NULL,
  `updateable` tinyint(1) NOT NULL,
  `alergias_alimentarias` longtext DEFAULT NULL,
  `porcentaje_beca` decimal(5,2) NOT NULL,
  PRIMARY KEY (`matricula`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  KEY `idx_estudiante_matricula` (`matricula`),
  KEY `idx_estudiante_grupo` (`grupo_id`),
  KEY `idx_estudiante_nombre_completo` (`apellido_paterno`,`apellido_materno`,`nombre`),
  CONSTRAINT `estudiantes_grupo_id_080625dd_fk_grupos_id` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`),
  CONSTRAINT `estudiantes_usuario_id_42607c6a_fk_users_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estudiantes`
--

LOCK TABLES `estudiantes` WRITE;
/*!40000 ALTER TABLE `estudiantes` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `estudiantes` VALUES
(1000,'ARRON ADRIAN','SOMALI','ALVA','YISUS MARIE',89,NULL,1,NULL,0.00),
(1001,'FLORENCIO','MOHAMED','RAMIREZ','Por El centro',90,NULL,1,NULL,0.00);
/*!40000 ALTER TABLE `estudiantes` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `estudiantes_tutores`
--

DROP TABLE IF EXISTS `estudiantes_tutores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `estudiantes_tutores` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `parentesco` varchar(100) NOT NULL,
  `fecha_asignacion` datetime(6) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `estudiante_matricula` int(11) NOT NULL,
  `tutor_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `estudiantes_tutores_estudiante_matricula_tutor_id_72e6c895_uniq` (`estudiante_matricula`,`tutor_id`),
  KEY `idx_estudiantetutor_estudiante` (`estudiante_matricula`),
  KEY `idx_estudiantetutor_tutor` (`tutor_id`),
  CONSTRAINT `estudiantes_tutores_estudiante_matricula_a3dca86b_fk_estudiant` FOREIGN KEY (`estudiante_matricula`) REFERENCES `estudiantes` (`matricula`),
  CONSTRAINT `estudiantes_tutores_tutor_id_a72f9574_fk_tutores_id` FOREIGN KEY (`tutor_id`) REFERENCES `tutores` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estudiantes_tutores`
--

LOCK TABLES `estudiantes_tutores` WRITE;
/*!40000 ALTER TABLE `estudiantes_tutores` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `estudiantes_tutores` VALUES
(10,'Padre','2026-01-27 20:12:56.785702',1,1000,2),
(11,'Madre','2026-01-27 20:12:56.786537',1,1000,1),
(12,'Padre','2026-01-27 22:50:40.972186',1,1001,4),
(13,'Madre','2026-01-27 22:50:40.972798',1,1001,3);
/*!40000 ALTER TABLE `estudiantes_tutores` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `evaluaciones_socioeconomicas`
--

DROP TABLE IF EXISTS `evaluaciones_socioeconomicas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `evaluaciones_socioeconomicas` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha_evaluacion` datetime(6) NOT NULL,
  `ingreso_mensual` decimal(10,2) NOT NULL,
  `tipo_vivienda` varchar(255) NOT NULL,
  `miembros_hogar` int(11) NOT NULL,
  `documentos_json` longtext NOT NULL,
  `aprobado` tinyint(1) DEFAULT NULL,
  `fecha_aprobacion` datetime(6) DEFAULT NULL,
  `estrato_id` bigint(20) DEFAULT NULL,
  `estudiante_matricula` int(11) NOT NULL,
  `comentarios_comision` longtext DEFAULT NULL,
  `es_reconsideracion` tinyint(1) NOT NULL,
  `estrato_sugerido_id` bigint(20) DEFAULT NULL,
  `fecha_vencimiento` date DEFAULT NULL,
  `justificacion_estrato` longtext DEFAULT NULL,
  `notificacion_enviada` tinyint(1) NOT NULL,
  `requiere_aprobacion_especial` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `evaluaciones_socioeconomicas_estrato_id_d58b0b82_fk_estratos_id` (`estrato_id`),
  KEY `idx_evalsocio_estudiante` (`estudiante_matricula`),
  KEY `idx_evalsocio_fecha` (`fecha_evaluacion`),
  KEY `idx_evalsocio_aprobado` (`aprobado`),
  KEY `evaluaciones_socioec_estrato_sugerido_id_e7b84d0e_fk_estratos_` (`estrato_sugerido_id`),
  CONSTRAINT `evaluaciones_socioec_estrato_sugerido_id_e7b84d0e_fk_estratos_` FOREIGN KEY (`estrato_sugerido_id`) REFERENCES `estratos` (`id`),
  CONSTRAINT `evaluaciones_socioec_estudiante_matricula_0ebd0a32_fk_estudiant` FOREIGN KEY (`estudiante_matricula`) REFERENCES `estudiantes` (`matricula`),
  CONSTRAINT `evaluaciones_socioeconomicas_estrato_id_d58b0b82_fk_estratos_id` FOREIGN KEY (`estrato_id`) REFERENCES `estratos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluaciones_socioeconomicas`
--

LOCK TABLES `evaluaciones_socioeconomicas` WRITE;
/*!40000 ALTER TABLE `evaluaciones_socioeconomicas` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `evaluaciones_socioeconomicas` VALUES
(69,'2026-01-27 20:33:26.489409',45876968.00,'Adobe',5,'f`ff',1,'2026-01-27 20:33:26.489484',17,1000,'Aprobado',0,17,NULL,'{}',0,0);
/*!40000 ALTER TABLE `evaluaciones_socioeconomicas` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `grados`
--

DROP TABLE IF EXISTS `grados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `grados` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `nivel` varchar(100) NOT NULL,
  `numero_grado` int(11) NOT NULL,
  `orden_global` int(11) NOT NULL,
  `nivel_educativo_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `grados_nombre_nivel_de2afc70_uniq` (`nombre`,`nivel`),
  KEY `idx_grado_nombre_nivel` (`nombre`,`nivel`),
  KEY `grados_nivel_educativo_id_cf44513c_fk_niveles_educativos_id` (`nivel_educativo_id`),
  KEY `idx_grado_orden_global` (`orden_global`),
  CONSTRAINT `grados_nivel_educativo_id_cf44513c_fk_niveles_educativos_id` FOREIGN KEY (`nivel_educativo_id`) REFERENCES `niveles_educativos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grados`
--

LOCK TABLES `grados` WRITE;
/*!40000 ALTER TABLE `grados` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `grados` VALUES
(28,'1°','Preescolar',1,1,1),
(29,'2°','Preescolar',2,2,1),
(30,'3°','Preescolar',3,3,1),
(31,'1°','Primaria',1,4,2),
(32,'2°','Primaria',2,5,2),
(33,'3°','Primaria',3,6,2),
(34,'4°','Primaria',4,7,2),
(35,'5°','Primaria',5,8,2),
(36,'6°','Primaria',6,9,2),
(37,'1°','Secundaria',1,10,3),
(38,'2°','Secundaria',2,11,3),
(39,'3°','Secundaria',3,12,3);
/*!40000 ALTER TABLE `grados` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `grupos`
--

DROP TABLE IF EXISTS `grupos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `grupos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `generacion` varchar(50) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `grado_id` bigint(20) NOT NULL,
  `capacidad_maxima` int(11) NOT NULL,
  `ciclo_escolar_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_grupo_grado` (`grado_id`),
  KEY `idx_grupo_ciclo` (`ciclo_escolar_id`),
  CONSTRAINT `grupos_ciclo_escolar_id_3fc38f0c_fk_ciclos_escolares_id` FOREIGN KEY (`ciclo_escolar_id`) REFERENCES `ciclos_escolares` (`id`),
  CONSTRAINT `grupos_grado_id_7d47e77c_fk_grados_id` FOREIGN KEY (`grado_id`) REFERENCES `grados` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=196 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupos`
--

LOCK TABLES `grupos` WRITE;
/*!40000 ALTER TABLE `grupos` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `grupos` VALUES
(16,'A','','Grupo A de 1° Preescolar','2026-01-27 19:42:35.700054',28,30,1),
(17,'B','','Grupo B de 1° Preescolar','2026-01-27 19:42:35.710693',28,30,1),
(18,'C','','Grupo C de 1° Preescolar','2026-01-27 19:42:35.714068',28,30,1),
(19,'A','','Grupo A de 2° Preescolar','2026-01-27 19:42:35.718033',29,30,1),
(20,'B','','Grupo B de 2° Preescolar','2026-01-27 19:42:35.722033',29,30,1),
(21,'C','','Grupo C de 2° Preescolar','2026-01-27 19:42:35.725374',29,30,1),
(22,'A','','Grupo A de 3° Preescolar','2026-01-27 19:42:35.729363',30,30,1),
(23,'B','','Grupo B de 3° Preescolar','2026-01-27 19:42:35.732760',30,30,1),
(24,'C','','Grupo C de 3° Preescolar','2026-01-27 19:42:35.736108',30,30,1),
(25,'A','','Grupo A de 1° Primaria','2026-01-27 19:42:35.741070',31,30,1),
(26,'B','','Grupo B de 1° Primaria','2026-01-27 19:42:35.744492',31,30,1),
(27,'C','','Grupo C de 1° Primaria','2026-01-27 19:42:35.748627',31,30,1),
(28,'A','','Grupo A de 2° Primaria','2026-01-27 19:42:35.753704',32,30,1),
(29,'B','','Grupo B de 2° Primaria','2026-01-27 19:42:35.757720',32,30,1),
(30,'C','','Grupo C de 2° Primaria','2026-01-27 19:42:35.761138',32,30,1),
(31,'A','','Grupo A de 3° Primaria','2026-01-27 19:42:35.765738',33,30,1),
(32,'B','','Grupo B de 3° Primaria','2026-01-27 19:42:35.769344',33,30,1),
(33,'C','','Grupo C de 3° Primaria','2026-01-27 19:42:35.772925',33,30,1),
(34,'A','','Grupo A de 4° Primaria','2026-01-27 19:42:35.777477',34,30,1),
(35,'B','','Grupo B de 4° Primaria','2026-01-27 19:42:35.781140',34,30,1),
(36,'C','','Grupo C de 4° Primaria','2026-01-27 19:42:35.784422',34,30,1),
(37,'A','','Grupo A de 5° Primaria','2026-01-27 19:42:35.788777',35,30,1),
(38,'B','','Grupo B de 5° Primaria','2026-01-27 19:42:35.792575',35,30,1),
(39,'C','','Grupo C de 5° Primaria','2026-01-27 19:42:35.796092',35,30,1),
(40,'A','','Grupo A de 6° Primaria','2026-01-27 19:42:35.800430',36,30,1),
(41,'B','','Grupo B de 6° Primaria','2026-01-27 19:42:35.804064',36,30,1),
(42,'C','','Grupo C de 6° Primaria','2026-01-27 19:42:35.807600',36,30,1),
(43,'A','','Grupo A de 1° Secundaria','2026-01-27 19:42:35.811951',37,30,1),
(44,'B','','Grupo B de 1° Secundaria','2026-01-27 19:42:35.815378',37,30,1),
(45,'C','','Grupo C de 1° Secundaria','2026-01-27 19:42:35.818792',37,30,1),
(46,'A','','Grupo A de 2° Secundaria','2026-01-27 19:42:35.823110',38,30,1),
(47,'B','','Grupo B de 2° Secundaria','2026-01-27 19:42:35.826324',38,30,1),
(48,'C','','Grupo C de 2° Secundaria','2026-01-27 19:42:35.829732',38,30,1),
(49,'A','','Grupo A de 3° Secundaria','2026-01-27 19:42:35.834152',39,30,1),
(50,'B','','Grupo B de 3° Secundaria','2026-01-27 19:42:35.841189',39,30,1),
(51,'C','','Grupo C de 3° Secundaria','2026-01-27 19:42:35.848474',39,30,1);
/*!40000 ALTER TABLE `grupos` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `historial_estados_estudiante`
--

DROP TABLE IF EXISTS `historial_estados_estudiante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_estados_estudiante` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `justificacion` longtext DEFAULT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `estado_id` bigint(20) NOT NULL,
  `estudiante_matricula` int(11) NOT NULL,
  `es_baja_temporal` tinyint(1) DEFAULT NULL,
  `fecha_baja` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_historialestado_estudiante` (`estudiante_matricula`),
  KEY `idx_historialestado_estado` (`estado_id`),
  CONSTRAINT `historial_estados_es_estado_id_70112f90_fk_estados_e` FOREIGN KEY (`estado_id`) REFERENCES `estados_estudiante` (`id`),
  CONSTRAINT `historial_estados_es_estudiante_matricula_32e02065_fk_estudiant` FOREIGN KEY (`estudiante_matricula`) REFERENCES `estudiantes` (`matricula`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_estados_estudiante`
--

LOCK TABLES `historial_estados_estudiante` WRITE;
/*!40000 ALTER TABLE `historial_estados_estudiante` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `historial_estados_estudiante` VALUES
(79,'Asignación inicial automática','2026-01-27 23:53:32.904835',1,1000,NULL,NULL),
(80,'Asignación inicial automática','2026-01-27 23:53:32.908251',1,1001,NULL,NULL);
/*!40000 ALTER TABLE `historial_estados_estudiante` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `inscripciones`
--

DROP TABLE IF EXISTS `inscripciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `inscripciones` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `estatus` varchar(50) NOT NULL,
  `fecha_inscripcion` datetime(6) NOT NULL,
  `fecha_baja` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  `promedio_final` decimal(4,2) DEFAULT NULL,
  `ciclo_escolar_id` bigint(20) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `grupo_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inscripciones_estudiante_id_ciclo_escolar_id_9013b0fd_uniq` (`estudiante_id`,`ciclo_escolar_id`),
  KEY `inscripciones_grupo_id_f5e700cb_fk_grupos_id` (`grupo_id`),
  KEY `idx_inscripcion_estudiante` (`estudiante_id`),
  KEY `idx_inscripcion_ciclo` (`ciclo_escolar_id`),
  KEY `idx_inscripcion_estatus` (`estatus`),
  CONSTRAINT `inscripciones_ciclo_escolar_id_fed8162f_fk_ciclos_escolares_id` FOREIGN KEY (`ciclo_escolar_id`) REFERENCES `ciclos_escolares` (`id`),
  CONSTRAINT `inscripciones_estudiante_id_64dcccda_fk_estudiantes_matricula` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiantes` (`matricula`),
  CONSTRAINT `inscripciones_grupo_id_f5e700cb_fk_grupos_id` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscripciones`
--

LOCK TABLES `inscripciones` WRITE;
/*!40000 ALTER TABLE `inscripciones` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `inscripciones` VALUES
(74,'activo','2026-01-27 20:12:56.784527',NULL,'2026-01-27 23:51:10.751628',NULL,1,1000,37),
(77,'activo','2026-01-27 23:41:52.399485',NULL,'2026-01-27 23:47:42.925020',NULL,1,1001,22);
/*!40000 ALTER TABLE `inscripciones` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `menus_semanales`
--

DROP TABLE IF EXISTS `menus_semanales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `menus_semanales` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `semana_inicio` date NOT NULL,
  `semana_fin` date NOT NULL,
  `archivo_pdf` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL,
  `fecha_subida` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menus_semanales`
--

LOCK TABLES `menus_semanales` WRITE;
/*!40000 ALTER TABLE `menus_semanales` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `menus_semanales` VALUES
(1,'2025-01-06','2025-01-10','menus/ejemplo.pdf','Menu Enero Semana 2',1,'2026-01-18 02:51:12.851975'),
(2,'2025-01-13','2025-01-17','menus/ejemplo.pdf','Menu Enero Semana 3',1,'2026-01-18 02:51:12.854657'),
(3,'2025-01-20','2025-01-24','menus/ejemplo.pdf','Menu Enero Semana 4',1,'2026-01-18 02:51:12.856706');
/*!40000 ALTER TABLE `menus_semanales` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `niveles_educativos`
--

DROP TABLE IF EXISTS `niveles_educativos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `niveles_educativos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `orden` int(11) NOT NULL,
  `grados_totales` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `niveles_educativos`
--

LOCK TABLES `niveles_educativos` WRITE;
/*!40000 ALTER TABLE `niveles_educativos` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `niveles_educativos` VALUES
(1,'Preescolar',1,3,'2026-01-27 16:54:17.279466','2026-01-27 16:54:17.279532'),
(2,'Primaria',2,6,'2026-01-27 16:54:17.284228','2026-01-27 16:54:17.284272'),
(3,'Secundaria',3,3,'2026-01-27 16:54:17.289771','2026-01-27 16:54:17.289819');
/*!40000 ALTER TABLE `niveles_educativos` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `pagos`
--

DROP TABLE IF EXISTS `pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `monto` decimal(10,2) NOT NULL,
  `fecha_pago` datetime(6) NOT NULL,
  `metodo_pago` varchar(100) NOT NULL,
  `numero_referencia` varchar(255) DEFAULT NULL,
  `ruta_recibo` longtext DEFAULT NULL,
  `recibido_por` varchar(255) DEFAULT NULL,
  `notas` longtext DEFAULT NULL,
  `adeudo_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_pago_adeudo` (`adeudo_id`),
  KEY `idx_pago_fecha` (`fecha_pago`),
  KEY `idx_pago_metodo` (`metodo_pago`),
  KEY `pagos_adeudo_id_14279390` (`adeudo_id`),
  CONSTRAINT `pagos_adeudo_id_14279390_fk_adeudos_id` FOREIGN KEY (`adeudo_id`) REFERENCES `adeudos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagos`
--

LOCK TABLES `pagos` WRITE;
/*!40000 ALTER TABLE `pagos` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `pagos` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tutor_temp`
--

DROP TABLE IF EXISTS `tutor_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tutor_temp` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido_paterno` varchar(100) DEFAULT NULL,
  `apellido_materno` varchar(100) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `numero_telefono` varchar(20) NOT NULL,
  `curp` varchar(18) DEFAULT NULL,
  `acta_nacimiento` varchar(255) DEFAULT NULL,
  `curp_pdf` varchar(255) DEFAULT NULL,
  `carta_bajo_protesta` varchar(255) DEFAULT NULL,
  `carta_ingresos` varchar(255) DEFAULT NULL,
  `comprobante_domicilio` varchar(255) DEFAULT NULL,
  `comprobante_ingresos` varchar(255) DEFAULT NULL,
  `contrato_arrendamiento_predial` varchar(255) DEFAULT NULL,
  `foto_fachada_domicilio` varchar(255) DEFAULT NULL,
  `ine_tutor` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_tutoradm_nombre_completo` (`apellido_paterno`,`apellido_materno`,`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tutor_temp`
--

LOCK TABLES `tutor_temp` WRITE;
/*!40000 ALTER TABLE `tutor_temp` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `tutor_temp` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tutores`
--

DROP TABLE IF EXISTS `tutores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tutores` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `apellido_paterno` varchar(255) NOT NULL,
  `apellido_materno` varchar(255) NOT NULL,
  `telefono` varchar(17) NOT NULL,
  `correo` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_tutor_correo` (`correo`),
  KEY `idx_tutor_telefono` (`telefono`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tutores`
--

LOCK TABLES `tutores` WRITE;
/*!40000 ALTER TABLE `tutores` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `tutores` VALUES
(1,'Maria FERNANDA','Garcia','Lopez','+52 449 888 8888','updated@ejemplo.com'),
(2,'PEPE EL PIYO','Sanchez','Pedroza','449 405 26 64','maracas@gmail.com'),
(3,'ROBERTA','OLED','JARAMILLO','449 294 34 48','roberta@test.com'),
(4,'JASSIEL','NUÑEZ','PEDROZA','34 894 73 84','ohyeah@outlook.es');
/*!40000 ALTER TABLE `tutores` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users_user`
--

DROP TABLE IF EXISTS `users_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `role` varchar(20) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) DEFAULT NULL,
  `mfa_code` varchar(6) DEFAULT NULL,
  `mfa_expires_at` datetime(6) DEFAULT NULL,
  `is_staff` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user`
--

LOCK TABLES `users_user` WRITE;
/*!40000 ALTER TABLE `users_user` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `users_user` VALUES
(1,'testpass123',NULL,'adancpphack@gmail.com','HECTOR ADAN','Estudiante',0,0,'adan',NULL,NULL,0),
(6,'pbkdf2_sha256$1200000$PYfy8QfRclfAEDompWnClV$LsWUIxjl1GT6mA+kwu9DAhVNelAA4tkgQS8h/cyh3PY=','2026-01-26 19:20:51.876247','hectorino2789@gmail.com','','Administrador',1,1,'adanov21',NULL,NULL,1),
(7,'pbkdf2_sha256$1200000$Wdq7sRvTKzdqTtMa5lNFng$72GkuIaUwJDP6N7sROw8goYf51Wo1PbvtgrzBBAj4OY=',NULL,'admin_test@example.com','','administrador',1,1,'admin_test','779630','2026-01-14 21:14:31.742135',1),
(8,'testpass123',NULL,'prueba@test.com','adanev','Estudiante',0,0,'adancito123',NULL,NULL,1),
(9,'pbkdf2_sha256$1200000$YURXgtUjSI1ZhUFWEBqIqx$h15NlypQj3wwxA/ok0wf61WXrOp/wJ4iO8ZigcWbJ7Q=',NULL,'admin_verify@test.com','','administrador',1,1,'admin_verify',NULL,NULL,1),
(16,'pbkdf2_sha256$1200000$ex65Ccm34dALh7NkqOOLCj$bRbmX6QYzsxl0UboE7TaQZi2X3AIEJnoQBAC6RnX/f4=',NULL,'student_crud@test.com','','estudiante',0,0,'STUDENT123',NULL,NULL,0),
(17,'pbkdf2_sha256$1200000$sQRtPbLjSiJ26rHlKqrlgf$nxuGLVYSi5ms2nAhrIIFAD2vZL1EUskK64ItvQITQ18=',NULL,'student_0_1468@test.com','','estudiante',1,0,'student_0_1468',NULL,NULL,0),
(18,'pbkdf2_sha256$1200000$xCTUuWayNJgoNbqAEFjSir$n0X4ZTwPtmJ4OGa1fxsOn1iAsdCdt9IN0C/xgwXMkrk=',NULL,'student_1_9604@test.com','','estudiante',1,0,'student_1_9604',NULL,NULL,0),
(19,'pbkdf2_sha256$1200000$fIymGSkm8dJvp9RWAI7lyi$oCv1Hza2f11QIH1uiEMLa78trIu+utmotIvUZDshQWE=',NULL,'student_2_2479@test.com','','estudiante',1,0,'student_2_2479',NULL,NULL,0),
(20,'pbkdf2_sha256$1200000$DYmkifxdoEwLlODIv4dfbA$RPJhsS0Xzgh7BeYPYK+yt9VhjZ1mIsiC8d/x3jpLxh0=',NULL,'student_3_9443@test.com','','estudiante',1,0,'student_3_9443',NULL,NULL,0),
(21,'pbkdf2_sha256$1200000$mF8kHV9l9i7kCzhuCjMrp5$fasdI7+QsD9vShWxkkCUB5uUUritdN2v1PDEJWsSQ7s=',NULL,'student_4_2977@test.com','','estudiante',1,0,'student_4_2977',NULL,NULL,0),
(22,'pbkdf2_sha256$1200000$UOKu2WeYNd2rZxVEjPM0x5$zY8ZtiiA96hoUEq4VsJO/qko04lda5l2gvX24FbL2To=',NULL,'student_5_6821@test.com','','estudiante',1,0,'student_5_6821',NULL,NULL,0),
(23,'pbkdf2_sha256$1200000$NE0ONUILA14Y8s0J78Z5xR$xwH8ug6nW41RL9WfMRthmEbDMQBfYSRuNJI3D6sRzm0=',NULL,'student_6_1320@test.com','','estudiante',1,0,'student_6_1320',NULL,NULL,0),
(24,'pbkdf2_sha256$1200000$oUimqunegAtEr65LoeAoL7$Hl+C2ADpojevTr7fQgwUae4QmYUKiUKdhYzSJG1Rwng=',NULL,'student_7_3514@test.com','','estudiante',1,0,'student_7_3514',NULL,NULL,0),
(25,'pbkdf2_sha256$1200000$30A21UbJNtCVLRO5rAU9EH$NXua19lKM6MRFumTvYTmT6TZCqLNWPibobnQeatJENk=',NULL,'student_8_1759@test.com','','estudiante',0,0,'student_8_1759',NULL,NULL,0),
(26,'pbkdf2_sha256$1200000$aBUIYyHl1g1m1XRMDQiVMc$qyhHeO50yhGnJD+LsIkhzbsxhRmSho7C7+SLG4xVdzw=',NULL,'student_9_3689@test.com','','estudiante',1,0,'student_9_3689',NULL,NULL,0),
(27,'pbkdf2_sha256$1200000$1MELiB92hBTVVojuhObOwW$JUJeUNiYSgvc85ai5ozxvAdwQIg37mwn8EWEgY2PBtM=',NULL,'student_10_2617@test.com','','estudiante',1,0,'student_10_2617',NULL,NULL,0),
(28,'pbkdf2_sha256$1200000$M823zynXAOdARIh4a8Xrfi$xixFAHCtZEBK2RmTB7xE7HssGkqYjPBFkRCQ6sbLMe8=',NULL,'student_11_3087@test.com','','estudiante',0,0,'student_11_3087',NULL,NULL,0),
(29,'pbkdf2_sha256$1200000$NxTrJBNDBrpiKKnMkRIoZY$pUvDecrFR4z1pv+Tg0mAN9eSs6KeFwpWxspssPfMjJM=',NULL,'student_12_4799@test.com','','estudiante',1,0,'student_12_4799',NULL,NULL,0),
(30,'pbkdf2_sha256$1200000$0LyoreRN6qrCKthPPOJogQ$QmmQv4DrTbUM20C1iyLAvef7sxlvfIfR0CUpYsO2/s4=',NULL,'student_13_6368@test.com','','estudiante',1,0,'student_13_6368',NULL,NULL,0),
(31,'pbkdf2_sha256$1200000$aoWGeRrGHMbjpnP2VX5oIM$f2//IDpUHHBDMsaGbM+6UqSjsPU93OfXgmwp/1ygRKw=',NULL,'student_14_1200@test.com','','estudiante',1,0,'student_14_1200',NULL,NULL,0),
(32,'pbkdf2_sha256$1200000$Wr5kTnExNymCqanRWzkwGP$hZ8TobmZCC4qrSBQzOLUhU5hxD9Xzpspt5NLOj6quFg=',NULL,'student_15_3220@test.com','','estudiante',1,0,'student_15_3220',NULL,NULL,0),
(33,'pbkdf2_sha256$1200000$ZoLCvkYgH11IOE9R3falR7$/VLV7fKgOo1fJoDXcKF04jkOb3c5EblPTAvgTZskV+M=',NULL,'student_16_6221@test.com','','estudiante',1,0,'student_16_6221',NULL,NULL,0),
(34,'pbkdf2_sha256$1200000$ZaSju1HcCxfB4aeBMgTSit$7Mknx9+hknUWHqhxv/ljuFhVQxNTaJxWzBLZCDYUC2E=',NULL,'student_17_2022@test.com','','estudiante',1,0,'student_17_2022',NULL,NULL,0),
(35,'pbkdf2_sha256$1200000$gKggrDAkB0HHvSTriM2car$rXGLFOi1do99u9CPVGMmjIe5m7D16uZfL0pkGdvD9FM=',NULL,'student_18_4298@test.com','','estudiante',1,0,'student_18_4298',NULL,NULL,0),
(36,'pbkdf2_sha256$1200000$2F3UXK9myMuTbsNTBdw5MZ$mkMnCI+KOaq7UAEJglsi6vz2YIj1LolPtEFitiAosqM=',NULL,'student_19_2004@test.com','','estudiante',1,0,'student_19_2004',NULL,NULL,0),
(37,'pbkdf2_sha256$1200000$JgQ7N6gRnFvOx28KN37G69$4ByBC/pirmEEFXB2qZsOQnRoU9zc94XBgiGWR/CEfJw=',NULL,'student_20_1007@test.com','','estudiante',1,0,'student_20_1007',NULL,NULL,0),
(38,'pbkdf2_sha256$1200000$EerHgJnMLFV14UvHcKGLl5$1Y++UYcusr0ofbADSFS+OaRSn1FsNAZcKHSu7lB4rcc=',NULL,'student_21_1115@test.com','','estudiante',1,0,'student_21_1115',NULL,NULL,0),
(39,'pbkdf2_sha256$1200000$lQVviGS4b9gJ5wxYJIa2HP$hbRgMsrrhrk7sl8zysGsVK4tFtLQE9gB5TP7w4mdPK8=',NULL,'student_22_1593@test.com','','estudiante',1,0,'student_22_1593',NULL,NULL,0),
(40,'pbkdf2_sha256$1200000$DyFo4Hzwzp4tOraVLLNMgW$juLY1z1Q3d/mtumJOgX1jOZ6p9lPqoj6UFA8uzmdLec=',NULL,'student_23_8078@test.com','','estudiante',1,0,'student_23_8078',NULL,NULL,0),
(41,'pbkdf2_sha256$1200000$jUTQVUdYGPRrcW5QiUzEJu$eCMMiFTBHiWobwMUKuT4vATNw3ngRmS1iFgImf+zC6Y=',NULL,'student_24_5431@test.com','','estudiante',1,0,'student_24_5431',NULL,NULL,0),
(42,'pbkdf2_sha256$1200000$JtFfmoJhO9K3YsJjAsa1Gr$1xdSz0RkeXBTkO8vP0NndEinIyr0EwdVZb3zb1JPRKo=',NULL,'student_25_5749@test.com','','estudiante',1,0,'student_25_5749',NULL,NULL,0),
(43,'pbkdf2_sha256$1200000$kj20PJy6kGQo8XvhUxoqoL$n3OIADQ95khizwgkjUjVh/+tWK6tRbnwl/mHQ22q8i0=',NULL,'student_26_3060@test.com','','estudiante',1,0,'student_26_3060',NULL,NULL,0),
(44,'pbkdf2_sha256$1200000$w6jGiTDUELfK3Euef7zfTH$NNUxwPb8obcRx/HXRYqYE1avY0JMUvzjuOGU2+6myMo=',NULL,'student_27_7915@test.com','','estudiante',1,0,'student_27_7915',NULL,NULL,0),
(45,'pbkdf2_sha256$1200000$cT6MLt6MUyEn2rf7rM2jJx$6lIIOCUxYK9y+O1XsL9EigHXpQ1jDRlrxedV16YiRYg=',NULL,'student_28_2491@test.com','','estudiante',1,0,'student_28_2491',NULL,NULL,0),
(46,'pbkdf2_sha256$1200000$2BlVavXhEim0lHrWQGLL96$vkEWfJlktI76kM2Gbbk/PK19wvF9GLxZ4dVUw9zKOB4=',NULL,'student_29_7825@test.com','','estudiante',1,0,'student_29_7825',NULL,NULL,0),
(47,'pbkdf2_sha256$1200000$ruj17uv0TjqJ7lJaNWDHeU$lxonQ7ZBpVDrbYq2M7eAw/gJFvM1sCkiJUUKzmAlaOo=',NULL,'student_0_1685@test.com','','estudiante',1,0,'student_0_1685',NULL,NULL,0),
(48,'pbkdf2_sha256$1200000$JDBGGYKNsOVscynJXzIYNN$pyxoy/ublMzj0wNGQCPa5wKfIhic6EwR3jRh6BavY5M=',NULL,'student_1_2090@test.com','','estudiante',1,0,'student_1_2090',NULL,NULL,0),
(49,'pbkdf2_sha256$1200000$OvumaIQ4vJO4CkaE2DVyNH$Usuw+tTiCzDe6gA04N2KySFuoT92dE/a4W0a76uswgw=',NULL,'student_2_9566@test.com','','estudiante',1,0,'student_2_9566',NULL,NULL,0),
(50,'pbkdf2_sha256$1200000$zrIkkil8PFKOEEZ3BPERkO$qsVz00OAAxxZm1GjSCZrX9IrIAQyF/SPF0Zpx54dipY=',NULL,'student_3_1698@test.com','','estudiante',1,0,'student_3_1698',NULL,NULL,0),
(51,'pbkdf2_sha256$1200000$XXNqKsGrYuiiH46oReZ9jo$TaIpeLS4USVOInhn1qyHLlS4/29MQ5DpF1XMyCKUDP8=',NULL,'student_4_9119@test.com','','estudiante',1,0,'student_4_9119',NULL,NULL,0),
(52,'pbkdf2_sha256$1200000$OsS9jRA7ofi6pBX51SKRwl$t3coh+Tk4x6wf3CQx1EdQKqoSEnsentTJk0+R3Nc/5M=',NULL,'student_5_4643@test.com','','estudiante',1,0,'student_5_4643',NULL,NULL,0),
(53,'pbkdf2_sha256$1200000$tXxQcLTcqys0vFHmCgVjUp$dkR92PSxLQeMHhWHguRfN5CC/37yRdV22U6lFwuq/tE=',NULL,'student_6_8534@test.com','','estudiante',1,0,'student_6_8534',NULL,NULL,0),
(54,'pbkdf2_sha256$1200000$3zSLX3uUoJs3NhGxw6SOqy$KEOzVtxuKvge7ky++IcysikPRIE/TrcwDreORju0HXc=',NULL,'student_7_5479@test.com','','estudiante',1,0,'student_7_5479',NULL,NULL,0),
(55,'pbkdf2_sha256$1200000$lXvSdqHOJySf3Tm0jhK76t$L7Qnrpt7SD7BS1fV6yTAmOx5tA/yzyGy3Za53Zk15eU=',NULL,'student_8_9706@test.com','','estudiante',1,0,'student_8_9706',NULL,NULL,0),
(56,'pbkdf2_sha256$1200000$JkfPAyq9BC6wrnnndIhU67$p89rJxnb/ChNwiOXIl1oYWozWMTHjKTSBa+7MhjJfGs=',NULL,'student_9_5652@test.com','','estudiante',1,0,'student_9_5652',NULL,NULL,0),
(57,'pbkdf2_sha256$1200000$eJHUv8xeBNkW1Ixnc5Hz7c$85b40lCd+MXXLTC3sPEutLmb4L2v1gOdK/7lHNDww5s=',NULL,'student_10_7371@test.com','','estudiante',1,0,'student_10_7371',NULL,NULL,0),
(58,'pbkdf2_sha256$1200000$ECumxo7amNp7v5xPkqwtzM$RvboqdAYCkqmgJy5HdhxnJtH858Ke6GHoDoZxDiL0eY=',NULL,'student_11_2128@test.com','','estudiante',1,0,'student_11_2128',NULL,NULL,0),
(59,'pbkdf2_sha256$1200000$ykAveBgkZRhF1mfuzJX0e4$Y/35jZMXVONveZAyBwbfi7LnDVKqw4jpILWwfAIThhI=',NULL,'student_12_6041@test.com','','estudiante',1,0,'student_12_6041',NULL,NULL,0),
(60,'pbkdf2_sha256$1200000$UGJMuK4q3sJpHWvyo4o1CE$2WHh/G/SCgrz4z2omNSTLEd4HN0/ek1jl9wVBg0MQU0=',NULL,'student_13_7314@test.com','','estudiante',1,0,'student_13_7314',NULL,NULL,0),
(61,'pbkdf2_sha256$1200000$BPDYITsBCLXySnL6wh27BK$1WkzAohChNNIMOSUqoJlRiSikxH76vdwkanokE7uYEE=',NULL,'student_14_3075@test.com','','estudiante',1,0,'student_14_3075',NULL,NULL,0),
(62,'pbkdf2_sha256$1200000$zpGt58HG7nr6ycZmWDerWE$wFSqPDIF3aTHm9DirJsHxs/AVTs9B6lXUQUKLA0SQWQ=',NULL,'student_15_1151@test.com','','estudiante',1,0,'student_15_1151',NULL,NULL,0),
(63,'pbkdf2_sha256$1200000$wAk3GRX5RcxXREZJZ0UrfQ$SvC1vv7YiV/BQsWeCZtmmL+ELn1P08N10/XyTM7O348=',NULL,'student_16_9351@test.com','','estudiante',1,0,'student_16_9351',NULL,NULL,0),
(64,'pbkdf2_sha256$1200000$QN1hsZAyjckv0XOVlkTyAI$AybKfhJzuDuct8PKJhqAXDpbE2Y5Gk9dxh6zjytfYDY=',NULL,'student_17_1759@test.com','','estudiante',1,0,'student_17_1759',NULL,NULL,0),
(65,'pbkdf2_sha256$1200000$Cq97cqDP6kGSw7aMY6XGKp$cJzL2alyhKDgLmW50CPv5dOFOJ7tmXhelT1WcXQ2/GA=',NULL,'student_18_4045@test.com','','estudiante',1,0,'student_18_4045',NULL,NULL,0),
(66,'pbkdf2_sha256$1200000$sTCS1vHYxPSEwDGjFnZJGz$zWnoXAjXrbkaGybpnwiMHOQ642qYj8Lax47ea2fcEAc=',NULL,'student_19_6407@test.com','','estudiante',1,0,'student_19_6407',NULL,NULL,0),
(67,'pbkdf2_sha256$1200000$nuJlLNWNdFcVNcGZpmRMy3$81DXcUwf7Nj3LWLF109YB0K3qd8wrctBZCK4Rd09WJE=',NULL,'student_20_1491@test.com','','estudiante',1,0,'student_20_1491',NULL,NULL,0),
(68,'pbkdf2_sha256$1200000$GGQ53ZEnw7Mu3zrEK3kDX9$y/UgoFVZzulj++M8bYu0AA7W9Gv9H2lSp/EAR1A1Y+E=',NULL,'student_21_2472@test.com','','estudiante',1,0,'student_21_2472',NULL,NULL,0),
(69,'pbkdf2_sha256$1200000$5H2mDx8IYm2WdxxStQrVgy$M3SjmR7bJ4FnECBvLeWvFDPbMIRnSuCz7+k/KKKRfUw=',NULL,'student_22_2212@test.com','','estudiante',1,0,'student_22_2212',NULL,NULL,0),
(70,'pbkdf2_sha256$1200000$wIssY5RM5NoV28pVlghcUU$gQV6Wz07vZ8sPsuuS0vLT3XVzSShOwF/xnMT5hmJHiM=',NULL,'student_23_3269@test.com','','estudiante',1,0,'student_23_3269',NULL,NULL,0),
(71,'pbkdf2_sha256$1200000$PhOBL5oJdzGuZe1avTk2Ku$aniDM3nAP5dmXBUHS/+SHH3uVQMCb7+RVLZ5DwgbKH0=',NULL,'student_24_2857@test.com','','estudiante',1,0,'student_24_2857',NULL,NULL,0),
(72,'pbkdf2_sha256$1200000$YKnx3ampMcuqjsqimD2WEb$2k6X4/+ZVSwHdoyrlcd0eGDTVLo4aFJU5PJr48Lpi9g=',NULL,'student_25_8416@test.com','','estudiante',1,0,'student_25_8416',NULL,NULL,0),
(73,'pbkdf2_sha256$1200000$tKYaX8oI8Aho1N71n5oM2M$0SCWWkfYAwgjWYpIRKYve6v13UhcfkvtoqvpLBa6Grg=',NULL,'student_26_8698@test.com','','estudiante',1,0,'student_26_8698',NULL,NULL,0),
(74,'pbkdf2_sha256$1200000$YSbcSQFuxQqIokWFKmkhCg$pacYj0W/xOFRjBsRyB1oB5Fef6oRXwBqbtH3bMZDI+Q=',NULL,'student_27_6221@test.com','','estudiante',1,0,'student_27_6221',NULL,NULL,0),
(75,'pbkdf2_sha256$1200000$EVhSX4OfDLP4tDOlly6nRb$/kz1LWCLwK+M9VBC+xvfcbBtDe9mn9JMpiK8DIxlOAQ=',NULL,'student_28_8696@test.com','','estudiante',1,0,'student_28_8696',NULL,NULL,0),
(76,'pbkdf2_sha256$1200000$LxdcMCAtfh90g8cp0loMOu$PFmKNc1ysjjjb7vrAhZvVZ4j2XD+TNNqUyGAMcWiuPk=',NULL,'student_29_6601@test.com','','estudiante',1,0,'student_29_6601',NULL,NULL,0),
(77,'testpass123',NULL,'bandit@test.com','bandit','Estudiante',1,0,'bandit0',NULL,NULL,1),
(78,'pbkdf2_sha256$1200000$HGGBzxOfuBQC5VhiztmtGC$NQnJ8g8ETnlTvm9ypHjPFQ7os2UDN3Q8rPlfZV4YVNo=',NULL,'test_1768949919@example.com','','estudiante',1,0,'TEST_USER_1768949919',NULL,NULL,0),
(79,'pbkdf2_sha256$1200000$fnme4Gd02Apz2P3vjtKv15$cEsRCCRzj5jrsDDTjK95DIdiOEHsAt5sMzBW7IljDvg=',NULL,'test_906028@school.com','','estudiante',0,0,'USER_906028',NULL,NULL,0),
(80,'pbkdf2_sha256$1200000$wmYnUxW5uvfu3RkyrAP3cf$afVRjc+XSLJhXrYn/hhGWL/vilWe65jA1eoiCucUjcU=',NULL,'test_923666@school.com','','estudiante',0,0,'USER_923666',NULL,NULL,0),
(81,'pbkdf2_sha256$1200000$DSgT0gMHnbvs24Zb0Mlnpr$GvINAl2IEIYr61VqKZ4ItE581be9EXUIe6oisSCXiPQ=',NULL,'e_830259@t.com','','estudiante',1,0,'U_830259',NULL,NULL,0),
(82,'pbkdf2_sha256$1200000$46n5A0V6mjsD7yJF6prdSZ$RN2MoiITVrXmHa5EYgPyh+tVb1uvfAp7BtkulSh+06M=',NULL,'e_828974@t.com','','estudiante',0,0,'U_828974',NULL,NULL,0),
(83,'pbkdf2_sha256$1200000$QShs4p3PZfMQoHMlnNgKry$OiDEWIdoENyxasbsMbWaZjHGQ3NwiyZ1wBK80O+Tio8=',NULL,'e_829740@t.com','','estudiante',0,0,'U_829740',NULL,NULL,0),
(84,'pbkdf2_sha256$1200000$AZvmqBqIgNaUrjhChTOQT5$91Au1q1C4YzGbHzmP6L51PM8Go02114pnLb+CsvVeR4=',NULL,'e_716821@t.com','','estudiante',0,0,'U_716821',NULL,NULL,0),
(85,'pbkdf2_sha256$1200000$oPcEojzHhFnfPhZbyxCMYq$g/vglxSKhxHBKfLniFK9d9J9rsUl3955qtlWouMYgOo=',NULL,'e_729293@t.com','','estudiante',0,0,'U_729293',NULL,NULL,0),
(86,'pbkdf2_sha256$1200000$7xKvccTDkIdPWnRRcpYR58$SL76hMJtVazKHpA+Kr3qGlInJt2ltNMautlVJrXD9l0=',NULL,'e_716081@t.com','','estudiante',0,0,'U_716081',NULL,NULL,0),
(89,'pbkdf2_sha256$1200000$zZsGxO56grOwm3lDVQKPf8$5iIvIFU3R0NGt52X4EFSTiTLA/M/M8E6rOmpECeQPtQ=',NULL,'testpass@gmail.com','adancito','estudiante',1,0,'adancito',NULL,NULL,0),
(90,'pbkdf2_sha256$1200000$mxLTCVPji4TxGDgN5s2i9P$d96y14I0ya5ztlTyACmAbCtSvH6BZx+0k7xgC/PHcXE=',NULL,'roberto@gmail.com','FLORENCIO MOHAMED','estudiante',1,0,'AAAAAAAAAAAAAAAAAAAA',NULL,NULL,0);
/*!40000 ALTER TABLE `users_user` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users_user_groups`
--

DROP TABLE IF EXISTS `users_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_groups_user_id_group_id_b88eab82_uniq` (`user_id`,`group_id`),
  KEY `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_user_groups_user_id_5f6f5a90_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_groups`
--

LOCK TABLES `users_user_groups` WRITE;
/*!40000 ALTER TABLE `users_user_groups` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `users_user_groups` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users_user_user_permissions`
--

DROP TABLE IF EXISTS `users_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_user_permissions_user_id_permission_id_43338c45_uniq` (`user_id`,`permission_id`),
  KEY `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_user_permissions_user_id_20aca447_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_user_permissions`
--

LOCK TABLES `users_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_user_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `users_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `usuarios_aspirantes`
--

DROP TABLE IF EXISTS `usuarios_aspirantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_aspirantes` (
  `folio` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`folio`),
  UNIQUE KEY `usuarios_aspirantes_email_d990f907_uniq` (`email`),
  KEY `idx_aspirante_folio` (`folio`),
  KEY `idx_aspirante_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_aspirantes`
--

LOCK TABLES `usuarios_aspirantes` WRITE;
/*!40000 ALTER TABLE `usuarios_aspirantes` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `usuarios_aspirantes` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `verification_codes`
--

DROP TABLE IF EXISTS `verification_codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `verification_codes` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `code` varchar(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `data_json` longtext DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_verification_email_code` (`email`,`code`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `verification_codes`
--

LOCK TABLES `verification_codes` WRITE;
/*!40000 ALTER TABLE `verification_codes` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `verification_codes` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-01-27 19:56:06
