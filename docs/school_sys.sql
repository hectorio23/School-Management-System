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
  `desactivar` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Menu`
--

LOCK TABLES `Menu` WRITE;
/*!40000 ALTER TABLE `Menu` DISABLE KEYS */;
set autocommit=0;
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
  `fecha_vencimiento` date DEFAULT NULL,
  `estatus` varchar(50) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `concepto_id` bigint(20) NOT NULL,
  `monto_pagado` decimal(10,2) NOT NULL,
  `generado_automaticamente` tinyint(1) NOT NULL,
  `justificacion_exencion` longtext DEFAULT NULL,
  `justificacion_manual` longtext DEFAULT NULL,
  `mes_correspondiente` date DEFAULT NULL,
  `recargo_exento` tinyint(1) NOT NULL,
  `adeudo_congelado` tinyint(1) NOT NULL,
  `dias_mora` int(11) NOT NULL,
  `recargo_fijo_aplicado` tinyint(1) NOT NULL,
  `tipo_adeudo` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_adeudo_estudiante` (`estudiante_id`),
  KEY `idx_adeudo_concepto` (`concepto_id`),
  KEY `idx_adeudo_vencimiento` (`fecha_vencimiento`),
  KEY `idx_adeudo_eststatus` (`estatus`),
  CONSTRAINT `adeudos_concepto_id_de3b7d87_fk_conceptos_pago_id` FOREIGN KEY (`concepto_id`) REFERENCES `conceptos_pago` (`id`),
  CONSTRAINT `adeudos_estudiante_id_83cfd3e8_fk_estudiantes_matricula` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiantes` (`matricula`)
) ENGINE=InnoDB AUTO_INCREMENT=369 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
-- Table structure for table `administradores_escolares`
--

DROP TABLE IF EXISTS `administradores_escolares`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `administradores_escolares` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `apellido_paterno` varchar(255) NOT NULL,
  `apellido_materno` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `nivel_educativo_id` bigint(20) DEFAULT NULL,
  `usuario_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  KEY `idx_adminesc_usuario` (`usuario_id`),
  KEY `idx_adminesc_nivel` (`nivel_educativo_id`),
  KEY `idx_adminesc_activo` (`activo`),
  CONSTRAINT `administradores_esco_nivel_educativo_id_5ec1c090_fk_niveles_e` FOREIGN KEY (`nivel_educativo_id`) REFERENCES `niveles_educativos` (`id`),
  CONSTRAINT `administradores_escolares_usuario_id_7f44c32b_fk_users_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administradores_escolares`
--

