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
-- Table structure for table `adeudos`
--

DROP TABLE IF EXISTS `adeudos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `adeudos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `monto_base` decimal(10,2) NOT NULL,
  `descuento_aplicado` decimal(10,2) NOT NULL,
  `monto_final` decimal(10,2) NOT NULL,
  `recargo_aplicado` decimal(10,2) NOT NULL,
  `monto_total` decimal(10,2) NOT NULL,
  `fecha_generacion` date NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `estatus` varchar(50) NOT NULL,
  `monto_pagado` decimal(10,2) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_actualizacion` datetime(6) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `concepto_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_adeudo_estudiante` (`estudiante_id`),
  KEY `idx_adeudo_concepto` (`concepto_id`),
  KEY `idx_adeudo_vencimiento` (`fecha_vencimiento`),
  KEY `idx_adeudo_estatus` (`estatus`),
  KEY `idx_adeudo_seguimiento` (`estudiante_id`,`concepto_id`,`fecha_generacion`),
  CONSTRAINT `adeudos_concepto_id_de3b7d87_fk_conceptos_pago_id` FOREIGN KEY (`concepto_id`) REFERENCES `conceptos_pago` (`id`),
  CONSTRAINT `adeudos_estudiante_id_83cfd3e8_fk_estudiantes_matricula` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiantes` (`matricula`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adeudos`
--

LOCK TABLES `adeudos` WRITE;
/*!40000 ALTER TABLE `adeudos` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `adeudos` VALUES
(1,5000.00,1000.00,4000.00,0.00,4000.00,'2026-01-01','2026-01-15','parcial',2000.00,'2026-01-11 07:45:04.648303','2026-01-11 07:45:04.648327',220548,1);
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `asistencia_cafeteria_estudiante_id_fecha_asis_ff254b5c_uniq` (`estudiante_id`,`fecha_asistencia`,`tipo_comida`),
  KEY `idx_cafeteria_estudiante` (`estudiante_id`),
  KEY `idx_cafeteria_fecha` (`fecha_asistencia`),
  CONSTRAINT `asistencia_cafeteria_estudiante_id_3911c454_fk_estudiant` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiantes` (`matricula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
(76,'Can view Pago',19,'view_pago');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `conceptos_pago_nombre_nivel_educativo_8f94b81a_uniq` (`nombre`,`nivel_educativo`),
  KEY `idx_concepto_activo` (`activo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conceptos_pago`
--

LOCK TABLES `conceptos_pago` WRITE;
/*!40000 ALTER TABLE `conceptos_pago` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `conceptos_pago` VALUES
(1,'Colegiatura Enero','Colegiatura del mes de enero',5000.00,'Universidad',1);
/*!40000 ALTER TABLE `conceptos_pago` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_admin_log` VALUES
(1,'2026-01-11 08:56:33.045437','2','PEPE EL PIYO Sanchez Pedroza',1,'[{\"added\": {}}]',15,3),
(2,'2026-01-11 08:56:41.414330','220548','220548 - HECTOR ADAN HURTADO',2,'[{\"added\": {\"name\": \"Estudiante-Tutor\", \"object\": \"220548 - HECTOR ADAN HURTADO -> PEPE EL PIYO Sanchez Pedroza (padre)\"}}]',9,3),
(3,'2026-01-11 08:58:15.974461','2','A (10%) (10%)',1,'[{\"added\": {}}]',8,3),
(4,'2026-01-11 08:58:32.435480','2','A (10.00%)',2,'[{\"changed\": {\"fields\": [\"Nombre\"]}}]',8,3),
(5,'2026-01-11 08:59:30.986139','2','[+] Evaluación 220548 - HECTOR ADAN HURTADO - Pendiente',1,'[{\"added\": {}}]',11,3);
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
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_content_type` VALUES
(2,'admin','logentry'),
(3,'auth','group'),
(4,'auth','permission'),
(16,'comedor','asistenciacafeteria'),
(5,'contenttypes','contenttype'),
(7,'estudiantes','estadoestudiante'),
(8,'estudiantes','estrato'),
(9,'estudiantes','estudiante'),
(10,'estudiantes','estudiantetutor'),
(11,'estudiantes','evaluacionsocioeconomica'),
(12,'estudiantes','grado'),
(13,'estudiantes','grupo'),
(14,'estudiantes','historialestadosestudiante'),
(15,'estudiantes','tutor'),
(17,'pagos','adeudo'),
(18,'pagos','conceptopago'),
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
(26,'estudiantes','0003_remove_tutor_idx_tutor_ultima_actualizacion_and_more','2026-01-11 08:05:11.228459');
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
('ma4zf92ag8wz6y27a8ku0n4ycf8yuhi6','.eJxVjMsOwiAQRf-FtSGFysule7-BzDCDVA0kpV0Z_92QdKHbe865bxFh30rcO69xIXERszj9bgjpyXUAekC9N5la3dYF5VDkQbu8NeLX9XD_Dgr0MmoNQSUINin03jsCnRGVYzRmziYrjZQsJRPIoIaJ2ejJzs568O6MLD5fBhs4lQ:1verBc:WrN3QPx-lk7alNXi8Aeka5qT-moC742T18lVWw3KsbY','2026-01-25 08:52:36.278559');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estados_estudiante`
--

LOCK TABLES `estados_estudiante` WRITE;
/*!40000 ALTER TABLE `estados_estudiante` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `estados_estudiante` VALUES
(1,'Activo','Estudiante inscrito y activo',1);
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `idx_estrato_activo` (`activo`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estratos`
--

LOCK TABLES `estratos` WRITE;
/*!40000 ALTER TABLE `estratos` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `estratos` VALUES
(1,'B','Estrato medio con descuento del 20%',20.00,1),
(2,'A','Estrato no tan mal',10.00,1);
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
(220548,'MARIANA','FLOWERS','KRAKOV','CHUY MARRY',1,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estudiantes_tutores`
--

LOCK TABLES `estudiantes_tutores` WRITE;
/*!40000 ALTER TABLE `estudiantes_tutores` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `estudiantes_tutores` VALUES
(1,'Madre','2026-01-11 07:45:04.637533',1,220548,1),
(2,'padre','2026-01-11 08:56:41.413232',1,220548,2);
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
  PRIMARY KEY (`id`),
  KEY `evaluaciones_socioeconomicas_estrato_id_d58b0b82_fk_estratos_id` (`estrato_id`),
  KEY `idx_evalsocio_estudiante` (`estudiante_matricula`),
  KEY `idx_evalsocio_fecha` (`fecha_evaluacion`),
  KEY `idx_evalsocio_aprobado` (`aprobado`),
  CONSTRAINT `evaluaciones_socioec_estudiante_matricula_0ebd0a32_fk_estudiant` FOREIGN KEY (`estudiante_matricula`) REFERENCES `estudiantes` (`matricula`),
  CONSTRAINT `evaluaciones_socioeconomicas_estrato_id_d58b0b82_fk_estratos_id` FOREIGN KEY (`estrato_id`) REFERENCES `estratos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluaciones_socioeconomicas`
--

LOCK TABLES `evaluaciones_socioeconomicas` WRITE;
/*!40000 ALTER TABLE `evaluaciones_socioeconomicas` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `evaluaciones_socioeconomicas` VALUES
(1,'2026-01-11 07:45:04.629659',15000.00,'Propia',4,'{}',1,'2026-01-11 07:45:04.629767',1,220548),
(2,'2026-01-11 08:59:30.985196',40000.00,'Adobe',3,'Unos cuantos documentos.',NULL,'2026-01-11 08:59:30.985264',2,220548);
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `grados_nombre_nivel_de2afc70_uniq` (`nombre`,`nivel`),
  KEY `idx_grado_nombre_nivel` (`nombre`,`nivel`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grados`
--

LOCK TABLES `grados` WRITE;
/*!40000 ALTER TABLE `grados` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `grados` VALUES
(1,'10','Universidad');
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
  `descripcion` varchar(255) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `grado_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `grupos_nombre_generacion_grado_id_a25c634a_uniq` (`nombre`,`generacion`,`grado_id`),
  KEY `idx_grupo_grado` (`grado_id`),
  CONSTRAINT `grupos_grado_id_7d47e77c_fk_grados_id` FOREIGN KEY (`grado_id`) REFERENCES `grados` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupos`
--

LOCK TABLES `grupos` WRITE;
/*!40000 ALTER TABLE `grupos` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `grupos` VALUES
(1,'IRIC','2022-2026','REDES','2026-01-11 10:30:00.000000',1);
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
  PRIMARY KEY (`id`),
  KEY `idx_historialestado_estudiante` (`estudiante_matricula`),
  KEY `idx_historialestado_estado` (`estado_id`),
  CONSTRAINT `historial_estados_es_estado_id_70112f90_fk_estados_e` FOREIGN KEY (`estado_id`) REFERENCES `estados_estudiante` (`id`),
  CONSTRAINT `historial_estados_es_estudiante_matricula_32e02065_fk_estudiant` FOREIGN KEY (`estudiante_matricula`) REFERENCES `estudiantes` (`matricula`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_estados_estudiante`
--

LOCK TABLES `historial_estados_estudiante` WRITE;
/*!40000 ALTER TABLE `historial_estados_estudiante` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `historial_estados_estudiante` VALUES
(1,'Inscripción inicial','2026-01-11 07:45:04.620118',1,220548);
/*!40000 ALTER TABLE `historial_estados_estudiante` ENABLE KEYS */;
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
  CONSTRAINT `pagos_adeudo_id_14279390_fk_adeudos_id` FOREIGN KEY (`adeudo_id`) REFERENCES `adeudos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tutores`
--

LOCK TABLES `tutores` WRITE;
/*!40000 ALTER TABLE `tutores` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `tutores` VALUES
(1,'Maria Actualizada','Garcia','Lopez','+52 449 888 8888','updated@ejemplo.com'),
(2,'PEPE EL PIYO','Sanchez','Pedroza','449 405 26 64','maracas@gmail.com');
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
  `is_staff` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user`
--

LOCK TABLES `users_user` WRITE;
/*!40000 ALTER TABLE `users_user` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `users_user` VALUES
(1,'pbkdf2_sha256$1200000$N5nLwJcWjCHRqXHcv3T5fZ$N21xPc2w6yBnq1RVmd1DRY8Y6DwDbW8SkmZS4H8S/+k=',NULL,'adancpphack@gmail.com','HECTOR ADAN','estudiante',1,0,0,'adan'),
(2,'pbkdf2_sha256$1200000$ORhQAJ45Xrhh5pYt6GWHJO$vnRHx23zbJMRxOETEISvzFzeuRBHZDqgmiuzcyOMDIA=',NULL,'hectorio@school.admin','','administrador',1,1,1,'hectorio'),
(3,'pbkdf2_sha256$1200000$itrGCgjnBvZYVrNJ4BAy2O$1V/OS1OU5sd0BpacYfmK2lNCA28v2ifXLxKma3VwQOI=','2026-01-11 08:52:36.275488','hectorino2789@gmail.com','','administrador',1,1,1,'hectorio23');
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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-01-12 13:03:54