LOCK TABLES `administradores_escolares` WRITE;
/*!40000 ALTER TABLE `administradores_escolares` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `administradores_escolares` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `asignaciones_maestro`
--

DROP TABLE IF EXISTS `asignaciones_maestro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `asignaciones_maestro` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha_asignacion` date NOT NULL,
  `activa` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `ciclo_escolar_id` bigint(20) NOT NULL,
  `grupo_id` bigint(20) NOT NULL,
  `maestro_id` bigint(20) NOT NULL,
  `materia_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asignaciones_maestro_grupo_id_materia_id_cicl_3d969df9_uniq` (`grupo_id`,`materia_id`,`ciclo_escolar_id`),
  KEY `idx_asignacion_maestro` (`maestro_id`),
  KEY `idx_asignacion_grupo` (`grupo_id`),
  KEY `idx_asignacion_materia` (`materia_id`),
  KEY `idx_asignacion_ciclo` (`ciclo_escolar_id`),
  KEY `idx_asignacion_activa` (`activa`),
  CONSTRAINT `asignaciones_maestro_ciclo_escolar_id_1334f354_fk_ciclos_es` FOREIGN KEY (`ciclo_escolar_id`) REFERENCES `ciclos_escolares` (`id`),
  CONSTRAINT `asignaciones_maestro_grupo_id_08ab5361_fk_grupos_id` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`),
  CONSTRAINT `asignaciones_maestro_maestro_id_3813e65b_fk_maestros_id` FOREIGN KEY (`maestro_id`) REFERENCES `maestros` (`id`),
  CONSTRAINT `asignaciones_maestro_materia_id_1bd64a09_fk_materias_id` FOREIGN KEY (`materia_id`) REFERENCES `materias` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asignaciones_maestro`
--

LOCK TABLES `asignaciones_maestro` WRITE;
/*!40000 ALTER TABLE `asignaciones_maestro` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `asignaciones_maestro` ENABLE KEYS */;
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
  `precio_aplicado` decimal(10,2) DEFAULT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `menu_id` bigint(20) DEFAULT NULL,
  `adeudo_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asistencia_cafeteria_estudiante_id_fecha_asis_ff254b5c_uniq` (`estudiante_id`,`fecha_asistencia`,`tipo_comida`),
  UNIQUE KEY `adeudo_id` (`adeudo_id`),
  KEY `idx_cafeteria_estudiante` (`estudiante_id`),
  KEY `idx_cafeteria_fecha` (`fecha_asistencia`),
  KEY `asistencia_cafeteria_menu_id_c53b8e68_fk_Menu_id` (`menu_id`),
  CONSTRAINT `asistencia_cafeteria_adeudo_id_263eceef_fk_adeudos_id` FOREIGN KEY (`adeudo_id`) REFERENCES `adeudos` (`id`),
  CONSTRAINT `asistencia_cafeteria_estudiante_id_3911c454_fk_estudiant` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiantes` (`matricula`),
  CONSTRAINT `asistencia_cafeteria_menu_id_c53b8e68_fk_Menu_id` FOREIGN KEY (`menu_id`) REFERENCES `Menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
  `comentarios_analisis` longtext DEFAULT NULL,
  `comentarios_comite` longtext DEFAULT NULL,
  `fecha_entrevista_psicologia` date DEFAULT NULL,
  `fecha_examen_pedagogico` date DEFAULT NULL,
  `fecha_visita_domiciliaria` datetime(6) DEFAULT NULL,
  `nivel_ingreso` varchar(20) DEFAULT NULL,
  `foto_fachada_domicilio` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `curp` (`curp`),
  KEY `idx_aspirante_curp` (`curp`),
  KEY `idx_aspirante_fase` (`fase_actual`),
  CONSTRAINT `aspirantes_user_id_7887eb14_fk_usuarios_aspirantes_folio` FOREIGN KEY (`user_id`) REFERENCES `usuarios_aspirantes` (`folio`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=209 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
(132,'Can view Nivel Educativo',33,'view_niveleducativo'),
(133,'Can add login attempt',34,'add_loginattempt'),
(134,'Can change login attempt',34,'change_loginattempt'),
(135,'Can delete login attempt',34,'delete_loginattempt'),
(136,'Can view login attempt',34,'view_loginattempt'),
(137,'Can add Adeudo de Comedor',35,'add_adeudocomedor'),
(138,'Can change Adeudo de Comedor',35,'change_adeudocomedor'),
(139,'Can delete Adeudo de Comedor',35,'delete_adeudocomedor'),
(140,'Can view Adeudo de Comedor',35,'view_adeudocomedor'),
(141,'Can add administrador escolar',36,'add_administradorescolar'),
(142,'Can change administrador escolar',36,'change_administradorescolar'),
(143,'Can delete administrador escolar',36,'delete_administradorescolar'),
(144,'Can view administrador escolar',36,'view_administradorescolar'),
(145,'Can add asignacion maestro',37,'add_asignacionmaestro'),
(146,'Can change asignacion maestro',37,'change_asignacionmaestro'),
(147,'Can delete asignacion maestro',37,'delete_asignacionmaestro'),
(148,'Can view asignacion maestro',37,'view_asignacionmaestro'),
(149,'Can add calificacion',39,'add_calificacion'),
(150,'Can change calificacion',39,'change_calificacion'),
(151,'Can delete calificacion',39,'delete_calificacion'),
(152,'Can view calificacion',39,'view_calificacion'),
(153,'Can add autorizacion cambio calificacion',38,'add_autorizacioncambiocalificacion'),
(154,'Can change autorizacion cambio calificacion',38,'change_autorizacioncambiocalificacion'),
(155,'Can delete autorizacion cambio calificacion',38,'delete_autorizacioncambiocalificacion'),
(156,'Can view autorizacion cambio calificacion',38,'view_autorizacioncambiocalificacion'),
(157,'Can add maestro',41,'add_maestro'),
(158,'Can change maestro',41,'change_maestro'),
(159,'Can delete maestro',41,'delete_maestro'),
(160,'Can view maestro',41,'view_maestro'),
(161,'Can add materia',42,'add_materia'),
(162,'Can change materia',42,'change_materia'),
(163,'Can delete materia',42,'delete_materia'),
(164,'Can view materia',42,'view_materia'),
(165,'Can add calificacion final',40,'add_calificacionfinal'),
(166,'Can change calificacion final',40,'change_calificacionfinal'),
(167,'Can delete calificacion final',40,'delete_calificacionfinal'),
(168,'Can view calificacion final',40,'view_calificacionfinal'),
(169,'Can add modificacion manual calificacion',43,'add_modificacionmanualcalificacion'),
(170,'Can change modificacion manual calificacion',43,'change_modificacionmanualcalificacion'),
(171,'Can delete modificacion manual calificacion',43,'delete_modificacionmanualcalificacion'),
(172,'Can view modificacion manual calificacion',43,'view_modificacionmanualcalificacion'),
(173,'Can add periodo evaluacion',44,'add_periodoevaluacion'),
(174,'Can change periodo evaluacion',44,'change_periodoevaluacion'),
(175,'Can delete periodo evaluacion',44,'delete_periodoevaluacion'),
(176,'Can view periodo evaluacion',44,'view_periodoevaluacion'),
(177,'Can add programa educativo',45,'add_programaeducativo'),
(178,'Can change programa educativo',45,'change_programaeducativo'),
(179,'Can delete programa educativo',45,'delete_programaeducativo'),
(180,'Can view programa educativo',45,'view_programaeducativo'),
(181,'Can add Libro',46,'add_libro'),
(182,'Can change Libro',46,'change_libro'),
(183,'Can delete Libro',46,'delete_libro'),
(184,'Can view Libro',46,'view_libro'),
(185,'Can add Préstamo',48,'add_prestamo'),
(186,'Can change Préstamo',48,'change_prestamo'),
(187,'Can delete Préstamo',48,'delete_prestamo'),
(188,'Can view Préstamo',48,'view_prestamo'),
(189,'Can add Multa',47,'add_multa'),
(190,'Can change Multa',47,'change_multa'),
(191,'Can delete Multa',47,'delete_multa'),
(192,'Can view Multa',47,'view_multa'),
(193,'Can add Usuario de Biblioteca',49,'add_usuariobiblioteca'),
(194,'Can change Usuario de Biblioteca',49,'change_usuariobiblioteca'),
(195,'Can delete Usuario de Biblioteca',49,'delete_usuariobiblioteca'),
(196,'Can view Usuario de Biblioteca',49,'view_usuariobiblioteca'),
(197,'Can add Blacklisted Token',50,'add_blacklistedtoken'),
(198,'Can change Blacklisted Token',50,'change_blacklistedtoken'),
(199,'Can delete Blacklisted Token',50,'delete_blacklistedtoken'),
(200,'Can view Blacklisted Token',50,'view_blacklistedtoken'),
(201,'Can add Outstanding Token',51,'add_outstandingtoken'),
(202,'Can change Outstanding Token',51,'change_outstandingtoken'),
(203,'Can delete Outstanding Token',51,'delete_outstandingtoken'),
(204,'Can view Outstanding Token',51,'view_outstandingtoken'),
(205,'Can add evento calendario',52,'add_eventocalendario'),
(206,'Can change evento calendario',52,'change_eventocalendario'),
(207,'Can delete evento calendario',52,'delete_eventocalendario'),
(208,'Can view evento calendario',52,'view_eventocalendario');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `autorizaciones_cambio_calificacion`
--

DROP TABLE IF EXISTS `autorizaciones_cambio_calificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `autorizaciones_cambio_calificacion` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `motivo` longtext NOT NULL,
  `fecha_autorizacion` datetime(6) NOT NULL,
  `utilizada` tinyint(1) NOT NULL,
  `fecha_uso` datetime(6) DEFAULT NULL,
  `valor_anterior` decimal(4,2) DEFAULT NULL,
  `valor_nuevo` decimal(4,2) DEFAULT NULL,
  `autorizado_por_id` bigint(20) NOT NULL,
  `calificacion_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_autcalif_calificacion` (`calificacion_id`),
  KEY `idx_autcalif_admin` (`autorizado_por_id`),
  KEY `idx_autcalif_utilizada` (`utilizada`),
  CONSTRAINT `autorizaciones_cambi_autorizado_por_id_484e38dc_fk_administr` FOREIGN KEY (`autorizado_por_id`) REFERENCES `administradores_escolares` (`id`),
  CONSTRAINT `autorizaciones_cambi_calificacion_id_1232d9cd_fk_calificac` FOREIGN KEY (`calificacion_id`) REFERENCES `calificaciones` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `autorizaciones_cambio_calificacion`
--

LOCK TABLES `autorizaciones_cambio_calificacion` WRITE;
/*!40000 ALTER TABLE `autorizaciones_cambio_calificacion` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `autorizaciones_cambio_calificacion` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `becas_estudiantes`
--

LOCK TABLES `becas_estudiantes` WRITE;
/*!40000 ALTER TABLE `becas_estudiantes` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `becas_estudiantes` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `biblioteca_libros`
--

DROP TABLE IF EXISTS `biblioteca_libros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca_libros` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) NOT NULL,
  `autor` varchar(255) NOT NULL,
  `editorial` varchar(255) NOT NULL,
  `anio` int(11) NOT NULL,
  `genero` varchar(100) NOT NULL,
  `isbn` varchar(20) NOT NULL,
  `numero_de_ejemplares` int(10) unsigned NOT NULL CHECK (`numero_de_ejemplares` >= 0),
  `numero_de_ejemplares_prestados` int(10) unsigned NOT NULL CHECK (`numero_de_ejemplares_prestados` >= 0),
  PRIMARY KEY (`id`),
  UNIQUE KEY `isbn` (`isbn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca_libros`
--

LOCK TABLES `biblioteca_libros` WRITE;
/*!40000 ALTER TABLE `biblioteca_libros` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `biblioteca_libros` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `biblioteca_multas`
--

DROP TABLE IF EXISTS `biblioteca_multas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca_multas` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `monto` decimal(10,2) NOT NULL,
  `fecha_de_pago` date DEFAULT NULL,
  `estado` varchar(20) NOT NULL,
  `prestamo_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `prestamo_id` (`prestamo_id`),
  CONSTRAINT `biblioteca_multas_prestamo_id_3a6e35bb_fk_bibliotec` FOREIGN KEY (`prestamo_id`) REFERENCES `biblioteca_prestamos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca_multas`
--

LOCK TABLES `biblioteca_multas` WRITE;
/*!40000 ALTER TABLE `biblioteca_multas` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `biblioteca_multas` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `biblioteca_prestamos`
--

DROP TABLE IF EXISTS `biblioteca_prestamos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca_prestamos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha_de_prestamo` date NOT NULL,
  `fecha_de_devolucion` date NOT NULL,
  `estado` varchar(20) NOT NULL,
  `fecha_real_devolucion` date DEFAULT NULL,
  `libro_id` bigint(20) NOT NULL,
  `usuario_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `biblioteca_prestamos_usuario_id_5735614b_fk_bibliotec` (`usuario_id`),
  KEY `biblioteca_prestamos_libro_id_0c258324_fk_biblioteca_libros_id` (`libro_id`),
  CONSTRAINT `biblioteca_prestamos_libro_id_0c258324_fk_biblioteca_libros_id` FOREIGN KEY (`libro_id`) REFERENCES `biblioteca_libros` (`id`),
  CONSTRAINT `biblioteca_prestamos_usuario_id_5735614b_fk_bibliotec` FOREIGN KEY (`usuario_id`) REFERENCES `biblioteca_usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca_prestamos`
--

LOCK TABLES `biblioteca_prestamos` WRITE;
/*!40000 ALTER TABLE `biblioteca_prestamos` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `biblioteca_prestamos` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `biblioteca_usuarios`
--

DROP TABLE IF EXISTS `biblioteca_usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca_usuarios` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `apellido` varchar(200) NOT NULL,
  `email` varchar(254) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` longtext DEFAULT NULL,
  `tipo_de_usuario` varchar(20) NOT NULL,
  `usuario_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `biblioteca_usuarios_usuario_id_62e1312c_fk_users_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca_usuarios`
--

LOCK TABLES `biblioteca_usuarios` WRITE;
/*!40000 ALTER TABLE `biblioteca_usuarios` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `biblioteca_usuarios` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `calificaciones`
--

DROP TABLE IF EXISTS `calificaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `calificaciones` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `calificacion` decimal(4,2) NOT NULL,
  `puede_modificar` tinyint(1) NOT NULL,
  `fecha_captura` datetime(6) NOT NULL,
  `fecha_ultima_modificacion` datetime(6) NOT NULL,
  `asignacion_maestro_id` bigint(20) NOT NULL,
  `autorizada_por_id` bigint(20) DEFAULT NULL,
  `estudiante_id` int(11) NOT NULL,
  `capturada_por_id` bigint(20) NOT NULL,
  `modificada_por_id` bigint(20) DEFAULT NULL,
  `periodo_evaluacion_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `calificaciones_estudiante_id_asignacion_8bcd3a9f_uniq` (`estudiante_id`,`asignacion_maestro_id`,`periodo_evaluacion_id`),
  KEY `calificaciones_capturada_por_id_1d30b50b_fk_maestros_id` (`capturada_por_id`),
  KEY `calificaciones_modificada_por_id_414ce90e_fk_maestros_id` (`modificada_por_id`),
  KEY `idx_calif_estudiante` (`estudiante_id`),
  KEY `idx_calif_asignacion` (`asignacion_maestro_id`),
  KEY `idx_calif_periodo` (`periodo_evaluacion_id`),
  KEY `idx_calif_captura` (`fecha_captura`),
  KEY `calificaciones_autorizada_por_id_de0f48a8_fk_administr` (`autorizada_por_id`),
  CONSTRAINT `calificaciones_asignacion_maestro_i_0dc295de_fk_asignacio` FOREIGN KEY (`asignacion_maestro_id`) REFERENCES `asignaciones_maestro` (`id`),
  CONSTRAINT `calificaciones_autorizada_por_id_de0f48a8_fk_administr` FOREIGN KEY (`autorizada_por_id`) REFERENCES `administradores_escolares` (`id`),
  CONSTRAINT `calificaciones_capturada_por_id_1d30b50b_fk_maestros_id` FOREIGN KEY (`capturada_por_id`) REFERENCES `maestros` (`id`),
  CONSTRAINT `calificaciones_estudiante_id_db8aad9a_fk_estudiantes_matricula` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiantes` (`matricula`),
  CONSTRAINT `calificaciones_modificada_por_id_414ce90e_fk_maestros_id` FOREIGN KEY (`modificada_por_id`) REFERENCES `maestros` (`id`),
  CONSTRAINT `calificaciones_periodo_evaluacion_i_c1c69a8b_fk_periodos_` FOREIGN KEY (`periodo_evaluacion_id`) REFERENCES `periodos_evaluacion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calificaciones`
--

LOCK TABLES `calificaciones` WRITE;
/*!40000 ALTER TABLE `calificaciones` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `calificaciones` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `calificaciones_finales`
--

DROP TABLE IF EXISTS `calificaciones_finales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `calificaciones_finales` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `calificaciones_periodos` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`calificaciones_periodos`)),
  `calificacion_final` decimal(4,2) NOT NULL,
  `estatus` varchar(2) NOT NULL,
  `modificacion_manual` tinyint(1) NOT NULL,
  `calificacion_recursamiento` decimal(4,2) DEFAULT NULL,
  `fecha_calculo` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `ciclo_escolar_id` bigint(20) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `materia_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `calificaciones_finales_estudiante_id_materia_id_38548a6e_uniq` (`estudiante_id`,`materia_id`,`ciclo_escolar_id`),
  KEY `idx_calfinal_estudiante` (`estudiante_id`),
  KEY `idx_calfinal_materia` (`materia_id`),
  KEY `idx_calfinal_ciclo` (`ciclo_escolar_id`),
  KEY `idx_calfinal_estatus` (`estatus`),
  CONSTRAINT `calificaciones_final_ciclo_escolar_id_9c961b2c_fk_ciclos_es` FOREIGN KEY (`ciclo_escolar_id`) REFERENCES `ciclos_escolares` (`id`),
  CONSTRAINT `calificaciones_final_estudiante_id_76539d89_fk_estudiant` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiantes` (`matricula`),
  CONSTRAINT `calificaciones_finales_materia_id_2e6ba047_fk_materias_id` FOREIGN KEY (`materia_id`) REFERENCES `materias` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calificaciones_finales`
--

LOCK TABLES `calificaciones_finales` WRITE;
/*!40000 ALTER TABLE `calificaciones_finales` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `calificaciones_finales` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ciclos_escolares`
--

LOCK TABLES `ciclos_escolares` WRITE;
/*!40000 ALTER TABLE `ciclos_escolares` DISABLE KEYS */;
set autocommit=0;
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
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=1383 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
set autocommit=0;
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
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_content_type` VALUES
(36,'academico','administradorescolar'),
(37,'academico','asignacionmaestro'),
(38,'academico','autorizacioncambiocalificacion'),
(39,'academico','calificacion'),
(40,'academico','calificacionfinal'),
(52,'academico','eventocalendario'),
(41,'academico','maestro'),
(42,'academico','materia'),
(43,'academico','modificacionmanualcalificacion'),
(44,'academico','periodoevaluacion'),
(45,'academico','programaeducativo'),
(2,'admin','logentry'),
(26,'admissions','admissiontutor'),
(27,'admissions','admissiontutoraspirante'),
(28,'admissions','admissionuser'),
(29,'admissions','aspirante'),
(30,'admissions','verificationcode'),
(3,'auth','group'),
(4,'auth','permission'),
(46,'biblioteca','libro'),
(47,'biblioteca','multa'),
(48,'biblioteca','prestamo'),
(49,'biblioteca','usuariobiblioteca'),
(35,'comedor','adeudocomedor'),
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
(50,'token_blacklist','blacklistedtoken'),
(51,'token_blacklist','outstandingtoken'),
(34,'users','loginattempt'),
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
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
(57,'pagos','0013_conceptopago_tipo_concepto_and_more','2026-01-27 16:54:05.657226'),
(58,'admissions','0011_aspirante_comentarios_analisis_and_more','2026-01-28 20:33:36.119672'),
(59,'admissions','0012_aspirante_nivel_ingreso','2026-01-28 23:07:49.208313'),
(60,'users','0005_loginattempt','2026-01-29 23:14:59.491444'),
(61,'estudiantes','0009_alter_grado_orden_global','2026-01-29 23:17:28.390061'),
(62,'comedor','0005_adeudocomedor','2026-01-29 23:17:28.530083'),
(63,'pagos','0014_remove_adeudo_idx_adeudo_seguimiento_and_more','2026-01-30 21:58:30.908944'),
(64,'comedor','0006_remove_adeudocomedor_idx_adeudo_comedor_pagado_and_more','2026-01-30 21:58:31.082701'),
(65,'estudiantes','0010_estudiante_curp_estudiante_escuela_procedencia_and_more','2026-02-01 03:33:36.054804'),
(66,'pagos','0015_adeudo_adeudo_congelado_adeudo_dias_mora_and_more','2026-02-01 03:33:36.237709'),
(67,'users','0006_alter_user_role','2026-02-02 21:58:55.059078'),
(68,'pagos','0016_alter_adeudo_fecha_vencimiento','2026-02-02 22:14:38.008484'),
(69,'users','0007_alter_user_role','2026-02-02 22:15:17.532106'),
(70,'pagos','0017_alter_adeudo_fecha_vencimiento','2026-02-04 00:45:17.955207'),
(71,'comedor','0007_alter_asistenciacafeteria_precio_aplicado','2026-02-04 00:56:30.725138'),
(72,'comedor','0008_remove_menu_precio','2026-02-04 01:03:55.296613'),
(73,'estudiantes','0011_remove_estudiante_idx_estudiante_grupo_and_more','2026-02-04 20:14:15.498911'),
(74,'estudiantes','0012_remove_inscripcion_idx_inscripcion_ciclo_and_more','2026-02-04 22:03:07.148318'),
(75,'pagos','0018_adeudo_tipo_adeudo','2026-02-04 23:14:37.526965'),
(76,'comedor','0009_remove_adeudocomedor_idx_adeudo_comedor_est_and_more','2026-02-04 23:14:37.678367'),
(77,'academico','0001_initial','2026-02-06 22:11:25.248919'),
(78,'users','0008_alter_user_role','2026-02-06 22:11:25.261709'),
(79,'biblioteca','0001_initial','2026-02-10 23:58:39.398138'),
(80,'users','0009_alter_user_role','2026-02-10 23:58:39.415630'),
(81,'token_blacklist','0001_initial','2026-02-11 00:43:10.311799'),
(82,'token_blacklist','0002_outstandingtoken_jti_hex','2026-02-11 00:43:10.342611'),
(83,'token_blacklist','0003_auto_20171017_2007','2026-02-11 00:43:10.396343'),
(84,'token_blacklist','0004_auto_20171017_2013','2026-02-11 00:43:10.461383'),
(85,'token_blacklist','0005_remove_outstandingtoken_jti','2026-02-11 00:43:10.494651'),
(86,'token_blacklist','0006_auto_20171017_2113','2026-02-11 00:43:10.525651'),
(87,'token_blacklist','0007_auto_20171017_2214','2026-02-11 00:43:10.789611'),
(88,'token_blacklist','0008_migrate_to_bigautofield','2026-02-11 00:43:10.978342'),
(89,'token_blacklist','0010_fix_migrate_to_bigautofield','2026-02-11 00:43:11.034959'),
(90,'token_blacklist','0011_linearizes_history','2026-02-11 00:43:11.036717'),
(91,'token_blacklist','0012_alter_outstandingtoken_user','2026-02-11 00:43:11.079135'),
(92,'token_blacklist','0013_alter_blacklistedtoken_options_and_more','2026-02-11 00:43:11.098209'),
(93,'academico','0002_remove_maestro_email_remove_materia_fecha_fin_and_more','2026-02-13 04:03:19.950148'),
(94,'admissions','0013_remove_admissiontutor_foto_fachada_domicilio_and_more','2026-02-17 22:19:50.681589'),
(95,'estudiantes','0013_estudiantetutor_es_principal','2026-02-18 00:41:20.578899'),
(96,'academico','0003_eventocalendario','2026-02-18 19:35:03.508537'),
(97,'pagos','0019_alter_pago_metodo_pago','2026-02-18 19:38:43.676930'),
(98,'estudiantes','0014_alter_inscripcion_grupo','2026-02-19 23:18:35.832701'),
(99,'academico','0004_alter_administradorescolar_nivel_educativo_and_more','2026-02-19 23:18:36.105274'),
(100,'users','0010_alter_user_role','2026-02-19 23:58:29.320523');
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
('61lis8r370zbha44rrsqm9fd3ebafx74','.eJxVjDsOwyAQBe9CHSGD-Tllep8BscsSnEQgGbuKcvdgyUXSzsx7b-bDvmW_N1r9EtmVCWXZ5ZdCwCeVQ8VHKPfKsZZtXYAfCT9t43ON9Lqd7d9BDi33dUhGUQQcyWrtkNJAg3AStCYwRsoRSVrA1OlkHFg7oVBaKDl2l5Jhny9KODg-:1vtadX:UeBtoPaGofvK6PQ-70CHLQZCba3NrKXdOLO_IFsDhU8','2026-03-07 00:14:19.024113'),
('dwpvx1fqoclttjn0k7ahwp144boxpr9o','.eJxVjDsOwjAQBe_iGln-rZ1Q0nMGa9dr4wBypDipEHeHSCmgfTPzXiLitta49bzEicVZeHH63QjTI7cd8B3bbZZpbusykdwVedAurzPn5-Vw_w4q9vqtIZfCLoHRqIPTiiyz8UgjKlJoDQckp4LSNoEOACpZBsfDAOxpLCTeH-wMN-M:1vkS8p:VG6Nxqk4DJ4F5CuMwa1yt7h_T0_6hV2Kip5NpTCfiDA','2026-02-09 19:20:51.879519'),
('fu7jhpatze0b6q2kesnfmq6agu62ticv','.eJxVjDsOwjAQBe_iGln-rZ1Q0nMGa9dr4wBypDipEHeHSCmgfTPzXiLitta49bzEicVZeHH63QjTI7cd8B3bbZZpbusykdwVedAurzPn5-Vw_w4q9vqtIZfCLoHRqIPTiiyz8UgjKlJoDQckp4LSNoEOACpZBsfDAOxpLCTeH-wMN-M:1vg8dI:lA6MIU3c_Ec4JWvYKciojmoiQp3QXMPDSImkbmF714A','2026-01-28 21:42:28.928797'),
('ma4zf92ag8wz6y27a8ku0n4ycf8yuhi6','.eJxVjMsOwiAQRf-FtSGFysule7-BzDCDVA0kpV0Z_92QdKHbe865bxFh30rcO69xIXERszj9bgjpyXUAekC9N5la3dYF5VDkQbu8NeLX9XD_Dgr0MmoNQSUINin03jsCnRGVYzRmziYrjZQsJRPIoIaJ2ejJzs568O6MLD5fBhs4lQ:1verBc:WrN3QPx-lk7alNXi8Aeka5qT-moC742T18lVWw3KsbY','2026-01-25 08:52:36.278559'),
('oqvo9kptxvxsiisuq13nn41wsgntft0p','.eJxVjDsOwjAQBe_iGln-rZ1Q0nMGa9dr4wBypDipEHeHSCmgfTPzXiLitta49bzEicVZeHH63QjTI7cd8B3bbZZpbusykdwVedAurzPn5-Vw_w4q9vqtIZfCLoHRqIPTiiyz8UgjKlJoDQckp4LSNoEOACpZBsfDAOxpLCTeH-wMN-M:1vhJEf:NgY9F1pXKnpyM69aUeypBCoBDZUuJdYEV8KTzf-9AB4','2026-02-01 03:13:53.559281'),
('twoh2h80gw2863j5hg5oeharge9qvgla','.eJxVjDsOwjAQRO_iGll2_Fso6TmDtV5vcADZUpxUiLuTSCmgG817M28RcV1KXDvPccriIpw4_XYJ6cl1B_mB9d4ktbrMU5K7Ig_a5a1lfl0P9--gYC_b2toBIXDShrLzW8wKWEFipQfS5NiP3ngeLQKb7AgDJSAInqxV5qzF5wvszjgI:1vfSNb:Xqjy_B7NUDIHvh7R9NXYFdxY8EnR8msf9uBEuTg96DE','2026-01-27 00:35:27.355781'),
('zyhuy2vzf81li3ivrcl7k5wsek6liils','.eJxVjDsOwjAQBe_iGln-rZ1Q0nMGa9dr4wBypDipEHeHSCmgfTPzXiLitta49bzEicVZeHH63QjTI7cd8B3bbZZpbusykdwVedAurzPn5-Vw_w4q9vqtIZfCLoHRqIPTiiyz8UgjKlJoDQckp4LSNoEOACpZBsfDAOxpLCTeH-wMN-M:1vtCxb:I1Ce_BsfMEV-seKk0k9Kdw6CjZ6OuFXtsJNvTVRRpes','2026-03-05 22:57:27.886261');
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
(5,'EGRESADO','Estado EGRESADO',0),
(14,'Baja por Falta de Pago','Estudiante dado de baja por adeudo prolongado',0),
(15,'No Reinscrito','Pendiente de pago de reinscripción',0);
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
  `updateable` tinyint(1) NOT NULL,
  `alergias_alimentarias` longtext DEFAULT NULL,
  `porcentaje_beca` decimal(5,2) NOT NULL,
  `curp` varchar(18) DEFAULT NULL,
  `escuela_procedencia` varchar(255) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `sexo` varchar(1) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`matricula`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  UNIQUE KEY `curp` (`curp`),
  KEY `idx_estudiante_matricula` (`matricula`),
  KEY `idx_estudiante_nombre_completo` (`apellido_paterno`,`apellido_materno`,`nombre`),
  CONSTRAINT `estudiantes_usuario_id_42607c6a_fk_users_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estudiantes`
--

LOCK TABLES `estudiantes` WRITE;
/*!40000 ALTER TABLE `estudiantes` DISABLE KEYS */;
set autocommit=0;
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
  `es_principal` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `estudiantes_tutores_estudiante_matricula_tutor_id_72e6c895_uniq` (`estudiante_matricula`,`tutor_id`),
  KEY `idx_estudiantetutor_estudiante` (`estudiante_matricula`),
  KEY `idx_estudiantetutor_tutor` (`tutor_id`),
  CONSTRAINT `estudiantes_tutores_estudiante_matricula_a3dca86b_fk_estudiant` FOREIGN KEY (`estudiante_matricula`) REFERENCES `estudiantes` (`matricula`),
  CONSTRAINT `estudiantes_tutores_tutor_id_a72f9574_fk_tutores_id` FOREIGN KEY (`tutor_id`) REFERENCES `tutores` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estudiantes_tutores`
--

LOCK TABLES `estudiantes_tutores` WRITE;
/*!40000 ALTER TABLE `estudiantes_tutores` DISABLE KEYS */;
set autocommit=0;
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
  `porcentaje_descuento_snapshot` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `evaluaciones_socioeconomicas_estrato_id_d58b0b82_fk_estratos_id` (`estrato_id`),
  KEY `idx_evalsocio_estudiante` (`estudiante_matricula`),
  KEY `idx_evalsocio_fecha` (`fecha_evaluacion`),
  KEY `idx_evalsocio_aprobado` (`aprobado`),
  KEY `evaluaciones_socioec_estrato_sugerido_id_e7b84d0e_fk_estratos_` (`estrato_sugerido_id`),
  CONSTRAINT `evaluaciones_socioec_estrato_sugerido_id_e7b84d0e_fk_estratos_` FOREIGN KEY (`estrato_sugerido_id`) REFERENCES `estratos` (`id`),
  CONSTRAINT `evaluaciones_socioec_estudiante_matricula_0ebd0a32_fk_estudiant` FOREIGN KEY (`estudiante_matricula`) REFERENCES `estudiantes` (`matricula`),
  CONSTRAINT `evaluaciones_socioeconomicas_estrato_id_d58b0b82_fk_estratos_id` FOREIGN KEY (`estrato_id`) REFERENCES `estratos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluaciones_socioeconomicas`
--

LOCK TABLES `evaluaciones_socioeconomicas` WRITE;
/*!40000 ALTER TABLE `evaluaciones_socioeconomicas` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `evaluaciones_socioeconomicas` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `eventos_calendario`
--

DROP TABLE IF EXISTS `eventos_calendario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventos_calendario` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) NOT NULL,
  `descripcion` longtext DEFAULT NULL,
  `fecha_inicio` datetime(6) NOT NULL,
  `fecha_fin` datetime(6) NOT NULL,
  `tipo_evento` varchar(20) NOT NULL,
  `color` varchar(7) NOT NULL,
  `es_global` tinyint(1) NOT NULL,
  `nivel_educativo_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `eventos_calendario_nivel_educativo_id_8079fdf5_fk_niveles_e` (`nivel_educativo_id`),
  CONSTRAINT `eventos_calendario_nivel_educativo_id_8079fdf5_fk_niveles_e` FOREIGN KEY (`nivel_educativo_id`) REFERENCES `niveles_educativos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos_calendario`
--

LOCK TABLES `eventos_calendario` WRITE;
/*!40000 ALTER TABLE `eventos_calendario` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `eventos_calendario` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
(39,'3°','Secundaria',3,12,3),
(54,'1°','1',1,0,1),
(55,'2°','2',1,0,1),
(56,'3°','3',1,0,1),
(57,'4°','4',1,0,1),
(58,'5°','5',1,0,1),
(59,'6°','6',1,0,1),
(62,'4°','PREESCOLAR',4,4,1),
(63,'5°','PREESCOLAR',5,5,1),
(64,'6°','PREESCOLAR',6,6,1),
(65,'4°','SECUNDARIA',4,16,3),
(66,'5°','SECUNDARIA',5,17,3),
(67,'6°','SECUNDARIA',6,18,3);
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
) ENGINE=InnoDB AUTO_INCREMENT=466 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupos`
--

LOCK TABLES `grupos` WRITE;
/*!40000 ALTER TABLE `grupos` DISABLE KEYS */;
set autocommit=0;
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
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_estados_estudiante`
--

LOCK TABLES `historial_estados_estudiante` WRITE;
/*!40000 ALTER TABLE `historial_estados_estudiante` DISABLE KEYS */;
set autocommit=0;
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
  `estudiante_id` int(11) NOT NULL,
  `grupo_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inscripciones_estudiante_id_grupo_id_f004ae54_uniq` (`estudiante_id`,`grupo_id`),
  KEY `inscripciones_grupo_id_f5e700cb_fk_grupos_id` (`grupo_id`),
  KEY `idx_inscripcion_estudiante` (`estudiante_id`),
  KEY `idx_inscripcion_estatus` (`estatus`),
  CONSTRAINT `inscripciones_estudiante_id_64dcccda_fk_estudiantes_matricula` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiantes` (`matricula`),
  CONSTRAINT `inscripciones_grupo_id_f5e700cb_fk_grupos_id` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscripciones`
--

LOCK TABLES `inscripciones` WRITE;
/*!40000 ALTER TABLE `inscripciones` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `inscripciones` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `login_attempts`
--

DROP TABLE IF EXISTS `login_attempts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_attempts` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `ip_address` char(39) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `was_successful` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_login_email_time` (`email`,`timestamp`),
  KEY `idx_login_ip_time` (`ip_address`,`timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_attempts`
--

LOCK TABLES `login_attempts` WRITE;
/*!40000 ALTER TABLE `login_attempts` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `login_attempts` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `maestros`
--

DROP TABLE IF EXISTS `maestros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `maestros` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `apellido_paterno` varchar(255) NOT NULL,
  `apellido_materno` varchar(255) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `fecha_contratacion` date NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `nivel_educativo_id` bigint(20) NOT NULL,
  `usuario_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  KEY `idx_maestro_usuario` (`usuario_id`),
  KEY `idx_maestro_nivel` (`nivel_educativo_id`),
  KEY `idx_maestro_activo` (`activo`),
  CONSTRAINT `maestros_nivel_educativo_id_e284bebe_fk_niveles_educativos_id` FOREIGN KEY (`nivel_educativo_id`) REFERENCES `niveles_educativos` (`id`),
  CONSTRAINT `maestros_usuario_id_cbe29ae5_fk_users_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maestros`
--

LOCK TABLES `maestros` WRITE;
/*!40000 ALTER TABLE `maestros` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `maestros` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `materias`
--

DROP TABLE IF EXISTS `materias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `materias` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `clave` varchar(20) NOT NULL,
  `descripcion` longtext DEFAULT NULL,
  `creditos` decimal(4,2) NOT NULL,
  `activa` tinyint(1) NOT NULL,
  `orden` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `grado_id` bigint(20) NOT NULL,
  `programa_educativo_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `clave` (`clave`),
  KEY `idx_materia_grado` (`grado_id`),
  KEY `idx_materia_programa` (`programa_educativo_id`),
  KEY `idx_materia_activa` (`activa`),
  CONSTRAINT `materias_grado_id_7bfd0332_fk_grados_id` FOREIGN KEY (`grado_id`) REFERENCES `grados` (`id`),
  CONSTRAINT `materias_programa_educativo_i_a01577e6_fk_programas` FOREIGN KEY (`programa_educativo_id`) REFERENCES `programas_educativos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materias`
--

LOCK TABLES `materias` WRITE;
/*!40000 ALTER TABLE `materias` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `materias` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menus_semanales`
--

LOCK TABLES `menus_semanales` WRITE;
/*!40000 ALTER TABLE `menus_semanales` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `menus_semanales` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `modificaciones_manuales_calificaciones`
--

DROP TABLE IF EXISTS `modificaciones_manuales_calificaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `modificaciones_manuales_calificaciones` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `valor_anterior` decimal(4,2) NOT NULL,
  `valor_nuevo` decimal(4,2) NOT NULL,
  `motivo` longtext NOT NULL,
  `estatus_anterior` varchar(2) NOT NULL,
  `estatus_nuevo` varchar(2) NOT NULL,
  `fecha_modificacion` datetime(6) NOT NULL,
  `calificacion_id` bigint(20) NOT NULL,
  `calificacion_final_id` bigint(20) NOT NULL,
  `modificado_por_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_modman_calfinal` (`calificacion_final_id`),
  KEY `idx_modman_calif` (`calificacion_id`),
  KEY `idx_modman_admin` (`modificado_por_id`),
  KEY `idx_modman_fecha` (`fecha_modificacion`),
  CONSTRAINT `modificaciones_manua_calificacion_final_i_f99575b2_fk_calificac` FOREIGN KEY (`calificacion_final_id`) REFERENCES `calificaciones_finales` (`id`),
  CONSTRAINT `modificaciones_manua_calificacion_id_4553bdb8_fk_calificac` FOREIGN KEY (`calificacion_id`) REFERENCES `calificaciones` (`id`),
  CONSTRAINT `modificaciones_manua_modificado_por_id_553c140a_fk_administr` FOREIGN KEY (`modificado_por_id`) REFERENCES `administradores_escolares` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modificaciones_manuales_calificaciones`
--

LOCK TABLES `modificaciones_manuales_calificaciones` WRITE;
/*!40000 ALTER TABLE `modificaciones_manuales_calificaciones` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `modificaciones_manuales_calificaciones` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
  KEY `pagos_adeudo_id_14279390` (`adeudo_id`),
  CONSTRAINT `pagos_adeudo_id_14279390_fk_adeudos_id` FOREIGN KEY (`adeudo_id`) REFERENCES `adeudos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
-- Table structure for table `periodos_evaluacion`
--

DROP TABLE IF EXISTS `periodos_evaluacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `periodos_evaluacion` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `numero_periodo` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `fecha_inicio_captura` date NOT NULL,
  `fecha_fin_captura` date NOT NULL,
  `estatus` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `ciclo_escolar_id` bigint(20) NOT NULL,
  `programa_educativo_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `periodos_evaluacion_ciclo_escolar_id_program_980d46ae_uniq` (`ciclo_escolar_id`,`programa_educativo_id`,`numero_periodo`),
  KEY `idx_periodo_ciclo` (`ciclo_escolar_id`),
  KEY `idx_periodo_programa` (`programa_educativo_id`),
  KEY `idx_periodo_estatus` (`estatus`),
  CONSTRAINT `periodos_evaluacion_ciclo_escolar_id_bb2f9a82_fk_ciclos_es` FOREIGN KEY (`ciclo_escolar_id`) REFERENCES `ciclos_escolares` (`id`),
  CONSTRAINT `periodos_evaluacion_programa_educativo_i_d886f6e4_fk_programas` FOREIGN KEY (`programa_educativo_id`) REFERENCES `programas_educativos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `periodos_evaluacion`
--

LOCK TABLES `periodos_evaluacion` WRITE;
/*!40000 ALTER TABLE `periodos_evaluacion` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `periodos_evaluacion` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `programas_educativos`
--

DROP TABLE IF EXISTS `programas_educativos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `programas_educativos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext DEFAULT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date DEFAULT NULL,
  `numero_periodos_evaluacion` int(11) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `nivel_educativo_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_programa_nivel` (`nivel_educativo_id`),
  KEY `idx_programa_activo` (`activo`),
  CONSTRAINT `programas_educativos_nivel_educativo_id_eafad1ea_fk_niveles_e` FOREIGN KEY (`nivel_educativo_id`) REFERENCES `niveles_educativos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programas_educativos`
--

LOCK TABLES `programas_educativos` WRITE;
/*!40000 ALTER TABLE `programas_educativos` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `programas_educativos` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

DROP TABLE IF EXISTS `token_blacklist_blacklistedtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_blacklistedtoken`
--

LOCK TABLES `token_blacklist_blacklistedtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `token_blacklist_blacklistedtoken` VALUES
(1,'2026-02-11 00:46:59.252685',1),
(2,'2026-02-11 00:53:30.324291',3),
(3,'2026-02-11 00:59:36.889600',4),
(4,'2026-02-11 01:07:46.130309',6),
(5,'2026-02-12 01:55:47.438699',8),
(6,'2026-02-12 02:24:07.687551',10),
(7,'2026-02-12 02:55:54.453103',13),
(8,'2026-02-12 03:01:23.995154',14),
(9,'2026-02-17 18:10:16.807150',20),
(10,'2026-02-18 00:42:51.745593',21),
(11,'2026-02-19 23:02:14.459952',24),
(12,'2026-02-19 23:02:45.434006',23),
(13,'2026-02-19 23:36:04.071324',27),
(14,'2026-02-19 23:37:49.478209',28);
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

DROP TABLE IF EXISTS `token_blacklist_outstandingtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `jti` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outs_user_id_83bc629a_fk_users_use` (`user_id`),
  CONSTRAINT `token_blacklist_outs_user_id_83bc629a_fk_users_use` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

LOCK TABLES `token_blacklist_outstandingtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `token_blacklist_outstandingtoken` VALUES
(1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDg1NzAyMCwiaWF0IjoxNzcwNzcwNjIwLCJqdGkiOiIxZmM4NjNkYzc1OTI0NzhiYjQwNmRkODE3ZWE5YWEzZiIsInVzZXJfaWQiOiIxIn0.PaH_RMqA3nJdS-vBH5k7PwSwARsb1DpBKMuOgG3P2wA','2026-02-11 00:43:40.139358','2026-02-12 00:43:40.000000',NULL,'1fc863dc7592478bb406dd817ea9aa3f'),
(2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDg1NzIzMywiaWF0IjoxNzcwNzcwODMzLCJqdGkiOiJmN2QxYTI0ZmIxNDA0NjI0YTJiOWUwOWQyOWY5YTU2NiIsInVzZXJfaWQiOiI2In0.TUBKZlw4WJzwqzotA5PM8AEkAnDQDrW0IJe5pGbzw7M','2026-02-11 00:47:13.048476','2026-02-12 00:47:13.000000',NULL,'f7d1a24fb1404624a2b9e09d29f9a566'),
(3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDg1NzI0NCwiaWF0IjoxNzcwNzcwODQ0LCJqdGkiOiI5MTZjODlmNzlmOGE0NmE1OWE1ODA1ZTQ5MTExMjI3NCIsInVzZXJfaWQiOiI2In0.z_6BuWgaVE_s89x4jZWSUqrFRRwaf4qUSOgSdppJb6M','2026-02-11 00:47:24.315906','2026-02-12 00:47:24.000000',NULL,'916c89f79f8a46a59a5805e491112274'),
(4,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDg1NzYyMSwiaWF0IjoxNzcwNzcxMjIxLCJqdGkiOiJlYmRhNzQ0Nzc1MzM0MzFmOTFhYWZhNWNhYmUzY2Q3ZiIsInVzZXJfaWQiOiIxIn0.r1TOx0LkaRs6PpKqjzvPBendUAVEKivNG7AHnnRSl0Q','2026-02-11 00:53:41.184920','2026-02-12 00:53:41.000000',NULL,'ebda74477533431f91aafa5cabe3cd7f'),
(5,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDg1ODAwNCwiaWF0IjoxNzcwNzcxNjA0LCJqdGkiOiJlMTEzNzVjOGFkMTE0ZTA1OGE5ODQ4NWM5Y2QyZjE1ZCIsInVzZXJfaWQiOiI2In0.h02WSk-nGbunfrZvbmiWnmPOalfqBw3p_BSWwmvunfY','2026-02-11 01:00:04.151361','2026-02-12 01:00:04.000000',NULL,'e11375c8ad114e058a98485c9cd2f15d'),
(6,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDg1ODAxNSwiaWF0IjoxNzcwNzcxNjE1LCJqdGkiOiJkOTNjNmRjNmNhOTM0YjhmYjYwZjEwMGU0OWRlZjQwYiIsInVzZXJfaWQiOiI2In0.wUSgnaiv7AZbDZ0RilvqqFAu15mH_5t7ktdYYT-JpjQ','2026-02-11 01:00:15.209920','2026-02-12 01:00:15.000000',NULL,'d93c6dc6ca934b8fb60f100e49def40b'),
(7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDg1ODQ3NSwiaWF0IjoxNzcwNzcyMDc1LCJqdGkiOiIwYmRkNGIxYmMwMGU0YmQwODdiM2M3NWEwNTM0ZDU2OSIsInVzZXJfaWQiOiI3NyJ9.FE9KN3ajpXlv5aYlzhsUAFa-9NzB9aGVgd2CVqpLFUE','2026-02-11 01:07:55.022307','2026-02-12 01:07:55.000000',NULL,'0bdd4b1bc00e4bd087b3c75a0534d569'),
(8,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk0NzcyNSwiaWF0IjoxNzcwODYxMzI1LCJqdGkiOiI0ZDk2NDQ3NzI4NzU0MDgwODI0OWJjODIwNmFiODFmYyIsInVzZXJfaWQiOiIxIn0.uLKWbNLEXYkka61deGuu-8ErqspC8cxGmUpan06Pnqs','2026-02-12 01:55:25.527644','2026-02-13 01:55:25.000000',NULL,'4d964477287540808249bc8206ab81fc'),
(9,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk0Nzc1OSwiaWF0IjoxNzcwODYxMzU5LCJqdGkiOiIzOWNhNzkyYTA5MjA0ZGZlYjA4OTExMzk4ZGRhODUyOCIsInVzZXJfaWQiOiI2In0.icptsUd5FAfjMv1zh3yGhyCEFNdj1XnHeM9pawX-UHw','2026-02-12 01:55:59.919935','2026-02-13 01:55:59.000000',NULL,'39ca792a09204dfeb08911398dda8528'),
(10,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk0Nzc3MCwiaWF0IjoxNzcwODYxMzcwLCJqdGkiOiI5M2U2MzgyNzYwN2E0OTUwYjk2NTNkZTZmZmRiY2RiYiIsInVzZXJfaWQiOiI2In0.yQgPcQ6Gs5uaGTCzn_Ecd0oIhsME8aQdDuXYMvUpyqw','2026-02-12 01:56:10.171093','2026-02-13 01:56:10.000000',NULL,'93e63827607a4950b9653de6ffdbcdbb'),
(11,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk0OTQ1OCwiaWF0IjoxNzcwODYzMDU4LCJqdGkiOiIwNGIzYzY0Y2Q0ZTk0ODQwYWUwYjRhNTc5OTk4YTM2MyIsInVzZXJfaWQiOiIxIn0.fXcvER_Jko4bTJDKG2VDTBbdhS8AmDUARoWFanNvb2s','2026-02-12 02:24:18.438980','2026-02-13 02:24:18.000000',NULL,'04b3c64cd4e94840ae0b4a579998a363'),
(12,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk1MTE2MSwiaWF0IjoxNzcwODY0NzYxLCJqdGkiOiI0NTQ1ODQ1ZGRlNzU0MmQzODNiYTZjNzdkZGY4OGI2ZCIsInVzZXJfaWQiOiI5NSJ9.Z_e6fL7-uCCinpgMaNIJvenZepj3h9WdwPGwTY2K4Ic','2026-02-12 02:52:41.926366','2026-02-13 02:52:41.000000',NULL,'4545845dde7542d383ba6c77ddf88b6d'),
(13,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk1MTMxMywiaWF0IjoxNzcwODY0OTEzLCJqdGkiOiIxMzk0NWFjYmRhMGI0NDJkYjA2YjBhNDQxZDUzNzEzYSIsInVzZXJfaWQiOiIxIn0.hMWdJ4Xdiv34MvIi_hLCxhvwN_q5HrlMIzPnTHjl204','2026-02-12 02:55:13.529990','2026-02-13 02:55:13.000000',NULL,'13945acbda0b442db06b0a441d53713a'),
(14,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk1MTM2NSwiaWF0IjoxNzcwODY0OTY1LCJqdGkiOiI2YWY2NjQyYzMwMGI0MGIyODY3ZjllMDMyYTQ0ZGQ2OCIsInVzZXJfaWQiOiIxNyJ9.TIrXdhFgwMjeRaRBoR_Jld2pLY8tNgILi0fFRVfTMFk','2026-02-12 02:56:05.307854','2026-02-13 02:56:05.000000',NULL,'6af6642c300b40b2867f9e032a44dd68'),
(15,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk1MTM3NywiaWF0IjoxNzcwODY0OTc3LCJqdGkiOiJkODYyYjI3NDViNGQ0MmIyODg5MDhiYjUyZWVhNjlkMyIsInVzZXJfaWQiOiIxNyJ9.4Nrxm9tvnE9bdPINDJRv5pwpM_HUq5XPeWmI3AcVN6o','2026-02-12 02:56:17.537267','2026-02-13 02:56:17.000000',NULL,'d862b2745b4d42b288908bb52eea69d3'),
(16,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk1MjAwMCwiaWF0IjoxNzcwODY1NjAwLCJqdGkiOiI1MTc3N2U0Y2QwMTI0MzE3YTA5ODg0NzM4N2Y0OWMyMyIsInVzZXJfaWQiOiI5MiJ9.VYRqjTT7hV7x4zWzAA2TYYrlSnCpr4aHIpxMft65QIM','2026-02-12 03:06:40.635682','2026-02-13 03:06:40.000000',NULL,'51777e4cd0124317a098847387f49c23'),
(17,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTAwOTE1MiwiaWF0IjoxNzcwOTIyNzUyLCJqdGkiOiIzZWNhNmRlNDdjYzI0OGU1ODgxMWYwMmFhNDJiMGZmZiIsInVzZXJfaWQiOiIxMTkifQ.0_E92ozjILWTQuA-QLmjKC2S3CeXb8U3kWhKVCQll-E','2026-02-12 18:59:12.132705','2026-02-13 18:59:12.000000',NULL,'3eca6de47cc248e58811f02aa42b0fff'),
(18,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTM1NjUyNCwiaWF0IjoxNzcxMjcwMTI0LCJqdGkiOiI0N2U0ZTBkZjk3YzU0YTJlODA3YzdiMWQ4M2MyNTg5ZCIsInVzZXJfaWQiOiI2In0.g-5MilYPW1egkcfNk6SAoP37QPiNSTVsxDr8bwNkOc4','2026-02-16 19:28:44.746680','2026-02-17 19:28:44.000000',NULL,'47e4e0df97c54a2e807c7b1d83c2589d'),
(19,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTM2MTE2MywiaWF0IjoxNzcxMjc0NzYzLCJqdGkiOiIwMjk4MTViZTg5NmY0MzA2OGJhMjBjMzljZjFlYzBlNSIsInVzZXJfaWQiOiI2In0.mAlNLDODuHviZd-1qYJU-Fg6EU-HoyEIfQkdCJx9uu8','2026-02-16 20:46:03.705961','2026-02-17 20:46:03.000000',NULL,'029815be896f43068ba20c39cf1ec0e5'),
(20,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTM2MTE3NiwiaWF0IjoxNzcxMjc0Nzc2LCJqdGkiOiI2YzFkYjNmYjIzMjU0ZWU2OThmYjI0MjhiMjY2MjlhMiIsInVzZXJfaWQiOiI2In0.UkzOyDA_BIVP418w_YVIR2bwB31PvldiBk78vyQs5Bg','2026-02-16 20:46:16.497740','2026-02-17 20:46:16.000000',NULL,'6c1db3fb23254ee698fb2428b26629a2'),
(21,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTQ1NzAzNiwiaWF0IjoxNzcxMzcwNjM2LCJqdGkiOiI4OGI3ZTE2MWI4M2M0NGNjYjAyNGIyODE1M2U0YzVhZSIsInVzZXJfaWQiOiIxNDEifQ.1ohG0wpLWkWwV4ww0LMgsI89Y0G_Fg2SdAkIeZyhxVk','2026-02-17 23:23:56.597785','2026-02-18 23:23:56.000000',NULL,'88b7e161b83c44ccb024b28153e4c5ae'),
(22,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTQ2MTc4OSwiaWF0IjoxNzcxMzc1Mzg5LCJqdGkiOiI0NTE5M2FiMDhkNDc0YTMyYTM0YjZmMTJkNjQwMGI4MyIsInVzZXJfaWQiOiIxNDUifQ.3jJ9Qtw4jh41xoe0-Urjia-JfGLie4xfDZryIyCapKs','2026-02-18 00:43:09.579297','2026-02-19 00:43:09.000000',NULL,'45193ab08d474a32a34b6f12d6400b83'),
(23,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTU1NjAzMiwiaWF0IjoxNzcxNDY5NjMyLCJqdGkiOiIwZGYzNGQ5ZWI1ZmY0YzFhOTNiNWM5OTAyYzYwN2JkOCIsInVzZXJfaWQiOiIxIn0.wea0lo3PJS6hRvVp_2tJitsqGJGl2MKxf14JpLmBp9c','2026-02-19 02:53:52.515907','2026-02-20 02:53:52.000000',NULL,'0df34d9eb5ff4c1a93b5c9902c607bd8'),
(24,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTYyODE5NSwiaWF0IjoxNzcxNTQxNzk1LCJqdGkiOiJmNGYyZmFmYmUwMTc0ZjhmYTM5NmUyMDdiN2M2NjA1ZCIsInVzZXJfaWQiOiIxNDUifQ.etUAKWQFZ_4q0b8yaPJqruVRW_9T1BHoLLDojXRYXFY','2026-02-19 22:56:35.016004','2026-02-20 22:56:35.000000',NULL,'f4f2fafbe0174f8fa396e207b7c6605d'),
(25,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTYyODU0NiwiaWF0IjoxNzcxNTQyMTQ2LCJqdGkiOiJlNjUxZjNhZTZmZTI0OTg0OTdkNTczYjIxZWY0ZTRlMSIsInVzZXJfaWQiOiIxNDYifQ.25sWvBwUSfTtCedVTqZITNRzMayUsf3POquGh0xWbE4','2026-02-19 23:02:26.144395','2026-02-20 23:02:26.000000',NULL,'e651f3ae6fe2498497d573b21ef4e4e1'),
(26,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTYyODU3MiwiaWF0IjoxNzcxNTQyMTcyLCJqdGkiOiI3YWY3ODM2MGU1N2U0NTg2YTczOTEzMDA5NWE5M2IwYSIsInVzZXJfaWQiOiIxNDYifQ.vq6v-iE8LpTsvpJdJ88mQEk0iZlfzEvpMCdGrAxnftk','2026-02-19 23:02:52.436724','2026-02-20 23:02:52.000000',NULL,'7af78360e57e4586a739130095a93b0a'),
(27,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTYzMDM5OSwiaWF0IjoxNzcxNTQzOTk5LCJqdGkiOiJiMWNjZmY4YmY3ZTY0ZTU0YjUyMjhkNWZhYTcxMWIwMCIsInVzZXJfaWQiOiIxNDYifQ.YSE-3Jg64kmjIa37W5j3KEP0UZIKc_e9Vx3Uf2tKu4k','2026-02-19 23:33:19.418603','2026-02-20 23:33:19.000000',NULL,'b1ccff8bf7e64e54b5228d5faa711b00'),
(28,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTYzMDU3NywiaWF0IjoxNzcxNTQ0MTc3LCJqdGkiOiJkYzA4NzNkMGQ2ZWQ0NGNiODYxZTNkZjRhNjg2YzkwYiIsInVzZXJfaWQiOiIxNDYifQ.sjpaNN9e02s9ffgnTMNQMGK_i6QrxeQDh6jwyVGxoFU','2026-02-19 23:36:17.831948','2026-02-20 23:36:17.000000',NULL,'dc0873d0d6ed44cb861e3df4a686c90b'),
(29,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTYzMDc0OSwiaWF0IjoxNzcxNTQ0MzQ5LCJqdGkiOiIxODdiNjNmM2IzOTU0MGJjYjdmOTI0Njg0YTk4ODRjZCIsInVzZXJfaWQiOiIxNDYifQ.9VkksxyAVQnq9OweDtbx_HjuC7wniIKK7iPwkJlTM2w','2026-02-19 23:39:09.020764','2026-02-20 23:39:09.000000',NULL,'187b63f3b39540bcb7f924684a9884cd'),
(30,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTYzMjk1MywiaWF0IjoxNzcxNTQ2NTUzLCJqdGkiOiJlZjE2NDY0MWJkZDA0MzY3OTM5M2M1NGM1YzZhNmI3NyIsInVzZXJfaWQiOiIxNDYifQ.SLHUvsmM66DuszbIs8vsa6H2IYxiOrzH1qzrjF9ECH4','2026-02-20 00:15:53.011645','2026-02-21 00:15:53.000000',NULL,'ef164641bdd043679393c54c5c6a6b77'),
(31,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTcxNzMyNiwiaWF0IjoxNzcxNjMwOTI2LCJqdGkiOiI1NDEwMjg5ZGVhNmU0YzU1YjZlMDg4YWFjZDQwOTE4OCIsInVzZXJfaWQiOiIxNDYifQ.VRBcaBv1LtbE7XcQL8Bvr5TgMJUS1wgvR9Mq9XAgUz8','2026-02-20 23:42:06.450915','2026-02-21 23:42:06.000000',NULL,'5410289dea6e4c55b6e088aacd409188');
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` ENABLE KEYS */;
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
  `ine_tutor` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_tutoradm_nombre_completo` (`apellido_paterno`,`apellido_materno`,`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tutores`
--

LOCK TABLES `tutores` WRITE;
/*!40000 ALTER TABLE `tutores` DISABLE KEYS */;
set autocommit=0;
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
  `role` varchar(50) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) DEFAULT NULL,
  `mfa_code` varchar(6) DEFAULT NULL,
  `mfa_expires_at` datetime(6) DEFAULT NULL,
  `is_staff` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=148 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user`
--

LOCK TABLES `users_user` WRITE;
/*!40000 ALTER TABLE `users_user` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `users_user` VALUES
(147,'pbkdf2_sha256$1200000$LevDcdWXOCSTxnFvqw2x3L$KfZll/e9i7OcMV/qv8Sm0cjhDwp1YrznnjC0kSB6m4w=','2026-02-21 00:14:19.019709','hectorino2789@gmail.com','','administrador',1,1,'adancito',NULL,NULL,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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

-- Dump completed on 2026-02-20 18:41:13
