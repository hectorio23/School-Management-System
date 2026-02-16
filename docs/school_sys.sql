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
) ENGINE=InnoDB AUTO_INCREMENT=366 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adeudos`
--

LOCK TABLES `adeudos` WRITE;
/*!40000 ALTER TABLE `adeudos` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `adeudos` VALUES
(342,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pagado',1000,42,1500.00,1,NULL,NULL,NULL,0,0,0,0,'CONCEPTO DE PAGO'),
(343,1500.00,900.00,0.00,600.00,'2026-02-12','2026-03-10','pendiente',1001,42,0.00,1,NULL,NULL,NULL,0,0,0,0,'CONCEPTO DE PAGO'),
(344,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pagado',20240000,43,1500.00,1,NULL,NULL,NULL,0,0,0,0,'CONCEPTO DE PAGO'),
(345,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pagado',20240001,43,1500.00,1,NULL,NULL,NULL,0,0,0,0,'CONCEPTO DE PAGO'),
(346,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pagado',20240002,43,1500.00,1,NULL,NULL,NULL,0,0,0,0,'CONCEPTO DE PAGO'),
(347,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pagado',20240003,43,1500.00,1,NULL,NULL,NULL,0,0,0,0,'CONCEPTO DE PAGO'),
(348,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pagado',20240004,43,1500.00,1,NULL,NULL,NULL,0,0,0,0,'CONCEPTO DE PAGO'),
(349,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pagado',20240005,43,1500.00,1,NULL,NULL,NULL,0,0,0,0,'CONCEPTO DE PAGO'),
(350,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pagado',20240006,43,1500.00,1,NULL,NULL,NULL,0,0,0,0,'CONCEPTO DE PAGO'),
(351,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pagado',20240007,43,1500.00,1,NULL,NULL,NULL,0,0,0,0,'CONCEPTO DE PAGO'),
(352,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pagado',20240008,43,1500.00,1,NULL,NULL,NULL,0,0,0,0,'CONCEPTO DE PAGO'),
(353,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pagado',20240009,43,1500.00,1,NULL,NULL,NULL,0,0,0,0,'CONCEPTO DE PAGO'),
(354,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pendiente',20240000,45,0.00,1,NULL,NULL,'2026-02-01',0,0,0,0,'CONCEPTO DE PAGO'),
(355,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pendiente',20240001,45,0.00,1,NULL,NULL,'2026-02-01',0,0,0,0,'CONCEPTO DE PAGO'),
(356,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pendiente',20240002,45,0.00,1,NULL,NULL,'2026-02-01',0,0,0,0,'CONCEPTO DE PAGO'),
(357,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pendiente',20240003,45,0.00,1,NULL,NULL,'2026-02-01',0,0,0,0,'CONCEPTO DE PAGO'),
(358,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pendiente',20240004,45,0.00,1,NULL,NULL,'2026-02-01',0,0,0,0,'CONCEPTO DE PAGO'),
(359,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pendiente',20240005,45,0.00,1,NULL,NULL,'2026-02-01',0,0,0,0,'CONCEPTO DE PAGO'),
(360,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pendiente',20240006,45,0.00,1,NULL,NULL,'2026-02-01',0,0,0,0,'CONCEPTO DE PAGO'),
(361,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pendiente',20240007,45,0.00,1,NULL,NULL,'2026-02-01',0,0,0,0,'CONCEPTO DE PAGO'),
(362,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pendiente',20240008,45,0.00,1,NULL,NULL,'2026-02-01',0,0,0,0,'CONCEPTO DE PAGO'),
(363,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-10','pendiente',20240009,45,0.00,1,NULL,NULL,'2026-02-01',0,0,0,0,'CONCEPTO DE PAGO'),
(364,1500.00,0.00,0.00,1500.00,'2026-02-12','2026-03-06','pendiente',1000,47,0.00,1,NULL,'Reinscripción automática - Ciclo CI-2024-2025',NULL,0,0,0,0,'CONCEPTO DE PAGO'),
(365,1500.00,900.00,0.00,600.00,'2026-02-12','2026-03-06','pendiente',1001,47,0.00,1,NULL,'Reinscripción automática - Ciclo CI-2024-2025',NULL,0,0,0,0,'CONCEPTO DE PAGO');
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
  `nivel_educativo_id` bigint(20) NOT NULL,
  `usuario_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  KEY `idx_adminesc_usuario` (`usuario_id`),
  KEY `idx_adminesc_nivel` (`nivel_educativo_id`),
  KEY `idx_adminesc_activo` (`activo`),
  CONSTRAINT `administradores_esco_nivel_educativo_id_5ec1c090_fk_niveles_e` FOREIGN KEY (`nivel_educativo_id`) REFERENCES `niveles_educativos` (`id`),
  CONSTRAINT `administradores_escolares_usuario_id_7f44c32b_fk_users_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asignaciones_maestro`
--

LOCK TABLES `asignaciones_maestro` WRITE;
/*!40000 ALTER TABLE `asignaciones_maestro` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `asignaciones_maestro` VALUES
(2,'2026-02-12',1,'2026-02-12 18:57:09.342710','2026-02-12 18:57:23.819043',25,292,5,2),
(3,'2026-02-12',1,'2026-02-13 04:35:26.061896','2026-02-13 04:35:26.061926',27,357,6,3);
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
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `curp` (`curp`),
  KEY `idx_aspirante_curp` (`curp`),
  KEY `idx_aspirante_fase` (`fase_actual`),
  CONSTRAINT `aspirantes_user_id_7887eb14_fk_usuarios_aspirantes_folio` FOREIGN KEY (`user_id`) REFERENCES `usuarios_aspirantes` (`folio`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=205 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
(204,'Can view Outstanding Token',51,'view_outstandingtoken');
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `becas_estudiantes`
--

LOCK TABLES `becas_estudiantes` WRITE;
/*!40000 ALTER TABLE `becas_estudiantes` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `becas_estudiantes` VALUES
(13,'2026-02-12 18:05:34.136113',NULL,1,'',NULL,1,1000);
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calificaciones`
--

LOCK TABLES `calificaciones` WRITE;
/*!40000 ALTER TABLE `calificaciones` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `calificaciones` VALUES
(4,10.00,0,'2026-02-12 18:58:05.330396','2026-02-12 19:00:48.786590',2,NULL,1000,5,NULL,2),
(5,9.00,0,'2026-02-13 04:35:26.074851','2026-02-13 04:39:23.129685',3,NULL,20240000,6,NULL,3),
(6,7.00,0,'2026-02-13 04:35:26.080670','2026-02-13 04:39:23.143534',3,NULL,20240001,6,NULL,3),
(7,6.00,0,'2026-02-13 04:35:26.086160','2026-02-13 04:39:23.149797',3,NULL,20240002,6,NULL,3),
(8,10.00,0,'2026-02-13 04:35:26.092296','2026-02-13 04:39:23.156951',3,NULL,20240003,6,NULL,3),
(9,10.00,0,'2026-02-13 04:35:26.098369','2026-02-13 04:39:23.161786',3,NULL,20240004,6,NULL,3),
(10,8.00,0,'2026-02-13 04:35:26.104225','2026-02-13 04:39:23.166381',3,NULL,20240005,6,NULL,3),
(11,9.00,0,'2026-02-13 04:35:26.110217','2026-02-13 04:39:23.172119',3,NULL,20240006,6,NULL,3),
(12,7.00,0,'2026-02-13 04:35:26.116516','2026-02-13 04:39:23.176885',3,NULL,20240007,6,NULL,3),
(13,8.00,0,'2026-02-13 04:35:26.122466','2026-02-13 04:39:23.180986',3,NULL,20240008,6,NULL,3),
(14,6.00,0,'2026-02-13 04:35:26.128559','2026-02-13 04:39:23.187100',3,NULL,20240009,6,NULL,3);
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
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ciclos_escolares`
--

LOCK TABLES `ciclos_escolares` WRITE;
/*!40000 ALTER TABLE `ciclos_escolares` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `ciclos_escolares` VALUES
(25,'2026-2027','2026-02-12','2027-02-12',0,'2026-02-12 17:47:16.737056','2026-02-12 17:47:16.737096'),
(26,'2027-2028','2027-02-12','2028-02-12',0,'2026-02-12 19:03:03.706103','2026-02-12 19:03:03.706160'),
(27,'CI-2024-2025','2024-08-01','2025-07-15',1,'2026-02-13 04:16:30.352718','2026-02-13 04:16:30.352746');
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
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conceptos_pago`
--

LOCK TABLES `conceptos_pago` WRITE;
/*!40000 ALTER TABLE `conceptos_pago` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `conceptos_pago` VALUES
(42,'Reinscripción Primaria Automática','',1500.00,'Primaria',1,'reinscripcion'),
(43,'Mensualidad Septiembre','Pago de mensualidad de septiembre',1500.00,'PRIMARIA',1,'colegiatura'),
(44,'Colegiatura Febrero 2026','Colegiatura mensual correspondiente a Febrero 2026',0.00,'Preescolar',1,'colegiatura'),
(45,'Colegiatura Febrero 2026','Colegiatura mensual correspondiente a Febrero 2026',1500.00,'Primaria',1,'colegiatura'),
(46,'Colegiatura Febrero 2026','Colegiatura mensual correspondiente a Febrero 2026',0.00,'Secundaria',1,'colegiatura'),
(47,'Reinscripción CI-2024-2025','Pago de reinscripción para el ciclo CI-2024-2025',1500.00,'Todos',1,'reinscripcion');
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
) ENGINE=InnoDB AUTO_INCREMENT=1202 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
(669,'2026-01-27 23:51:19.591869','1001','1001 - FLORENCIO MOHAMED',2,'[]',9,6),
(670,'2026-01-28 22:22:07.388887','35','2001 - Apellido AspiranteTest',3,'',29,6),
(671,'2026-01-28 22:22:07.388969','34','2000 - None AspiranteTest',3,'',29,6),
(672,'2026-01-28 22:26:09.259939','36','2002 - Apellido AspiranteTest',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',29,6),
(673,'2026-01-28 22:27:37.788399','36','2002 - Apellido AspiranteTest',2,'[{\"changed\": {\"fields\": [\"Status\", \"Acta nacimiento\"]}}]',29,6),
(674,'2026-01-28 23:35:31.882815','41','2007 - Apellido AspiranteTest',2,'[{\"changed\": {\"fields\": [\"Fecha visita domiciliaria\"]}}]',29,6),
(675,'2026-01-28 23:36:29.882942','41','2007 - Apellido AspiranteTest',2,'[{\"changed\": {\"fields\": [\"Fecha entrevista psicologia\"]}}]',29,6),
(676,'2026-01-30 19:53:55.079610','45','1001 - FLORENCIO MOHAMED - 2026-01-30 (Desayuno)',1,'[{\"added\": {}}]',16,6),
(677,'2026-01-30 19:54:16.726254','45','1001 - FLORENCIO MOHAMED - 2026-01-30 (Desayuno)',3,'',16,6),
(678,'2026-01-30 20:02:17.606321','46','1001 - FLORENCIO MOHAMED - 2026-01-30 (Desayuno)',1,'[{\"added\": {}}]',16,6),
(679,'2026-01-30 21:59:33.440423','1','1001 - FLORENCIO MOHAMED - $10.00 (PENDIENTE)',3,'',35,6),
(680,'2026-01-30 22:16:00.282804','48','1001 - FLORENCIO MOHAMED - 2026-01-30 (Comida)',1,'[{\"added\": {}}]',16,6),
(681,'2026-01-30 22:24:07.669827','81','Pago $13.50 - 2026-01-30',1,'[{\"added\": {}}]',19,6),
(682,'2026-02-02 22:02:33.644135','77','bandit@test.com (Estudiante)',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',1,6),
(683,'2026-02-02 22:11:01.494371','1','adancpphack@gmail.com (Estudiante)',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',1,6),
(684,'2026-02-02 22:11:50.301030','6','hectorino2789@gmail.com (administrador)',2,'[{\"changed\": {\"fields\": [\"Nombre\", \"Role\"]}}]',1,6),
(685,'2026-02-02 22:12:00.901112','1','adancpphack@gmail.com (estudiante)',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',1,6),
(686,'2026-02-02 22:12:10.963396','77','bandit@test.com (estudiante)',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',1,6),
(687,'2026-02-02 22:22:03.454671','314','1001 - FLORENCIO MOHAMED - Consumo Cafeteria - Todos ($136.0000)',2,'[{\"changed\": {\"fields\": [\"Fecha vencimiento\"]}}]',17,6),
(688,'2026-02-03 22:38:15.328337','82','Pago $136.00 - 2026-02-03',1,'[{\"added\": {}}]',19,6),
(689,'2026-02-03 22:38:38.376804','83','Pago $10.00 - 2026-02-03',1,'[{\"added\": {}}]',19,6),
(690,'2026-02-03 22:38:59.732440','1001','1001 - FLORENCIO MOHAMED',2,'[{\"changed\": {\"name\": \"Inscripci\\u00f3n\", \"object\": \"1001 - FLORENCIO MOHAMED - 3\\u00b0A - Preescolar (activo)\", \"fields\": [\"Ciclo escolar\"]}}]',9,6),
(691,'2026-02-03 22:39:10.680106','1000','1000 - ARRON ADRIAN SOMALI',2,'[{\"changed\": {\"name\": \"Inscripci\\u00f3n\", \"object\": \"1000 - ARRON ADRIAN SOMALI - 5\\u00b0A - Primaria (activo)\", \"fields\": [\"Ciclo escolar\"]}}]',9,6),
(692,'2026-02-03 22:39:50.034243','1002','1002 - ESTUDIANTE TEST',2,'[{\"added\": {\"name\": \"Inscripci\\u00f3n\", \"object\": \"1002 - ESTUDIANTE TEST - 1\\u00b0B - Preescolar (activo)\"}}]',9,6),
(693,'2026-02-03 22:42:06.458356','91','admin_testing@school.com (becas_admin)',2,'[{\"changed\": {\"fields\": [\"Nombre\", \"Role\"]}}]',1,6),
(694,'2026-02-03 22:48:30.541986','51','1000 - ARRON ADRIAN SOMALI - 2026-02-03 (Comida)',1,'[{\"added\": {}}]',16,6),
(695,'2026-02-03 22:51:44.072832','7','2026-2027 ',1,'[{\"added\": {}}]',31,6),
(696,'2026-02-03 22:59:38.633671','7','2026-2027 [ACTIVO]',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(697,'2026-02-03 22:59:38.635696','6','2025-2026 ',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',31,6),
(698,'2026-02-04 20:43:17.944910','91','admin_testing@school.com (administrador)',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',1,6),
(699,'2026-02-04 20:57:02.982960','91','admin_testing@school.com (comedor_admin)',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',1,6),
(700,'2026-02-04 20:57:31.102222','91','admin_testing@school.com (admisiones_admin)',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',1,6),
(701,'2026-02-04 23:18:13.094727','55','1001 - FLORENCIO MOHAMED - 2026-02-04 (Desayuno)',1,'[{\"added\": {}}]',16,6),
(702,'2026-02-05 01:25:18.765229','91','admin_testing@school.com (estudiante)',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',1,6),
(703,'2026-02-05 01:25:57.967307','91','admin_testing@school.com (finanzas_admin)',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',1,6),
(704,'2026-02-05 03:21:44.809909','91','admin_testing@school.com (becas_admin)',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',1,6),
(705,'2026-02-05 03:22:26.088326','91','admin_testing@school.com (administrador)',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',1,6),
(706,'2026-02-05 03:22:50.745397','91','admin_testing@school.com (comedor_admin)',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',1,6),
(707,'2026-02-12 03:06:33.799000','92','student_test_final@school.com (estudiante)',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',1,6),
(708,'2026-02-12 17:37:48.236049','3','Autorización 3 - 99988886 - Juanito Perez - 10.00',3,'',38,6),
(709,'2026-02-12 17:37:48.236143','2','Autorización 2 - 99988885 - Juanito Perez - 10.00',3,'',38,6),
(710,'2026-02-12 17:37:48.236202','1','Autorización 1 - 99988884 - Juanito Perez - 10.00',3,'',38,6),
(711,'2026-02-12 17:38:29.523591','3','99988886 - Juanito Perez - 10.00',3,'',39,6),
(712,'2026-02-12 17:38:29.523660','2','99988885 - Juanito Perez - 10.00',3,'',39,6),
(713,'2026-02-12 17:38:29.523705','1','99988884 - Juanito Perez - 10.00',3,'',39,6),
(714,'2026-02-12 17:38:53.526065','1','Profesor X Y - Matemáticas I (MAT-1P-TEST) (1A_TESTA_TEST (2025-2026-TEST))',3,'',37,6),
(715,'2026-02-12 17:39:06.048176','3','99988886 - Juanito Perez - Matemáticas I (MAT-1P-TEST) - AO',3,'',40,6),
(716,'2026-02-12 17:39:06.048266','2','99988885 - Juanito Perez - Matemáticas I (MAT-1P-TEST) - AO',3,'',40,6),
(717,'2026-02-12 17:39:06.048320','1','99988884 - Juanito Perez - Matemáticas I (MAT-1P-TEST) - AO',3,'',40,6),
(718,'2026-02-12 17:39:15.066185','1','Matemáticas I (MAT-1P-TEST)',3,'',42,6),
(719,'2026-02-12 17:39:46.884335','1','Parcial 1 - 2025-2026-TEST [ACTIVO]',3,'',44,6),
(720,'2026-02-12 17:40:05.962222','57','2015 - MIGRACION JUAN',3,'',29,6),
(721,'2026-02-12 17:40:05.962310','48','2014 - Perez Juan',3,'',29,6),
(722,'2026-02-12 17:40:05.962363','47','2013 - TEST ASPIRANTE ACTUALIZADO',3,'',29,6),
(723,'2026-02-12 17:40:05.962408','46','2012 - TEST ASPIRANTE ACTUALIZADO',3,'',29,6),
(724,'2026-02-12 17:40:05.962450','45','2011 - TEST ASPIRANTE',3,'',29,6),
(725,'2026-02-12 17:40:05.962492','44','2010 - TEST ASPIRANTE',3,'',29,6),
(726,'2026-02-12 17:40:05.962533','43','2009 - Apellido AspiranteTest',3,'',29,6),
(727,'2026-02-12 17:40:05.962574','42','2008 - Apellido AspiranteTest',3,'',29,6),
(728,'2026-02-12 17:40:05.962616','41','2007 - Apellido AspiranteTest',3,'',29,6),
(729,'2026-02-12 17:40:05.962658','40','2006 - Apellido AspiranteTest',3,'',29,6),
(730,'2026-02-12 17:40:05.962699','39','2005 - Apellido AspiranteTest',3,'',29,6),
(731,'2026-02-12 17:40:05.962740','38','2004 - Apellido AspiranteTest',3,'',29,6),
(732,'2026-02-12 17:40:05.962780','37','2003 - Apellido AspiranteTest',3,'',29,6),
(733,'2026-02-12 17:40:05.962821','36','2002 - Apellido AspiranteTest',3,'',29,6),
(734,'2026-02-12 17:40:17.425274','42','DE PRUEBA PADRE',3,'',26,6),
(735,'2026-02-12 17:40:17.425359','41','Paterno2 Materno2 Tutor Dos',3,'',26,6),
(736,'2026-02-12 17:40:17.425409','40','Paterno Materno Tutor Uno',3,'',26,6),
(737,'2026-02-12 17:40:17.425452','39','Paterno2 Materno2 Tutor Dos',3,'',26,6),
(738,'2026-02-12 17:40:17.425492','38','Paterno Materno Tutor Uno',3,'',26,6),
(739,'2026-02-12 17:40:17.425533','37','Paterno2 Materno2 Tutor Dos',3,'',26,6),
(740,'2026-02-12 17:40:17.425574','36','Paterno Materno Tutor Uno',3,'',26,6),
(741,'2026-02-12 17:40:17.425614','35','Paterno2 Materno2 Tutor Dos',3,'',26,6),
(742,'2026-02-12 17:40:17.425661','34','Paterno Materno Tutor Uno',3,'',26,6),
(743,'2026-02-12 17:40:17.425723','33','Paterno2 Materno2 Tutor Dos',3,'',26,6),
(744,'2026-02-12 17:40:17.425788','32','Paterno Materno Tutor Uno',3,'',26,6),
(745,'2026-02-12 17:40:17.425849','31','Paterno2 Materno2 Tutor Dos',3,'',26,6),
(746,'2026-02-12 17:40:17.425911','30','Paterno Materno Tutor Uno',3,'',26,6),
(747,'2026-02-12 17:40:17.425952','29','Paterno2 Materno2 Tutor Dos',3,'',26,6),
(748,'2026-02-12 17:40:17.426013','28','Paterno Materno Tutor Uno',3,'',26,6),
(749,'2026-02-12 17:40:17.426055','27','Paterno2 Materno2 Tutor Dos',3,'',26,6),
(750,'2026-02-12 17:40:17.426095','26','Paterno Materno Tutor Uno',3,'',26,6),
(751,'2026-02-12 17:40:17.426134','25','Paterno2 Materno2 Tutor Dos',3,'',26,6),
(752,'2026-02-12 17:40:17.426173','24','Paterno Materno Tutor Uno',3,'',26,6),
(753,'2026-02-12 17:40:17.426210','23','Paterno2 Materno2 Tutor Dos',3,'',26,6),
(754,'2026-02-12 17:40:17.426248','22','Paterno Materno Tutor Uno',3,'',26,6),
(755,'2026-02-12 17:40:29.503142','2015','Folio 2015 - test_migracion@example.com',3,'',28,6),
(756,'2026-02-12 17:40:29.503246','2014','Folio 2014 - aspirante@test.com',3,'',28,6),
(757,'2026-02-12 17:40:29.503316','2013','Folio 2013 - aspirante_test_1770062701@school.com',3,'',28,6),
(758,'2026-02-12 17:40:29.503374','2012','Folio 2012 - aspirante_test_1770062618@school.com',3,'',28,6),
(759,'2026-02-12 17:40:29.503438','2011','Folio 2011 - aspirante_test_1770062583@school.com',3,'',28,6),
(760,'2026-02-12 17:40:29.503495','2010','Folio 2010 - aspirante_test_1770062563@school.com',3,'',28,6),
(761,'2026-02-12 17:40:29.503552','2009','Folio 2009 - test_5807@example.com',3,'',28,6),
(762,'2026-02-12 17:40:29.503595','2008','Folio 2008 - test_2976@example.com',3,'',28,6),
(763,'2026-02-12 17:40:29.503635','2007','Folio 2007 - test_9133@example.com',3,'',28,6),
(764,'2026-02-12 17:40:29.503673','2006','Folio 2006 - test_7766@example.com',3,'',28,6),
(765,'2026-02-12 17:40:29.503714','2005','Folio 2005 - test_4259@example.com',3,'',28,6),
(766,'2026-02-12 17:40:29.503754','2004','Folio 2004 - test_10798@example.com',3,'',28,6),
(767,'2026-02-12 17:40:29.503792','2003','Folio 2003 - test_8802@example.com',3,'',28,6),
(768,'2026-02-12 17:40:29.503831','2002','Folio 2002 - test_10336@example.com',3,'',28,6),
(769,'2026-02-12 17:40:29.503870','2001','Folio 2001 - test_2237@example.com',3,'',28,6),
(770,'2026-02-12 17:40:29.503910','2000','Folio 2000 - test_5550@example.com',3,'',28,6),
(771,'2026-02-12 17:40:43.665947','66','VerificationCode object (66)',3,'',30,6),
(772,'2026-02-12 17:40:43.666055','65','VerificationCode object (65)',3,'',30,6),
(773,'2026-02-12 17:40:43.666104','64','VerificationCode object (64)',3,'',30,6),
(774,'2026-02-12 17:40:43.666146','63','VerificationCode object (63)',3,'',30,6),
(775,'2026-02-12 17:40:43.666188','62','VerificationCode object (62)',3,'',30,6),
(776,'2026-02-12 17:40:43.666230','61','VerificationCode object (61)',3,'',30,6),
(777,'2026-02-12 17:40:43.666271','60','VerificationCode object (60)',3,'',30,6),
(778,'2026-02-12 17:40:43.666311','59','VerificationCode object (59)',3,'',30,6),
(779,'2026-02-12 17:40:43.666349','58','VerificationCode object (58)',3,'',30,6),
(780,'2026-02-12 17:40:43.666392','57','VerificationCode object (57)',3,'',30,6),
(781,'2026-02-12 17:40:43.666433','56','VerificationCode object (56)',3,'',30,6),
(782,'2026-02-12 17:40:43.666472','55','VerificationCode object (55)',3,'',30,6),
(783,'2026-02-12 17:40:43.666510','54','VerificationCode object (54)',3,'',30,6),
(784,'2026-02-12 17:40:43.666549','53','VerificationCode object (53)',3,'',30,6),
(785,'2026-02-12 17:40:43.666588','52','VerificationCode object (52)',3,'',30,6),
(786,'2026-02-12 17:40:43.666626','51','VerificationCode object (51)',3,'',30,6),
(787,'2026-02-12 17:40:43.666664','50','VerificationCode object (50)',3,'',30,6),
(788,'2026-02-12 17:40:43.666703','49','VerificationCode object (49)',3,'',30,6),
(789,'2026-02-12 17:40:43.666742','48','VerificationCode object (48)',3,'',30,6),
(790,'2026-02-12 17:40:43.666780','47','VerificationCode object (47)',3,'',30,6),
(791,'2026-02-12 17:40:43.666818','46','VerificationCode object (46)',3,'',30,6),
(792,'2026-02-12 17:41:00.724656','3','Director Z',3,'',36,6),
(793,'2026-02-12 17:41:00.724738','2','Director Z',3,'',36,6),
(794,'2026-02-12 17:41:00.724785','1','Director Z',3,'',36,6),
(795,'2026-02-12 17:41:15.246537','4','Profesor X Y',3,'',41,6),
(796,'2026-02-12 17:41:15.246621','3','Profesor X Y',3,'',41,6),
(797,'2026-02-12 17:41:15.246669','2','Profesor X Y',3,'',41,6),
(798,'2026-02-12 17:41:15.246710','1','Profesor X Y',3,'',41,6),
(799,'2026-02-12 17:41:30.611922','1','Programa Primaria 2025 TEST',3,'',45,6),
(800,'2026-02-12 17:42:07.417256','55','1001 - FLORENCIO MOHAMED - 2026-02-04 (Desayuno)',3,'',16,6),
(801,'2026-02-12 17:42:07.417316','54','1001 - FLORENCIO MOHAMED - 2026-02-04 (Comida)',3,'',16,6),
(802,'2026-02-12 17:42:07.417348','53','1001 - FLORENCIO MOHAMED - 2026-02-03 (Comida)',3,'',16,6),
(803,'2026-02-12 17:42:07.417376','51','1000 - ARRON ADRIAN SOMALI - 2026-02-03 (Comida)',3,'',16,6),
(804,'2026-02-12 17:42:07.417402','50','1001 - FLORENCIO MOHAMED - 2026-02-02 (Comida)',3,'',16,6),
(805,'2026-02-12 17:42:07.417429','49','1001 - FLORENCIO MOHAMED - 2026-01-31 (Comida)',3,'',16,6),
(806,'2026-02-12 17:42:07.417455','48','1001 - FLORENCIO MOHAMED - 2026-01-30 (Comida)',3,'',16,6),
(807,'2026-02-12 17:42:07.417481','47','1000 - ARRON ADRIAN SOMALI - 2026-01-30 (Comida)',3,'',16,6),
(808,'2026-02-12 17:42:07.417508','46','1001 - FLORENCIO MOHAMED - 2026-01-30 (Desayuno)',3,'',16,6),
(809,'2026-02-12 17:42:19.607621','22','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(810,'2026-02-12 17:42:19.607677','21','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(811,'2026-02-12 17:42:19.607707','20','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(812,'2026-02-12 17:42:19.607736','19','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(813,'2026-02-12 17:42:19.607766','18','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(814,'2026-02-12 17:42:19.607792','17','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(815,'2026-02-12 17:42:19.607819','16','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(816,'2026-02-12 17:42:19.607846','15','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(817,'2026-02-12 17:42:19.607872','14','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(818,'2026-02-12 17:42:19.607898','13','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(819,'2026-02-12 17:42:19.607926','12','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(820,'2026-02-12 17:42:19.607953','11','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(821,'2026-02-12 17:42:19.607981','10','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(822,'2026-02-12 17:42:19.608035','9','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(823,'2026-02-12 17:42:19.608066','8','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(824,'2026-02-12 17:42:19.608093','7','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(825,'2026-02-12 17:42:19.608120','6','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(826,'2026-02-12 17:42:19.608146','5','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(827,'2026-02-12 17:42:19.608173','4','Menu 2026-02-02 - 2026-02-06',3,'',21,6),
(828,'2026-02-12 17:42:19.608202','3','Menu 2025-01-20 - 2025-01-24',3,'',21,6),
(829,'2026-02-12 17:42:19.608230','2','Menu 2025-01-13 - 2025-01-17',3,'',21,6),
(830,'2026-02-12 17:42:19.608258','1','Menu 2025-01-06 - 2025-01-10',3,'',21,6),
(831,'2026-02-12 17:42:32.659966','25','Menu Test',3,'',20,6),
(832,'2026-02-12 17:42:32.660050','24','Menu Test',3,'',20,6),
(833,'2026-02-12 17:42:32.660079','23','Menu Test',3,'',20,6),
(834,'2026-02-12 17:42:32.660104','22','Menu Test',3,'',20,6),
(835,'2026-02-12 17:42:32.660128','21','Menu Test',3,'',20,6),
(836,'2026-02-12 17:42:32.660151','20','Menu Test',3,'',20,6),
(837,'2026-02-12 17:42:32.660176','19','Menu Test',3,'',20,6),
(838,'2026-02-12 17:42:32.660199','18','Menu Test',3,'',20,6),
(839,'2026-02-12 17:42:32.660223','17','Menu Test',3,'',20,6),
(840,'2026-02-12 17:42:32.660246','16','Menu Test',3,'',20,6),
(841,'2026-02-12 17:42:32.660269','15','Menu Test',3,'',20,6),
(842,'2026-02-12 17:42:32.660291','14','Menu Test',3,'',20,6),
(843,'2026-02-12 17:42:32.660313','13','Menu Test 1770166749',3,'',20,6),
(844,'2026-02-12 17:42:32.660337','12','Menu Test 1770062512',3,'',20,6),
(845,'2026-02-12 17:42:32.660360','11','Menu Test 1769917676',3,'',20,6),
(846,'2026-02-12 17:42:32.660383','10','Menu Test 1769917410',3,'',20,6),
(847,'2026-02-12 17:42:32.660405','9','Menu Test 1769917382',3,'',20,6),
(848,'2026-02-12 17:42:32.660429','8','Menu Test 1769917101',3,'',20,6),
(849,'2026-02-12 17:42:32.660451','7','Menu Test 1769917023',3,'',20,6),
(850,'2026-02-12 17:42:32.660474','6','Comida Corrida Test',3,'',20,6),
(851,'2026-02-12 17:42:32.660497','5','Jugo de Naranja',3,'',20,6),
(852,'2026-02-12 17:42:32.660521','4','Sandwich de Pollo',3,'',20,6),
(853,'2026-02-12 17:42:32.660546','3','Comida Corrida del Dia',3,'',20,6),
(854,'2026-02-12 17:42:32.660574','2','Molletes con Chorizo',3,'',20,6),
(855,'2026-02-12 17:42:32.660598','1','Chilaquiles Rojos',3,'',20,6),
(856,'2026-02-12 17:42:56.789502','9999','9999 - Maria Garcia',3,'',9,6),
(857,'2026-02-12 17:42:56.789556','123457','123457 - JUAN MIGRACION',3,'',9,6),
(858,'2026-02-12 17:42:56.789584','1001','1001 - FLORENCIO MOHAMED',3,'',9,6),
(859,'2026-02-12 17:42:56.789611','123456','123456 - Juan Perez',3,'',9,6),
(860,'2026-02-12 17:42:56.789636','99988886','99988886 - Juanito Perez',3,'',9,6),
(861,'2026-02-12 17:42:56.789661','99988885','99988885 - Juanito Perez',3,'',9,6),
(862,'2026-02-12 17:42:56.789685','99988884','99988884 - Juanito Perez',3,'',9,6),
(863,'2026-02-12 17:42:56.789709','99988883','99988883 - PEDRO REINSC',3,'',9,6),
(864,'2026-02-12 17:42:56.789733','99988828','99988828 - PEDRO REINSC',3,'',9,6),
(865,'2026-02-12 17:42:56.789756','99988814','99988814 - PEDRO REINSC',3,'',9,6),
(866,'2026-02-12 17:42:56.789780','253475','253475 - PEDRO REINSC',3,'',9,6),
(867,'2026-02-12 17:42:56.789804','253430','253430 - PEDRO REINSC',3,'',9,6),
(868,'2026-02-12 17:42:56.789827','1000','1000 - ARRON ADRIAN SOMALI',3,'',9,6),
(869,'2026-02-12 17:42:56.789850','1002','1002 - ESTUDIANTE TEST',3,'',9,6),
(870,'2026-02-12 17:43:24.154252','41','Reinscripcion-Test-1770253475 - ',3,'',18,6),
(871,'2026-02-12 17:43:24.154344','40','Reinscripcion-Test-1770253430 - ',3,'',18,6),
(872,'2026-02-12 17:43:24.154394','39','Reinscripcion 2026-10169 - ',3,'',18,6),
(873,'2026-02-12 17:43:24.154440','38','Reinscripcion 2026-68577 - ',3,'',18,6),
(874,'2026-02-12 17:43:24.154484','36','Reinscripcion 2026 - ',3,'',18,6),
(875,'2026-02-12 17:43:24.154532','35','Reinscripción TEST-2026 - Todos',3,'',18,6),
(876,'2026-02-12 17:43:24.154575','34','Test Concepto - ',3,'',18,6),
(877,'2026-02-12 17:43:24.154622','33','Colegiatura Test - ',3,'',18,6),
(878,'2026-02-12 17:43:24.154665','32','Test Reinscripcion Debt - Todos',3,'',18,6),
(879,'2026-02-12 17:43:24.154712','31','Test Extra Debt - Todos',3,'',18,6),
(880,'2026-02-12 17:43:24.154754','30','Test Reinscripcion - Todos',3,'',18,6),
(881,'2026-02-12 17:43:24.154801','29','Test Extra - Todos',3,'',18,6),
(882,'2026-02-12 17:43:24.154854','28','Reinscripción Preescolar Automática - Preescolar',3,'',18,6),
(883,'2026-02-12 17:43:24.154900','27','Reinscripción Primaria Automática - Primaria',3,'',18,6),
(884,'2026-02-12 17:43:24.154941','26','Consumo Cafeteria - Todos',3,'',18,6),
(885,'2026-02-12 17:44:12.358605','284','1A_TESTA_TEST (2025-2026-TEST)',3,'',13,6),
(886,'2026-02-12 17:44:12.358663','283','1° TESTA TEST (2025-2026 TEST)',3,'',13,6),
(887,'2026-02-12 17:44:12.358694','282','2do-T-1770253475A (Ciclo-Next-1770253475)',3,'',13,6),
(888,'2026-02-12 17:44:12.358723','281','1ro-T-1770253475A (Ciclo-Act-1770253475)',3,'',13,6),
(889,'2026-02-12 17:44:12.358749','280','2do-T-1770253430A (Ciclo-Next-1770253430)',3,'',13,6),
(890,'2026-02-12 17:44:12.358776','279','1ro-T-1770253430A (Ciclo-Act-1770253430)',3,'',13,6),
(891,'2026-02-12 17:44:12.358803','278','2do-T-10169A (2026-Next-10169)',3,'',13,6),
(892,'2026-02-12 17:44:12.358830','277','1ro-T-10169A (2025-Act-10169)',3,'',13,6),
(893,'2026-02-12 17:44:12.358856','276','2do-T-68577A (2026-Next-68577)',3,'',13,6),
(894,'2026-02-12 17:44:12.358882','275','1ro-T-68577A (2025-Act-68577)',3,'',13,6),
(895,'2026-02-12 17:44:12.358908','274','2do-T-25378A (2026-Next-25378)',3,'',13,6),
(896,'2026-02-12 17:44:12.358934','273','1ro-T-25378A (2025-Act-25378)',3,'',13,6),
(897,'2026-02-12 17:44:49.164433','53','1A_TEST PRIMARIA_TEST',3,'',12,6),
(898,'2026-02-12 17:44:49.164515','52','1° TEST - PRIMARIA',3,'',12,6),
(899,'2026-02-12 17:44:49.164566','51','2do-T-1770253475 Nivel-Test-1770253475',3,'',12,6),
(900,'2026-02-12 17:44:49.164612','50','1ro-T-1770253475 Nivel-Test-1770253475',3,'',12,6),
(901,'2026-02-12 17:44:49.164657','49','2do-T-1770253430 Nivel-Test-1770253430',3,'',12,6),
(902,'2026-02-12 17:44:49.164701','48','1ro-T-1770253430 Nivel-Test-1770253430',3,'',12,6),
(903,'2026-02-12 17:44:49.164745','47','2do-T-10169 Primaria',3,'',12,6),
(904,'2026-02-12 17:44:49.164789','46','1ro-T-10169 Primaria',3,'',12,6),
(905,'2026-02-12 17:44:49.164833','45','2do-T-68577 Primaria',3,'',12,6),
(906,'2026-02-12 17:44:49.164876','44','1ro-T-68577 Primaria',3,'',12,6),
(907,'2026-02-12 17:44:49.164919','43','2do-T-25378 Primaria',3,'',12,6),
(908,'2026-02-12 17:44:49.164964','42','1ro-T-25378 Primaria',3,'',12,6),
(909,'2026-02-12 17:45:07.684083','40','1ro Primaria',3,'',12,6),
(910,'2026-02-12 17:45:07.684162','41','2do Primaria',3,'',12,6),
(911,'2026-02-12 17:46:25.125642','233','1°A (2026-2027)',3,'',13,6),
(912,'2026-02-12 17:46:25.125692','16','1°A (2024-2025)',3,'',13,6),
(913,'2026-02-12 17:46:25.125723','234','1°B (2026-2027)',3,'',13,6),
(914,'2026-02-12 17:46:25.125751','17','1°B (2024-2025)',3,'',13,6),
(915,'2026-02-12 17:46:25.125778','235','1°C (2026-2027)',3,'',13,6),
(916,'2026-02-12 17:46:25.125806','18','1°C (2024-2025)',3,'',13,6),
(917,'2026-02-12 17:46:25.125833','236','2°A (2026-2027)',3,'',13,6),
(918,'2026-02-12 17:46:25.125860','19','2°A (2024-2025)',3,'',13,6),
(919,'2026-02-12 17:46:25.125886','237','2°B (2026-2027)',3,'',13,6),
(920,'2026-02-12 17:46:25.125912','20','2°B (2024-2025)',3,'',13,6),
(921,'2026-02-12 17:46:25.125939','238','2°C (2026-2027)',3,'',13,6),
(922,'2026-02-12 17:46:25.125965','21','2°C (2024-2025)',3,'',13,6),
(923,'2026-02-12 17:46:25.126006','239','3°A (2026-2027)',3,'',13,6),
(924,'2026-02-12 17:46:25.126033','22','3°A (2024-2025)',3,'',13,6),
(925,'2026-02-12 17:46:25.126058','240','3°B (2026-2027)',3,'',13,6),
(926,'2026-02-12 17:46:25.126084','23','3°B (2024-2025)',3,'',13,6),
(927,'2026-02-12 17:46:25.126110','241','3°C (2026-2027)',3,'',13,6),
(928,'2026-02-12 17:46:25.126136','24','3°C (2024-2025)',3,'',13,6),
(929,'2026-02-12 17:46:25.126162','269','1°A (TEST-2026)',3,'',13,6),
(930,'2026-02-12 17:46:25.126188','242','1°A (2026-2027)',3,'',13,6),
(931,'2026-02-12 17:46:25.126214','196','1°A (2025-2026)',3,'',13,6),
(932,'2026-02-12 17:46:25.126240','25','1°A (2024-2025)',3,'',13,6),
(933,'2026-02-12 17:46:25.126266','243','1°B (2026-2027)',3,'',13,6),
(934,'2026-02-12 17:46:25.126291','26','1°B (2024-2025)',3,'',13,6),
(935,'2026-02-12 17:46:25.126317','244','1°C (2026-2027)',3,'',13,6),
(936,'2026-02-12 17:46:25.126342','27','1°C (2024-2025)',3,'',13,6),
(937,'2026-02-12 17:46:25.126367','245','2°A (2026-2027)',3,'',13,6),
(938,'2026-02-12 17:46:25.126393','28','2°A (2024-2025)',3,'',13,6),
(939,'2026-02-12 17:46:25.126418','246','2°B (2026-2027)',3,'',13,6),
(940,'2026-02-12 17:46:25.126444','29','2°B (2024-2025)',3,'',13,6),
(941,'2026-02-12 17:46:25.126469','247','2°C (2026-2027)',3,'',13,6),
(942,'2026-02-12 17:46:25.126495','30','2°C (2024-2025)',3,'',13,6),
(943,'2026-02-12 17:46:25.126520','248','3°A (2026-2027)',3,'',13,6),
(944,'2026-02-12 17:46:25.126546','31','3°A (2024-2025)',3,'',13,6),
(945,'2026-02-12 17:46:25.126572','249','3°B (2026-2027)',3,'',13,6),
(946,'2026-02-12 17:46:25.126597','32','3°B (2024-2025)',3,'',13,6),
(947,'2026-02-12 17:46:25.126623','250','3°C (2026-2027)',3,'',13,6),
(948,'2026-02-12 17:46:25.126648','33','3°C (2024-2025)',3,'',13,6),
(949,'2026-02-12 17:46:25.126673','251','4°A (2026-2027)',3,'',13,6),
(950,'2026-02-12 17:46:25.126699','34','4°A (2024-2025)',3,'',13,6),
(951,'2026-02-12 17:46:25.126725','252','4°B (2026-2027)',3,'',13,6),
(952,'2026-02-12 17:46:25.126751','35','4°B (2024-2025)',3,'',13,6),
(953,'2026-02-12 17:46:25.126777','253','4°C (2026-2027)',3,'',13,6),
(954,'2026-02-12 17:46:25.126803','36','4°C (2024-2025)',3,'',13,6),
(955,'2026-02-12 17:46:25.126830','254','5°A (2026-2027)',3,'',13,6),
(956,'2026-02-12 17:46:25.126857','37','5°A (2024-2025)',3,'',13,6),
(957,'2026-02-12 17:46:25.126883','255','5°B (2026-2027)',3,'',13,6),
(958,'2026-02-12 17:46:25.126908','38','5°B (2024-2025)',3,'',13,6),
(959,'2026-02-12 17:46:25.126935','256','5°C (2026-2027)',3,'',13,6),
(960,'2026-02-12 17:46:25.126961','39','5°C (2024-2025)',3,'',13,6),
(961,'2026-02-12 17:46:25.126987','257','6°A (2026-2027)',3,'',13,6),
(962,'2026-02-12 17:46:25.127038','40','6°A (2024-2025)',3,'',13,6),
(963,'2026-02-12 17:46:25.127071','258','6°B (2026-2027)',3,'',13,6),
(964,'2026-02-12 17:46:25.127098','41','6°B (2024-2025)',3,'',13,6),
(965,'2026-02-12 17:46:25.127124','259','6°C (2026-2027)',3,'',13,6),
(966,'2026-02-12 17:46:25.127150','42','6°C (2024-2025)',3,'',13,6),
(967,'2026-02-12 17:46:25.127176','260','1°A (2026-2027)',3,'',13,6),
(968,'2026-02-12 17:46:25.127201','43','1°A (2024-2025)',3,'',13,6),
(969,'2026-02-12 17:46:25.127229','261','1°B (2026-2027)',3,'',13,6),
(970,'2026-02-12 17:46:25.127254','44','1°B (2024-2025)',3,'',13,6),
(971,'2026-02-12 17:46:25.127280','262','1°C (2026-2027)',3,'',13,6),
(972,'2026-02-12 17:46:25.127305','45','1°C (2024-2025)',3,'',13,6),
(973,'2026-02-12 17:46:25.127332','263','2°A (2026-2027)',3,'',13,6),
(974,'2026-02-12 17:46:25.127357','46','2°A (2024-2025)',3,'',13,6),
(975,'2026-02-12 17:46:25.127383','264','2°B (2026-2027)',3,'',13,6),
(976,'2026-02-12 17:46:25.127409','47','2°B (2024-2025)',3,'',13,6),
(977,'2026-02-12 17:46:25.127435','265','2°C (2026-2027)',3,'',13,6),
(978,'2026-02-12 17:46:25.127461','48','2°C (2024-2025)',3,'',13,6),
(979,'2026-02-12 17:46:25.127487','266','3°A (2026-2027)',3,'',13,6),
(980,'2026-02-12 17:46:25.127512','49','3°A (2024-2025)',3,'',13,6),
(981,'2026-02-12 17:46:25.127537','267','3°B (2026-2027)',3,'',13,6),
(982,'2026-02-12 17:46:25.127563','50','3°B (2024-2025)',3,'',13,6),
(983,'2026-02-12 17:46:25.127588','268','3°C (2026-2027)',3,'',13,6),
(984,'2026-02-12 17:46:25.127612','51','3°C (2024-2025)',3,'',13,6),
(985,'2026-02-12 17:46:51.435559','23','2025-2026 TEST ',3,'',31,6),
(986,'2026-02-12 17:46:51.435634','7','2026-2027 ',3,'',31,6),
(987,'2026-02-12 17:46:51.435676','22','Ciclo-Next-1770253475 ',3,'',31,6),
(988,'2026-02-12 17:46:51.435717','20','Ciclo-Next-1770253430 ',3,'',31,6),
(989,'2026-02-12 17:46:51.435756','18','2026-Next-10169 ',3,'',31,6),
(990,'2026-02-12 17:46:51.435791','16','2026-Next-68577 ',3,'',31,6),
(991,'2026-02-12 17:46:51.435829','14','2026-Next-25378 ',3,'',31,6),
(992,'2026-02-12 17:46:51.435867','12','2026-Next ',3,'',31,6),
(993,'2026-02-12 17:46:51.435905','9','2026-Test ',3,'',31,6),
(994,'2026-02-12 17:46:51.435943','8','TEST-2026 ',3,'',31,6),
(995,'2026-02-12 17:46:51.435982','24','2025-2026-TEST [ACTIVO]',3,'',31,6),
(996,'2026-02-12 17:46:51.436040','6','2025-2026 ',3,'',31,6),
(997,'2026-02-12 17:46:51.436076','21','Ciclo-Act-1770253475 ',3,'',31,6),
(998,'2026-02-12 17:46:51.436112','19','Ciclo-Act-1770253430 ',3,'',31,6),
(999,'2026-02-12 17:46:51.436150','17','2025-Act-10169 ',3,'',31,6),
(1000,'2026-02-12 17:46:51.436190','15','2025-Act-68577 ',3,'',31,6),
(1001,'2026-02-12 17:46:51.436228','13','2025-Act-25378 ',3,'',31,6),
(1002,'2026-02-12 17:46:51.436269','11','2025-Act ',3,'',31,6),
(1003,'2026-02-12 17:46:51.436308','1','2024-2025 ',3,'',31,6),
(1004,'2026-02-12 17:47:16.856544','25','2026-2027 [ACTIVO]',1,'[{\"added\": {}}]',31,6),
(1005,'2026-02-12 17:53:41.365793','6','PRIMARIA_TEST',3,'',33,6),
(1006,'2026-02-12 17:53:41.365850','5','Nivel-Test-1770253475',3,'',33,6),
(1007,'2026-02-12 17:53:41.365879','4','Nivel-Test-1770253430',3,'',33,6),
(1008,'2026-02-12 17:55:02.841620','2','Programa educativo 2017 Preescolar',1,'[{\"added\": {}}]',45,6),
(1009,'2026-02-12 17:56:52.787210','3','Programa Edcuativo 2017 - Primaria',1,'[{\"added\": {}}]',45,6),
(1010,'2026-02-12 18:01:08.659706','4','Programa Educativo Secundaria 2017',1,'[{\"added\": {}}]',45,6),
(1011,'2026-02-12 18:03:17.456478','2','Enero-Febrero - 2026-2027 [ACTIVO]',1,'[{\"added\": {}}]',44,6),
(1012,'2026-02-12 18:05:12.476367','1000','1000 - MAURICIO ANDRÉS PADILLA',1,'[{\"added\": {}}]',9,6),
(1013,'2026-02-12 18:05:34.137024','1000','1000 - MAURICIO ANDRÉS PADILLA',2,'[{\"added\": {\"name\": \"Beca-Estudiante\", \"object\": \"1000 - MAURICIO ANDR\\u00c9S PADILLA - Beca 10% (Activa)\"}}]',9,6),
(1014,'2026-02-12 18:05:48.656017','1000','1000 - MAURICIO ANDRÉS PADILLA',2,'[]',9,6),
(1015,'2026-02-12 18:07:27.689122','1000','1000 - MAURICIO ANDRÉS PADILLA',2,'[{\"added\": {\"name\": \"Evaluaci\\u00f3n Socioecon\\u00f3mica\", \"object\": \"Evaluaci\\u00f3n 1000 - MAURICIO ANDR\\u00c9S PADILLA - Pendiente\"}}]',9,6),
(1016,'2026-02-12 18:07:39.849455','1000','1000 - MAURICIO ANDRÉS PADILLA',2,'[]',9,6),
(1017,'2026-02-12 18:08:10.511976','72','Evaluación 1000 - MAURICIO ANDRÉS PADILLA - Aprobada',2,'[{\"changed\": {\"fields\": [\"Aprobado\"]}}]',11,6),
(1018,'2026-02-12 18:11:23.745951','1001','1001 - RAMIRO PATADA',1,'[{\"added\": {}}, {\"added\": {\"name\": \"Estudiante-Tutor\", \"object\": \"1001 - RAMIRO PATADA -> Maria FERNANDA Garcia Lopez (Madre)\"}}]',9,6),
(1019,'2026-02-12 18:12:00.144569','1001','1001 - RAMIRO PATADA',2,'[{\"added\": {\"name\": \"Evaluaci\\u00f3n Socioecon\\u00f3mica\", \"object\": \"Evaluaci\\u00f3n 1001 - RAMIRO PATADA - Aprobada\"}}]',9,6),
(1020,'2026-02-12 18:12:25.305398','1001','1001 - RAMIRO PATADA',2,'[{\"changed\": {\"name\": \"Inscripci\\u00f3n\", \"object\": \"1001 - RAMIRO PATADA - 3\\u00b0B (2026-2027) (activo)\", \"fields\": [\"Grupo\"]}}]',9,6),
(1021,'2026-02-12 18:18:46.688807','2','Enero-Febrero - 2026-2027 [ACTIVO]',2,'[{\"changed\": {\"fields\": [\"Estatus\"]}}]',44,6),
(1022,'2026-02-12 18:19:58.369514','2','Matemáticas (1)',1,'[{\"added\": {}}]',42,6),
(1023,'2026-02-12 18:20:39.498908','117','admin_escolar_test_4016@school.com (admin_escolar)',3,'',1,6),
(1024,'2026-02-12 18:20:39.499022','111','admin_escolar_test_6777@school.com (admin_escolar)',3,'',1,6),
(1025,'2026-02-12 18:20:39.499074','114','admin_escolar_test_9163@school.com (admin_escolar)',3,'',1,6),
(1026,'2026-02-12 18:20:39.499136','7','admin_test@example.com (administrador)',3,'',1,6),
(1027,'2026-02-12 18:20:39.499198','91','admin_testing@school.com (comedor_admin)',3,'',1,6),
(1028,'2026-02-12 18:20:39.499253','9','admin_verify@test.com (administrador)',3,'',1,6),
(1029,'2026-02-12 18:20:39.499293','94','aspirante@test.com (aspirante)',3,'',1,6),
(1030,'2026-02-12 18:20:39.499332','77','bandit@test.com (estudiante)',3,'',1,6),
(1031,'2026-02-12 18:20:39.499371','86','e_716081@t.com (estudiante)',3,'',1,6),
(1032,'2026-02-12 18:20:39.499411','84','e_716821@t.com (estudiante)',3,'',1,6),
(1033,'2026-02-12 18:20:39.499452','85','e_729293@t.com (estudiante)',3,'',1,6),
(1034,'2026-02-12 18:20:39.499492','82','e_828974@t.com (estudiante)',3,'',1,6),
(1035,'2026-02-12 18:20:39.499533','83','e_829740@t.com (estudiante)',3,'',1,6),
(1036,'2026-02-12 18:20:39.499572','81','e_830259@t.com (estudiante)',3,'',1,6),
(1037,'2026-02-12 18:20:39.499611','118','estudiante_test_4016@school.com (estudiante)',3,'',1,6),
(1038,'2026-02-12 18:20:39.499649','112','estudiante_test_6777@school.com (estudiante)',3,'',1,6),
(1039,'2026-02-12 18:20:39.499694','115','estudiante_test_9163@school.com (estudiante)',3,'',1,6),
(1040,'2026-02-12 18:20:39.499751','95','estudiante@test.com (estudiante)',3,'',1,6),
(1041,'2026-02-12 18:20:39.499791','116','maestro_test_4016@school.com (maestro)',3,'',1,6),
(1042,'2026-02-12 18:20:39.499829','110','maestro_test_6777@school.com (maestro)',3,'',1,6),
(1043,'2026-02-12 18:20:39.499867','113','maestro_test_9163@school.com (maestro)',3,'',1,6),
(1044,'2026-02-12 18:20:39.499924','108','maestro_test@school.com (maestro)',3,'',1,6),
(1045,'2026-02-12 18:20:39.499973','8','prueba@test.com (Estudiante)',3,'',1,6),
(1046,'2026-02-12 18:20:39.500030','90','roberto@gmail.com (estudiante)',3,'',1,6),
(1047,'2026-02-12 18:20:39.500074','17','student_0_1468@test.com (estudiante)',3,'',1,6),
(1048,'2026-02-12 18:20:39.500130','47','student_0_1685@test.com (estudiante)',3,'',1,6),
(1049,'2026-02-12 18:20:39.500170','48','student_1_2090@test.com (estudiante)',3,'',1,6),
(1050,'2026-02-12 18:20:39.500208','18','student_1_9604@test.com (estudiante)',3,'',1,6),
(1051,'2026-02-12 18:20:39.500246','27','student_10_2617@test.com (estudiante)',3,'',1,6),
(1052,'2026-02-12 18:20:39.500284','57','student_10_7371@test.com (estudiante)',3,'',1,6),
(1053,'2026-02-12 18:20:39.500322','58','student_11_2128@test.com (estudiante)',3,'',1,6),
(1054,'2026-02-12 18:20:39.500359','28','student_11_3087@test.com (estudiante)',3,'',1,6),
(1055,'2026-02-12 18:20:39.500396','29','student_12_4799@test.com (estudiante)',3,'',1,6),
(1056,'2026-02-12 18:20:39.500435','59','student_12_6041@test.com (estudiante)',3,'',1,6),
(1057,'2026-02-12 18:20:39.500474','30','student_13_6368@test.com (estudiante)',3,'',1,6),
(1058,'2026-02-12 18:20:39.500511','60','student_13_7314@test.com (estudiante)',3,'',1,6),
(1059,'2026-02-12 18:20:39.500549','31','student_14_1200@test.com (estudiante)',3,'',1,6),
(1060,'2026-02-12 18:20:39.500586','61','student_14_3075@test.com (estudiante)',3,'',1,6),
(1061,'2026-02-12 18:20:39.500624','62','student_15_1151@test.com (estudiante)',3,'',1,6),
(1062,'2026-02-12 18:20:39.500661','32','student_15_3220@test.com (estudiante)',3,'',1,6),
(1063,'2026-02-12 18:20:39.500698','33','student_16_6221@test.com (estudiante)',3,'',1,6),
(1064,'2026-02-12 18:20:39.500737','63','student_16_9351@test.com (estudiante)',3,'',1,6),
(1065,'2026-02-12 18:20:39.500775','64','student_17_1759@test.com (estudiante)',3,'',1,6),
(1066,'2026-02-12 18:20:39.500827','34','student_17_2022@test.com (estudiante)',3,'',1,6),
(1067,'2026-02-12 18:20:39.500885','65','student_18_4045@test.com (estudiante)',3,'',1,6),
(1068,'2026-02-12 18:20:39.500926','35','student_18_4298@test.com (estudiante)',3,'',1,6),
(1069,'2026-02-12 18:20:39.500966','36','student_19_2004@test.com (estudiante)',3,'',1,6),
(1070,'2026-02-12 18:20:39.501019','66','student_19_6407@test.com (estudiante)',3,'',1,6),
(1071,'2026-02-12 18:20:39.501062','19','student_2_2479@test.com (estudiante)',3,'',1,6),
(1072,'2026-02-12 18:20:39.501100','49','student_2_9566@test.com (estudiante)',3,'',1,6),
(1073,'2026-02-12 18:20:39.501138','37','student_20_1007@test.com (estudiante)',3,'',1,6),
(1074,'2026-02-12 18:20:39.501176','67','student_20_1491@test.com (estudiante)',3,'',1,6),
(1075,'2026-02-12 18:20:39.501215','38','student_21_1115@test.com (estudiante)',3,'',1,6),
(1076,'2026-02-12 18:20:39.501253','68','student_21_2472@test.com (estudiante)',3,'',1,6),
(1077,'2026-02-12 18:20:39.501292','39','student_22_1593@test.com (estudiante)',3,'',1,6),
(1078,'2026-02-12 18:20:39.501330','69','student_22_2212@test.com (estudiante)',3,'',1,6),
(1079,'2026-02-12 18:20:39.501368','70','student_23_3269@test.com (estudiante)',3,'',1,6),
(1080,'2026-02-12 18:20:39.501407','40','student_23_8078@test.com (estudiante)',3,'',1,6),
(1081,'2026-02-12 18:20:39.501463','71','student_24_2857@test.com (estudiante)',3,'',1,6),
(1082,'2026-02-12 18:20:39.501504','41','student_24_5431@test.com (estudiante)',3,'',1,6),
(1083,'2026-02-12 18:20:39.501542','42','student_25_5749@test.com (estudiante)',3,'',1,6),
(1084,'2026-02-12 18:20:39.501597','72','student_25_8416@test.com (estudiante)',3,'',1,6),
(1085,'2026-02-12 18:20:39.501654','43','student_26_3060@test.com (estudiante)',3,'',1,6),
(1086,'2026-02-12 18:20:39.501711','73','student_26_8698@test.com (estudiante)',3,'',1,6),
(1087,'2026-02-12 18:20:39.501755','74','student_27_6221@test.com (estudiante)',3,'',1,6),
(1088,'2026-02-12 18:20:39.501796','44','student_27_7915@test.com (estudiante)',3,'',1,6),
(1089,'2026-02-12 18:20:39.501834','45','student_28_2491@test.com (estudiante)',3,'',1,6),
(1090,'2026-02-12 18:20:39.501872','75','student_28_8696@test.com (estudiante)',3,'',1,6),
(1091,'2026-02-12 18:20:39.501910','76','student_29_6601@test.com (estudiante)',3,'',1,6),
(1092,'2026-02-12 18:20:39.501947','46','student_29_7825@test.com (estudiante)',3,'',1,6),
(1093,'2026-02-12 18:20:39.501985','50','student_3_1698@test.com (estudiante)',3,'',1,6),
(1094,'2026-02-12 18:20:39.502048','20','student_3_9443@test.com (estudiante)',3,'',1,6),
(1095,'2026-02-12 18:20:39.502087','21','student_4_2977@test.com (estudiante)',3,'',1,6),
(1096,'2026-02-12 18:20:39.502125','51','student_4_9119@test.com (estudiante)',3,'',1,6),
(1097,'2026-02-12 18:20:39.502163','52','student_5_4643@test.com (estudiante)',3,'',1,6),
(1098,'2026-02-12 18:20:39.502201','22','student_5_6821@test.com (estudiante)',3,'',1,6),
(1099,'2026-02-12 18:20:39.502239','23','student_6_1320@test.com (estudiante)',3,'',1,6),
(1100,'2026-02-12 18:20:39.502278','53','student_6_8534@test.com (estudiante)',3,'',1,6),
(1101,'2026-02-12 18:20:39.502316','24','student_7_3514@test.com (estudiante)',3,'',1,6),
(1102,'2026-02-12 18:20:39.502354','54','student_7_5479@test.com (estudiante)',3,'',1,6),
(1103,'2026-02-12 18:20:39.502392','25','student_8_1759@test.com (estudiante)',3,'',1,6),
(1104,'2026-02-12 18:20:39.502430','55','student_8_9706@test.com (estudiante)',3,'',1,6),
(1105,'2026-02-12 18:20:39.502469','26','student_9_3689@test.com (estudiante)',3,'',1,6),
(1106,'2026-02-12 18:20:39.502507','56','student_9_5652@test.com (estudiante)',3,'',1,6),
(1107,'2026-02-12 18:20:39.502545','16','student_crud@test.com (estudiante)',3,'',1,6),
(1108,'2026-02-12 18:20:39.502583','92','student_test_final@school.com (estudiante)',3,'',1,6),
(1109,'2026-02-12 18:20:39.502622','78','test_1768949919@example.com (estudiante)',3,'',1,6),
(1110,'2026-02-12 18:20:39.502659','79','test_906028@school.com (estudiante)',3,'',1,6),
(1111,'2026-02-12 18:20:39.502697','80','test_923666@school.com (estudiante)',3,'',1,6),
(1112,'2026-02-12 18:20:39.502735','99','test_migracion@example.com (estudiante)',3,'',1,6),
(1113,'2026-02-12 18:20:39.502775','105','test_r_1770253420@example.com (estudiante)',3,'',1,6),
(1114,'2026-02-12 18:20:39.502814','106','test_r_1770253430@example.com (estudiante)',3,'',1,6),
(1115,'2026-02-12 18:20:39.502852','107','test_r_1770253475@example.com (estudiante)',3,'',1,6),
(1116,'2026-02-12 18:20:39.502891','101','test_reinscrip@example.com (estudiante)',3,'',1,6),
(1117,'2026-02-12 18:20:39.502930','104','test_reinscrip34913@example.com (estudiante)',3,'',1,6),
(1118,'2026-02-12 18:20:39.502967','103','test_reinscrip76763@example.com (estudiante)',3,'',1,6),
(1119,'2026-02-12 18:21:02.144895','102','test_reinscrip88201@example.com (estudiante)',3,'',1,6),
(1120,'2026-02-12 18:21:02.144972','93','test_reset@school.com (estudiante)',3,'',1,6),
(1121,'2026-02-12 18:21:02.145045','89','testpass@gmail.com (estudiante)',3,'',1,6),
(1122,'2026-02-12 18:56:44.548700','5','HECTOR ADAN HURTADO BRISEÑO',1,'[{\"added\": {}}]',41,6),
(1123,'2026-02-12 18:57:09.346464','2','HECTOR ADAN HURTADO BRISEÑO - Matemáticas (1) (3°B (2026-2027))',1,'[{\"added\": {}}]',37,6),
(1124,'2026-02-12 18:57:23.822214','2','HECTOR ADAN HURTADO BRISEÑO - Matemáticas (1) (3°B (2026-2027))',2,'[]',37,6),
(1125,'2026-02-12 18:58:05.331763','4','1000 - MAURICIO ANDRÉS PADILLA - 9',1,'[{\"added\": {}}]',39,6),
(1126,'2026-02-12 18:59:51.648405','1000','1000 - MAURICIO ANDRÉS PADILLA',2,'[{\"added\": {\"name\": \"Estudiante-Tutor\", \"object\": \"1000 - MAURICIO ANDR\\u00c9S PADILLA -> PEPE EL PIYO Sanchez Pedroza (Padre)\"}}]',9,6),
(1127,'2026-02-12 19:00:48.788241','4','1000 - MAURICIO ANDRÉS PADILLA - 10',2,'[{\"changed\": {\"fields\": [\"Calificacion\"]}}]',39,6),
(1128,'2026-02-12 19:03:03.878217','26','2027-2028 [ACTIVO]',1,'[{\"added\": {}}]',31,6),
(1129,'2026-02-12 19:04:41.543581','84','Pago $1500.00 - 2026-02-12',1,'[{\"added\": {}}]',19,6),
(1130,'2026-02-12 19:05:47.290080','71','padilla@gmail.com - 2026-02-12 18:59:12.142410+00:00 - EXITOSO',3,'',34,6),
(1131,'2026-02-12 19:05:47.290173','70','student_test_final@school.com - 2026-02-12 03:06:40.646335+00:00 - EXITOSO',3,'',34,6),
(1132,'2026-02-12 19:05:47.290229','69','student_test_final@school.com - 2026-02-12 03:02:15.939524+00:00 - FALLIDO',3,'',34,6),
(1133,'2026-02-12 19:05:47.290278','68','estudiante@test.com - 2026-02-12 03:01:31.032069+00:00 - FALLIDO',3,'',34,6),
(1134,'2026-02-12 19:05:47.290326','67','student_0_1468@test.com - 2026-02-12 02:56:17.548109+00:00 - EXITOSO',3,'',34,6),
(1135,'2026-02-12 19:05:47.290373','66','student_0_1468@test.com - 2026-02-12 02:56:05.317396+00:00 - EXITOSO',3,'',34,6),
(1136,'2026-02-12 19:05:47.290419','65','adancpphack@gmail.com - 2026-02-12 02:55:13.541091+00:00 - EXITOSO',3,'',34,6),
(1137,'2026-02-12 19:05:47.290464','64','adancpphack@gmail.com - 2026-02-12 02:24:18.448535+00:00 - EXITOSO',3,'',34,6),
(1138,'2026-02-12 19:05:47.290511','63','hectorino2789@gmail.com - 2026-02-12 01:55:59.929864+00:00 - EXITOSO',3,'',34,6),
(1139,'2026-02-12 19:05:47.290558','62','adancpphack@gmail.com - 2026-02-12 01:55:25.537917+00:00 - EXITOSO',3,'',34,6),
(1140,'2026-02-12 19:05:47.290604','61','adancpphack@gmail.com - 2026-02-12 01:55:05.716199+00:00 - FALLIDO',3,'',34,6),
(1141,'2026-02-12 19:05:47.290650','60','bandit@test.com - 2026-02-11 01:07:55.032340+00:00 - EXITOSO',3,'',34,6),
(1142,'2026-02-12 19:05:47.290695','59','hectorino2789@gmail.com - 2026-02-11 01:00:04.160930+00:00 - EXITOSO',3,'',34,6),
(1143,'2026-02-12 19:05:47.290740','58','adancpphack@gmail.com - 2026-02-11 00:53:41.195220+00:00 - EXITOSO',3,'',34,6),
(1144,'2026-02-12 19:05:47.290784','57','hectorino2789@gmail.com - 2026-02-11 00:47:13.058559+00:00 - EXITOSO',3,'',34,6),
(1145,'2026-02-12 19:05:47.290863','56','adancpphack@gmail.com - 2026-02-11 00:43:40.150698+00:00 - EXITOSO',3,'',34,6),
(1146,'2026-02-12 19:05:47.290933','55','admin_testing@school.com - 2026-02-05 03:23:28.843834+00:00 - EXITOSO',3,'',34,6),
(1147,'2026-02-12 19:05:47.290982','54','admin_testing@school.com - 2026-02-05 03:22:54.285594+00:00 - EXITOSO',3,'',34,6),
(1148,'2026-02-12 19:05:47.291027','53','admin_testing@school.com - 2026-02-05 03:22:30.059024+00:00 - EXITOSO',3,'',34,6),
(1149,'2026-02-12 19:05:47.291072','52','admin_testing@school.com - 2026-02-05 03:22:15.542382+00:00 - EXITOSO',3,'',34,6),
(1150,'2026-02-12 19:05:47.291117','51','admin_testing@school.com - 2026-02-05 03:21:52.295466+00:00 - EXITOSO',3,'',34,6),
(1151,'2026-02-12 19:05:47.291161','50','admin_testing@school.com - 2026-02-05 03:21:28.191287+00:00 - EXITOSO',3,'',34,6),
(1152,'2026-02-12 19:05:47.291207','49','admin_testing@school.com - 2026-02-05 03:20:27.353343+00:00 - EXITOSO',3,'',34,6),
(1153,'2026-02-12 19:05:47.291252','48','admin_testing@school.com - 2026-02-05 03:10:07.093456+00:00 - EXITOSO',3,'',34,6),
(1154,'2026-02-12 19:05:47.291296','47','admin_testing@school.com - 2026-02-05 03:08:36.082874+00:00 - EXITOSO',3,'',34,6),
(1155,'2026-02-12 19:05:47.291338','46','admin_testing@school.com - 2026-02-05 02:57:02.553703+00:00 - EXITOSO',3,'',34,6),
(1156,'2026-02-12 19:05:47.291383','45','admin_testing@school.com - 2026-02-05 01:37:21.641459+00:00 - EXITOSO',3,'',34,6),
(1157,'2026-02-12 19:05:47.291427','44','admin_testing@school.com - 2026-02-05 01:37:07.581978+00:00 - EXITOSO',3,'',34,6),
(1158,'2026-02-12 19:05:47.291470','43','admin_testing@school.com - 2026-02-05 01:36:54.992071+00:00 - EXITOSO',3,'',34,6),
(1159,'2026-02-12 19:05:47.291514','42','admin_testing@school.com - 2026-02-05 01:36:39.425734+00:00 - EXITOSO',3,'',34,6),
(1160,'2026-02-12 19:05:47.291558','41','admin_testing@school.com - 2026-02-05 01:36:37.098669+00:00 - EXITOSO',3,'',34,6),
(1161,'2026-02-12 19:05:47.291602','40','admin_testing@school.com - 2026-02-05 01:26:07.736337+00:00 - EXITOSO',3,'',34,6),
(1162,'2026-02-12 19:05:47.291647','39','admin_testing@school.com - 2026-02-05 01:25:40.760400+00:00 - EXITOSO',3,'',34,6),
(1163,'2026-02-12 19:05:47.291692','38','admin_testing@school.com - 2026-02-05 01:25:27.265800+00:00 - EXITOSO',3,'',34,6),
(1164,'2026-02-12 19:05:47.291737','37','admin_testing@school.com - 2026-02-05 01:24:31.823366+00:00 - EXITOSO',3,'',34,6),
(1165,'2026-02-12 19:05:47.291782','36','admin_testing@school.com - 2026-02-05 01:24:24.402485+00:00 - EXITOSO',3,'',34,6),
(1166,'2026-02-12 19:05:47.291847','35','admin_testing@school.com - 2026-02-04 23:16:58.318261+00:00 - EXITOSO',3,'',34,6),
(1167,'2026-02-12 19:05:47.291894','34','admin_testing@school.com - 2026-02-04 20:57:45.919319+00:00 - EXITOSO',3,'',34,6),
(1168,'2026-02-12 19:05:47.291938','33','admin_testing@school.com - 2026-02-04 20:57:06.756207+00:00 - EXITOSO',3,'',34,6),
(1169,'2026-02-12 19:05:47.291983','32','admin_testing@school.com - 2026-02-04 20:43:36.799819+00:00 - EXITOSO',3,'',34,6),
(1170,'2026-02-12 19:05:47.292028','31','admin_testing@school.com - 2026-02-04 20:43:25.218171+00:00 - EXITOSO',3,'',34,6),
(1171,'2026-02-12 19:05:47.292074','30','admin_testing@school.com - 2026-02-04 20:42:02.962524+00:00 - EXITOSO',3,'',34,6),
(1172,'2026-02-12 19:05:47.292119','29','admin_testing@school.com - 2026-02-04 20:41:45.094848+00:00 - EXITOSO',3,'',34,6),
(1173,'2026-02-12 19:05:47.292165','28','student_test_final@school.com - 2026-02-04 20:41:26.831783+00:00 - FALLIDO',3,'',34,6),
(1174,'2026-02-12 19:05:47.292212','27','admin_testing@school.com - 2026-02-04 20:41:02.764319+00:00 - EXITOSO',3,'',34,6),
(1175,'2026-02-12 19:05:47.292259','26','admin_testing@school.com - 2026-02-04 01:04:12.573052+00:00 - EXITOSO',3,'',34,6),
(1176,'2026-02-12 19:05:47.292304','25','admin_testing@school.com - 2026-02-04 01:01:21.769549+00:00 - EXITOSO',3,'',34,6),
(1177,'2026-02-12 19:05:47.292347','24','admin_testing@school.com - 2026-02-04 00:59:09.561751+00:00 - EXITOSO',3,'',34,6),
(1178,'2026-02-12 19:05:47.292393','23','student_test_final@school.com - 2026-02-03 22:35:07.640380+00:00 - EXITOSO',3,'',34,6),
(1179,'2026-02-12 19:05:47.292436','22','student_test_final@school.com - 2026-02-03 22:02:12.648362+00:00 - EXITOSO',3,'',34,6),
(1180,'2026-02-12 19:05:47.292480','21','student_test_final@school.com - 2026-02-02 20:03:53.635945+00:00 - EXITOSO',3,'',34,6),
(1181,'2026-02-12 19:05:47.292523','20','admin_testing@school.com - 2026-02-02 20:01:52.403165+00:00 - EXITOSO',3,'',34,6),
(1182,'2026-02-12 19:05:47.292566','19','admin_testing@school.com - 2026-02-02 20:01:42.871815+00:00 - EXITOSO',3,'',34,6),
(1183,'2026-02-12 19:05:47.292610','18','admin_testing@school.com - 2026-02-01 03:47:55.810506+00:00 - EXITOSO',3,'',34,6),
(1184,'2026-02-12 19:05:47.292653','17','admin_testing@school.com - 2026-02-01 03:47:54.303952+00:00 - EXITOSO',3,'',34,6),
(1185,'2026-02-12 19:05:47.292696','16','student_test_final@school.com - 2026-02-01 03:47:53.520042+00:00 - EXITOSO',3,'',34,6),
(1186,'2026-02-12 19:05:47.292739','15','admin_testing@school.com - 2026-02-01 03:43:30.267408+00:00 - EXITOSO',3,'',34,6),
(1187,'2026-02-12 19:05:47.292782','14','admin_testing@school.com - 2026-02-01 03:43:01.929910+00:00 - EXITOSO',3,'',34,6),
(1188,'2026-02-12 19:05:47.292846','13','admin_testing@school.com - 2026-02-01 03:43:00.276688+00:00 - EXITOSO',3,'',34,6),
(1189,'2026-02-12 19:05:47.292890','12','student_test_final@school.com - 2026-02-01 03:42:59.444071+00:00 - EXITOSO',3,'',34,6),
(1190,'2026-02-12 19:05:47.292933','11','student_0_1468@test.com - 2026-02-01 03:39:19.673109+00:00 - EXITOSO',3,'',34,6),
(1191,'2026-02-12 19:05:47.292976','10','admin_testing@school.com - 2026-02-01 03:38:20.862849+00:00 - EXITOSO',3,'',34,6),
(1192,'2026-02-12 19:05:47.293019','9','admin_testing@school.com - 2026-02-01 03:37:56.623309+00:00 - EXITOSO',3,'',34,6),
(1193,'2026-02-12 19:05:47.293062','8','admin_testing@school.com - 2026-02-01 03:37:02.560193+00:00 - EXITOSO',3,'',34,6),
(1194,'2026-02-12 19:05:47.293105','7','admin_testing@school.com - 2026-02-01 03:37:00.828055+00:00 - EXITOSO',3,'',34,6),
(1195,'2026-02-12 19:05:47.293148','6','admin_testing@school.com - 2026-02-01 03:36:08.661284+00:00 - EXITOSO',3,'',34,6),
(1196,'2026-02-12 19:05:47.293192','5','admin_testing@school.com - 2026-02-01 03:36:07.090642+00:00 - EXITOSO',3,'',34,6),
(1197,'2026-02-12 19:05:47.293234','4','admin_testing@school.com - 2026-02-01 03:34:07.637996+00:00 - EXITOSO',3,'',34,6),
(1198,'2026-02-12 19:05:47.293277','3','admin_testing@school.com - 2026-02-01 03:33:19.705030+00:00 - EXITOSO',3,'',34,6),
(1199,'2026-02-12 19:05:47.293318','2','admin_testing@school.com - 2026-02-01 03:32:48.603355+00:00 - EXITOSO',3,'',34,6),
(1200,'2026-02-12 19:05:47.293361','1','hectorino2789@gmail.com - 2026-01-30 19:27:15.185009+00:00 - EXITOSO',3,'',34,6),
(1201,'2026-02-16 19:39:33.034188','5','HECTOR ADRIAN MARTINEZ HERRERA JSJS',2,'[{\"changed\": {\"fields\": [\"Nombre\", \"Apellido paterno\", \"Apellido materno\", \"Telefono\"]}}]',41,6);
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
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
(93,'academico','0002_remove_maestro_email_remove_materia_fecha_fin_and_more','2026-02-13 04:03:19.950148');
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
('ccav1j5uzzqj7q5k90m7to4vc7nvv9p2','.eJxVjDsOwjAQBe_iGln-rZ1Q0nMGa9dr4wBypDipEHeHSCmgfTPzXiLitta49bzEicVZeHH63QjTI7cd8B3bbZZpbusykdwVedAurzPn5-Vw_w4q9vqtIZfCLoHRqIPTiiyz8UgjKlJoDQckp4LSNoEOACpZBsfDAOxpLCTeH-wMN-M:1vqN2H:loWNOLSlGW7ZohYy2FHPhhvyZ3mfqxxOLcS5U8GjMWc','2026-02-26 03:06:33.808664'),
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
INSERT INTO `estudiantes` VALUES
(1000,'MAURICIO ANDRÉS','PADILLA','RIOS','Por el Centro',119,1,NULL,0.00,NULL,NULL,NULL,NULL,NULL),
(1001,'RAMIRO','PATADA','LECHUGA','{}',120,1,NULL,0.00,NULL,NULL,NULL,NULL,NULL),
(20240000,'Alumno','Test 0','Simulado','',131,1,NULL,0.00,NULL,NULL,NULL,NULL,NULL),
(20240001,'Alumno','Test 1','Simulado','',132,1,NULL,0.00,NULL,NULL,NULL,NULL,NULL),
(20240002,'Alumno','Test 2','Simulado','',133,1,NULL,0.00,NULL,NULL,NULL,NULL,NULL),
(20240003,'Alumno','Test 3','Simulado','',134,1,NULL,0.00,NULL,NULL,NULL,NULL,NULL),
(20240004,'Alumno','Test 4','Simulado','',135,1,NULL,0.00,NULL,NULL,NULL,NULL,NULL),
(20240005,'Alumno','Test 5','Simulado','',136,1,NULL,0.00,NULL,NULL,NULL,NULL,NULL),
(20240006,'Alumno','Test 6','Simulado','',137,1,NULL,0.00,NULL,NULL,NULL,NULL,NULL),
(20240007,'Alumno','Test 7','Simulado','',138,1,NULL,0.00,NULL,NULL,NULL,NULL,NULL),
(20240008,'Alumno','Test 8','Simulado','',139,1,NULL,0.00,NULL,NULL,NULL,NULL,NULL),
(20240009,'Alumno','Test 9','Simulado','',140,1,NULL,0.00,NULL,NULL,NULL,NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estudiantes_tutores`
--

LOCK TABLES `estudiantes_tutores` WRITE;
/*!40000 ALTER TABLE `estudiantes_tutores` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `estudiantes_tutores` VALUES
(14,'Madre','2026-02-12 18:11:23.744351',1,1001,1),
(15,'Padre','2026-02-12 18:59:51.647223',1,1000,2);
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
INSERT INTO `evaluaciones_socioeconomicas` VALUES
(71,'2026-02-12 18:07:27.687620',50000.00,'Ladrillo',3,'{}',NULL,'2026-02-12 18:07:27.687770',16,1000,'',0,16,'2027-02-12','',0,0,NULL),
(72,'2026-02-12 18:08:10.510357',50000.00,'Ladrillo',3,'{}',1,'2026-02-12 18:08:10.510466',16,1000,'',0,16,'2027-02-12','',0,0,NULL),
(73,'2026-02-12 18:12:00.143619',5000.00,'Ladrillo',4,'{}',1,'2026-02-12 18:12:00.143689',17,1001,'{}',0,17,NULL,'',0,0,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=358 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupos`
--

LOCK TABLES `grupos` WRITE;
/*!40000 ALTER TABLE `grupos` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `grupos` VALUES
(285,'A','',NULL,'2026-02-12 17:47:16.742590',28,30,25),
(286,'B','',NULL,'2026-02-12 17:47:16.746837',28,30,25),
(287,'C','',NULL,'2026-02-12 17:47:16.750362',28,30,25),
(288,'A','',NULL,'2026-02-12 17:47:16.753910',29,30,25),
(289,'B','',NULL,'2026-02-12 17:47:16.757461',29,30,25),
(290,'C','',NULL,'2026-02-12 17:47:16.761488',29,30,25),
(291,'A','',NULL,'2026-02-12 17:47:16.765087',30,30,25),
(292,'B','',NULL,'2026-02-12 17:47:16.768482',30,30,25),
(293,'C','',NULL,'2026-02-12 17:47:16.771927',30,30,25),
(294,'A','',NULL,'2026-02-12 17:47:16.776084',31,30,25),
(295,'B','',NULL,'2026-02-12 17:47:16.779572',31,30,25),
(296,'C','',NULL,'2026-02-12 17:47:16.782499',31,30,25),
(297,'A','',NULL,'2026-02-12 17:47:16.786532',32,30,25),
(298,'B','',NULL,'2026-02-12 17:47:16.790303',32,30,25),
(299,'C','',NULL,'2026-02-12 17:47:16.794358',32,30,25),
(300,'A','',NULL,'2026-02-12 17:47:16.798059',33,30,25),
(301,'B','',NULL,'2026-02-12 17:47:16.801711',33,30,25),
(302,'C','',NULL,'2026-02-12 17:47:16.805352',33,30,25),
(303,'A','',NULL,'2026-02-12 17:47:16.809149',34,30,25),
(304,'B','',NULL,'2026-02-12 17:47:16.811937',34,30,25),
(305,'C','',NULL,'2026-02-12 17:47:16.814182',34,30,25),
(306,'A','',NULL,'2026-02-12 17:47:16.816388',35,30,25),
(307,'B','',NULL,'2026-02-12 17:47:16.818652',35,30,25),
(308,'C','',NULL,'2026-02-12 17:47:16.820835',35,30,25),
(309,'A','',NULL,'2026-02-12 17:47:16.823229',36,30,25),
(310,'B','',NULL,'2026-02-12 17:47:16.826903',36,30,25),
(311,'C','',NULL,'2026-02-12 17:47:16.829581',36,30,25),
(312,'A','',NULL,'2026-02-12 17:47:16.832327',37,30,25),
(313,'B','',NULL,'2026-02-12 17:47:16.834948',37,30,25),
(314,'C','',NULL,'2026-02-12 17:47:16.837680',37,30,25),
(315,'A','',NULL,'2026-02-12 17:47:16.840155',38,30,25),
(316,'B','',NULL,'2026-02-12 17:47:16.843093',38,30,25),
(317,'C','',NULL,'2026-02-12 17:47:16.845901',38,30,25),
(318,'A','',NULL,'2026-02-12 17:47:16.848569',39,30,25),
(319,'B','',NULL,'2026-02-12 17:47:16.851308',39,30,25),
(320,'C','',NULL,'2026-02-12 17:47:16.853961',39,30,25),
(321,'A','',NULL,'2026-02-12 19:03:03.712249',28,30,26),
(322,'B','',NULL,'2026-02-12 19:03:03.718763',28,30,26),
(323,'C','',NULL,'2026-02-12 19:03:03.723318',28,30,26),
(324,'A','',NULL,'2026-02-12 19:03:03.727199',29,30,26),
(325,'B','',NULL,'2026-02-12 19:03:03.730476',29,30,26),
(326,'C','',NULL,'2026-02-12 19:03:03.733740',29,30,26),
(327,'A','',NULL,'2026-02-12 19:03:03.738079',30,30,26),
(328,'B','',NULL,'2026-02-12 19:03:03.742590',30,30,26),
(329,'C','',NULL,'2026-02-12 19:03:03.746134',30,30,26),
(330,'A','',NULL,'2026-02-12 19:03:03.749386',31,30,26),
(331,'B','',NULL,'2026-02-12 19:03:03.753050',31,30,26),
(332,'C','',NULL,'2026-02-12 19:03:03.757606',31,30,26),
(333,'A','',NULL,'2026-02-12 19:03:03.761238',32,30,26),
(334,'B','',NULL,'2026-02-12 19:03:03.764409',32,30,26),
(335,'C','',NULL,'2026-02-12 19:03:03.767734',32,30,26),
(336,'A','',NULL,'2026-02-12 19:03:03.771402',33,30,26),
(337,'B','',NULL,'2026-02-12 19:03:03.775328',33,30,26),
(338,'C','',NULL,'2026-02-12 19:03:03.778581',33,30,26),
(339,'A','',NULL,'2026-02-12 19:03:03.781720',34,30,26),
(340,'B','',NULL,'2026-02-12 19:03:03.784986',34,30,26),
(341,'C','',NULL,'2026-02-12 19:03:03.788628',34,30,26),
(342,'A','',NULL,'2026-02-12 19:03:03.792716',35,30,26),
(343,'B','',NULL,'2026-02-12 19:03:03.796167',35,30,26),
(344,'C','',NULL,'2026-02-12 19:03:03.799145',35,30,26),
(345,'A','',NULL,'2026-02-12 19:03:03.802303',36,30,26),
(346,'B','',NULL,'2026-02-12 19:03:03.805452',36,30,26),
(347,'C','',NULL,'2026-02-12 19:03:03.808362',36,30,26),
(348,'A','',NULL,'2026-02-12 19:03:03.811127',37,30,26),
(349,'B','',NULL,'2026-02-12 19:03:03.813705',37,30,26),
(350,'C','',NULL,'2026-02-12 19:03:03.816369',37,30,26),
(351,'A','',NULL,'2026-02-12 19:03:03.819984',38,30,26),
(352,'B','',NULL,'2026-02-12 19:03:03.822862',38,30,26),
(353,'C','',NULL,'2026-02-12 19:03:03.825464',38,30,26),
(354,'A','',NULL,'2026-02-12 19:03:03.827986',39,30,26),
(355,'B','',NULL,'2026-02-12 19:03:03.830357',39,30,26),
(356,'C','',NULL,'2026-02-12 19:03:03.832733',39,30,26),
(357,'1-A','',NULL,'2026-02-13 04:30:34.473945',31,30,27);
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
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_estados_estudiante`
--

LOCK TABLES `historial_estados_estudiante` WRITE;
/*!40000 ALTER TABLE `historial_estados_estudiante` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `historial_estados_estudiante` VALUES
(89,'Alta automatica','2026-02-12 18:05:12.475403',1,1000,NULL,NULL),
(90,'Alta automatica','2026-02-12 18:11:23.742708',1,1001,NULL,NULL),
(91,'Generación automática de reinscripción - Ciclo CI-2024-2025','2026-02-13 04:44:12.708973',15,1000,NULL,NULL),
(92,'Generación automática de reinscripción - Ciclo CI-2024-2025','2026-02-13 04:44:12.718517',15,1001,NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscripciones`
--

LOCK TABLES `inscripciones` WRITE;
/*!40000 ALTER TABLE `inscripciones` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `inscripciones` VALUES
(92,'pendiente_pago','2026-02-12 18:05:12.473321',NULL,'2026-02-12 19:03:03.854219',NULL,1000,291),
(93,'pendiente_pago','2026-02-12 18:11:23.732025',NULL,'2026-02-12 19:03:03.876740',NULL,1001,301),
(94,'activo','2026-02-12 19:04:41.511554',NULL,'2026-02-12 19:04:41.511639',NULL,1000,330),
(95,'activo','2026-02-13 04:35:26.011422',NULL,'2026-02-13 04:35:26.011482',NULL,20240000,357),
(96,'activo','2026-02-13 04:35:26.023396',NULL,'2026-02-13 04:35:26.023453',NULL,20240001,357),
(97,'activo','2026-02-13 04:35:26.027850',NULL,'2026-02-13 04:35:26.027916',NULL,20240002,357),
(98,'activo','2026-02-13 04:35:26.031521',NULL,'2026-02-13 04:35:26.031557',NULL,20240003,357),
(99,'activo','2026-02-13 04:35:26.035398',NULL,'2026-02-13 04:35:26.035451',NULL,20240004,357),
(100,'activo','2026-02-13 04:35:26.039723',NULL,'2026-02-13 04:35:26.039761',NULL,20240005,357),
(101,'activo','2026-02-13 04:35:26.043526',NULL,'2026-02-13 04:35:26.043583',NULL,20240006,357),
(102,'activo','2026-02-13 04:35:26.047450',NULL,'2026-02-13 04:35:26.047504',NULL,20240007,357),
(103,'activo','2026-02-13 04:35:26.051465',NULL,'2026-02-13 04:35:26.051518',NULL,20240008,357),
(104,'activo','2026-02-13 04:35:26.055412',NULL,'2026-02-13 04:35:26.055464',NULL,20240009,357);
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
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_attempts`
--

LOCK TABLES `login_attempts` WRITE;
/*!40000 ALTER TABLE `login_attempts` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `login_attempts` VALUES
(72,'hectorino2789@gmail.com','127.0.0.1','2026-02-16 19:28:44.760045',1);
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
INSERT INTO `maestros` VALUES
(5,'HECTOR ADRIAN','MARTINEZ','HERRERA JSJS','440595839','2026-02-12',1,'2026-02-12 18:56:44.547395','2026-02-16 19:39:33.032259',2,1),
(6,'Maestro','Simulado 0','Test',NULL,'2024-01-01',1,'2026-02-13 04:30:28.264843','2026-02-13 04:30:28.264864',2,121),
(7,'Maestro','Simulado 1','Test',NULL,'2024-01-01',1,'2026-02-13 04:30:28.600301','2026-02-13 04:30:28.600323',2,122),
(8,'Maestro','Simulado 2','Test',NULL,'2024-01-01',1,'2026-02-13 04:30:28.933840','2026-02-13 04:30:28.933861',2,123),
(9,'Maestro','Simulado 3','Test',NULL,'2024-01-01',1,'2026-02-13 04:30:29.266171','2026-02-13 04:30:29.266191',2,124),
(10,'Maestro','Simulado 4','Test',NULL,'2024-01-01',1,'2026-02-13 04:30:29.599318','2026-02-13 04:30:29.599338',2,125),
(11,'Maestro','Simulado 5','Test',NULL,'2024-01-01',1,'2026-02-13 04:30:29.934600','2026-02-13 04:30:29.934621',2,126),
(12,'Maestro','Simulado 6','Test',NULL,'2024-01-01',1,'2026-02-13 04:30:30.269731','2026-02-13 04:30:30.269752',2,127),
(13,'Maestro','Simulado 7','Test',NULL,'2024-01-01',1,'2026-02-13 04:30:30.600256','2026-02-13 04:30:30.600278',2,128),
(14,'Maestro','Simulado 8','Test',NULL,'2024-01-01',1,'2026-02-13 04:30:30.930942','2026-02-13 04:30:30.930966',2,129),
(15,'Maestro','Simulado 9','Test',NULL,'2024-01-01',1,'2026-02-13 04:30:31.256574','2026-02-13 04:30:31.256595',2,130);
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materias`
--

LOCK TABLES `materias` WRITE;
/*!40000 ALTER TABLE `materias` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `materias` VALUES
(2,'Matemáticas','1','',18.00,1,1,'2026-02-12 18:19:58.368111','2026-02-12 18:19:58.368151',33,3),
(3,'Matemáticas','PRI1-0',NULL,0.00,1,0,'2026-02-13 04:30:27.880236','2026-02-13 04:30:27.880280',31,5),
(4,'Español','PRI1-1',NULL,0.00,1,1,'2026-02-13 04:30:27.893371','2026-02-13 04:30:27.893404',31,5),
(5,'Ciencias Naturales','PRI1-2',NULL,0.00,1,2,'2026-02-13 04:30:27.897949','2026-02-13 04:30:27.897983',31,5),
(6,'Historia','PRI1-3',NULL,0.00,1,3,'2026-02-13 04:30:27.906057','2026-02-13 04:30:27.906113',31,5),
(7,'Geografía','PRI1-4',NULL,0.00,1,4,'2026-02-13 04:30:27.911464','2026-02-13 04:30:27.911504',31,5),
(8,'Inglés','PRI1-5',NULL,0.00,1,5,'2026-02-13 04:30:27.916209','2026-02-13 04:30:27.916244',31,5);
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
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagos`
--

LOCK TABLES `pagos` WRITE;
/*!40000 ALTER TABLE `pagos` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `pagos` VALUES
(84,1500.00,'2026-02-12 19:04:41.487262','Efectivo',NULL,'{}','hectorino2789@gmail.com','{}',342),
(85,1500.00,'2026-02-13 04:35:26.151840','transferencia',NULL,NULL,'Simulador',NULL,344),
(86,1500.00,'2026-02-13 04:35:26.170184','transferencia',NULL,NULL,'Simulador',NULL,345),
(87,1500.00,'2026-02-13 04:35:26.186070','transferencia',NULL,NULL,'Simulador',NULL,346),
(88,1500.00,'2026-02-13 04:35:26.202246','transferencia',NULL,NULL,'Simulador',NULL,347),
(89,1500.00,'2026-02-13 04:35:26.220542','transferencia',NULL,NULL,'Simulador',NULL,348),
(90,1500.00,'2026-02-13 04:35:26.234098','transferencia',NULL,NULL,'Simulador',NULL,349),
(91,1500.00,'2026-02-13 04:35:26.247109','transferencia',NULL,NULL,'Simulador',NULL,350),
(92,1500.00,'2026-02-13 04:35:26.260371','transferencia',NULL,NULL,'Simulador',NULL,351),
(93,1500.00,'2026-02-13 04:35:26.274250','transferencia',NULL,NULL,'Simulador',NULL,352),
(94,1500.00,'2026-02-13 04:35:26.287802','transferencia',NULL,NULL,'Simulador',NULL,353);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `periodos_evaluacion`
--

LOCK TABLES `periodos_evaluacion` WRITE;
/*!40000 ALTER TABLE `periodos_evaluacion` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `periodos_evaluacion` VALUES
(2,1,'Enero-Febrero','2026-02-12','2026-04-16','2026-04-09','2026-04-16','ACTIVO','2026-02-12 18:03:17.454868','2026-02-12 18:18:46.687135',25,2),
(3,1,'Primer Trimestre','2024-08-01','2024-11-30','2024-11-23','2024-11-30','ACTIVO','2026-02-13 04:35:26.066804','2026-02-13 04:35:26.066830',27,5);
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
INSERT INTO `programas_educativos` VALUES
(2,'Programa educativo 2017 Preescolar','Es un programa educativo orientado a que los niños desarrollen sus capacidades motoras.','2026-02-12','2030-02-12',3,1,'2026-02-12 17:55:02.840167','2026-02-12 17:55:02.840198',1),
(3,'Programa Edcuativo 2017 - Primaria','','2026-02-12','2030-02-12',3,0,'2026-02-12 17:56:52.786354','2026-02-12 17:56:52.786379',2),
(4,'Programa Educativo Secundaria 2017','','2026-02-12','2030-02-12',3,1,'2026-02-12 18:01:08.658131','2026-02-12 18:01:08.658175',3),
(5,'Plan de Estudios Primaria 2024',NULL,'2024-01-01',NULL,3,1,'2026-02-13 04:16:30.358169','2026-02-13 04:16:30.358190',2);
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
(8,'2026-02-12 03:01:23.995154',14);
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
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

LOCK TABLES `token_blacklist_outstandingtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `token_blacklist_outstandingtoken` VALUES
(1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDg1NzAyMCwiaWF0IjoxNzcwNzcwNjIwLCJqdGkiOiIxZmM4NjNkYzc1OTI0NzhiYjQwNmRkODE3ZWE5YWEzZiIsInVzZXJfaWQiOiIxIn0.PaH_RMqA3nJdS-vBH5k7PwSwARsb1DpBKMuOgG3P2wA','2026-02-11 00:43:40.139358','2026-02-12 00:43:40.000000',1,'1fc863dc7592478bb406dd817ea9aa3f'),
(2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDg1NzIzMywiaWF0IjoxNzcwNzcwODMzLCJqdGkiOiJmN2QxYTI0ZmIxNDA0NjI0YTJiOWUwOWQyOWY5YTU2NiIsInVzZXJfaWQiOiI2In0.TUBKZlw4WJzwqzotA5PM8AEkAnDQDrW0IJe5pGbzw7M','2026-02-11 00:47:13.048476','2026-02-12 00:47:13.000000',6,'f7d1a24fb1404624a2b9e09d29f9a566'),
(3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDg1NzI0NCwiaWF0IjoxNzcwNzcwODQ0LCJqdGkiOiI5MTZjODlmNzlmOGE0NmE1OWE1ODA1ZTQ5MTExMjI3NCIsInVzZXJfaWQiOiI2In0.z_6BuWgaVE_s89x4jZWSUqrFRRwaf4qUSOgSdppJb6M','2026-02-11 00:47:24.315906','2026-02-12 00:47:24.000000',6,'916c89f79f8a46a59a5805e491112274'),
(4,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDg1NzYyMSwiaWF0IjoxNzcwNzcxMjIxLCJqdGkiOiJlYmRhNzQ0Nzc1MzM0MzFmOTFhYWZhNWNhYmUzY2Q3ZiIsInVzZXJfaWQiOiIxIn0.r1TOx0LkaRs6PpKqjzvPBendUAVEKivNG7AHnnRSl0Q','2026-02-11 00:53:41.184920','2026-02-12 00:53:41.000000',1,'ebda74477533431f91aafa5cabe3cd7f'),
(5,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDg1ODAwNCwiaWF0IjoxNzcwNzcxNjA0LCJqdGkiOiJlMTEzNzVjOGFkMTE0ZTA1OGE5ODQ4NWM5Y2QyZjE1ZCIsInVzZXJfaWQiOiI2In0.h02WSk-nGbunfrZvbmiWnmPOalfqBw3p_BSWwmvunfY','2026-02-11 01:00:04.151361','2026-02-12 01:00:04.000000',6,'e11375c8ad114e058a98485c9cd2f15d'),
(6,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDg1ODAxNSwiaWF0IjoxNzcwNzcxNjE1LCJqdGkiOiJkOTNjNmRjNmNhOTM0YjhmYjYwZjEwMGU0OWRlZjQwYiIsInVzZXJfaWQiOiI2In0.wUSgnaiv7AZbDZ0RilvqqFAu15mH_5t7ktdYYT-JpjQ','2026-02-11 01:00:15.209920','2026-02-12 01:00:15.000000',6,'d93c6dc6ca934b8fb60f100e49def40b'),
(7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDg1ODQ3NSwiaWF0IjoxNzcwNzcyMDc1LCJqdGkiOiIwYmRkNGIxYmMwMGU0YmQwODdiM2M3NWEwNTM0ZDU2OSIsInVzZXJfaWQiOiI3NyJ9.FE9KN3ajpXlv5aYlzhsUAFa-9NzB9aGVgd2CVqpLFUE','2026-02-11 01:07:55.022307','2026-02-12 01:07:55.000000',NULL,'0bdd4b1bc00e4bd087b3c75a0534d569'),
(8,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk0NzcyNSwiaWF0IjoxNzcwODYxMzI1LCJqdGkiOiI0ZDk2NDQ3NzI4NzU0MDgwODI0OWJjODIwNmFiODFmYyIsInVzZXJfaWQiOiIxIn0.uLKWbNLEXYkka61deGuu-8ErqspC8cxGmUpan06Pnqs','2026-02-12 01:55:25.527644','2026-02-13 01:55:25.000000',1,'4d964477287540808249bc8206ab81fc'),
(9,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk0Nzc1OSwiaWF0IjoxNzcwODYxMzU5LCJqdGkiOiIzOWNhNzkyYTA5MjA0ZGZlYjA4OTExMzk4ZGRhODUyOCIsInVzZXJfaWQiOiI2In0.icptsUd5FAfjMv1zh3yGhyCEFNdj1XnHeM9pawX-UHw','2026-02-12 01:55:59.919935','2026-02-13 01:55:59.000000',6,'39ca792a09204dfeb08911398dda8528'),
(10,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk0Nzc3MCwiaWF0IjoxNzcwODYxMzcwLCJqdGkiOiI5M2U2MzgyNzYwN2E0OTUwYjk2NTNkZTZmZmRiY2RiYiIsInVzZXJfaWQiOiI2In0.yQgPcQ6Gs5uaGTCzn_Ecd0oIhsME8aQdDuXYMvUpyqw','2026-02-12 01:56:10.171093','2026-02-13 01:56:10.000000',6,'93e63827607a4950b9653de6ffdbcdbb'),
(11,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk0OTQ1OCwiaWF0IjoxNzcwODYzMDU4LCJqdGkiOiIwNGIzYzY0Y2Q0ZTk0ODQwYWUwYjRhNTc5OTk4YTM2MyIsInVzZXJfaWQiOiIxIn0.fXcvER_Jko4bTJDKG2VDTBbdhS8AmDUARoWFanNvb2s','2026-02-12 02:24:18.438980','2026-02-13 02:24:18.000000',1,'04b3c64cd4e94840ae0b4a579998a363'),
(12,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk1MTE2MSwiaWF0IjoxNzcwODY0NzYxLCJqdGkiOiI0NTQ1ODQ1ZGRlNzU0MmQzODNiYTZjNzdkZGY4OGI2ZCIsInVzZXJfaWQiOiI5NSJ9.Z_e6fL7-uCCinpgMaNIJvenZepj3h9WdwPGwTY2K4Ic','2026-02-12 02:52:41.926366','2026-02-13 02:52:41.000000',NULL,'4545845dde7542d383ba6c77ddf88b6d'),
(13,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk1MTMxMywiaWF0IjoxNzcwODY0OTEzLCJqdGkiOiIxMzk0NWFjYmRhMGI0NDJkYjA2YjBhNDQxZDUzNzEzYSIsInVzZXJfaWQiOiIxIn0.hMWdJ4Xdiv34MvIi_hLCxhvwN_q5HrlMIzPnTHjl204','2026-02-12 02:55:13.529990','2026-02-13 02:55:13.000000',1,'13945acbda0b442db06b0a441d53713a'),
(14,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk1MTM2NSwiaWF0IjoxNzcwODY0OTY1LCJqdGkiOiI2YWY2NjQyYzMwMGI0MGIyODY3ZjllMDMyYTQ0ZGQ2OCIsInVzZXJfaWQiOiIxNyJ9.TIrXdhFgwMjeRaRBoR_Jld2pLY8tNgILi0fFRVfTMFk','2026-02-12 02:56:05.307854','2026-02-13 02:56:05.000000',NULL,'6af6642c300b40b2867f9e032a44dd68'),
(15,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk1MTM3NywiaWF0IjoxNzcwODY0OTc3LCJqdGkiOiJkODYyYjI3NDViNGQ0MmIyODg5MDhiYjUyZWVhNjlkMyIsInVzZXJfaWQiOiIxNyJ9.4Nrxm9tvnE9bdPINDJRv5pwpM_HUq5XPeWmI3AcVN6o','2026-02-12 02:56:17.537267','2026-02-13 02:56:17.000000',NULL,'d862b2745b4d42b288908bb52eea69d3'),
(16,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MDk1MjAwMCwiaWF0IjoxNzcwODY1NjAwLCJqdGkiOiI1MTc3N2U0Y2QwMTI0MzE3YTA5ODg0NzM4N2Y0OWMyMyIsInVzZXJfaWQiOiI5MiJ9.VYRqjTT7hV7x4zWzAA2TYYrlSnCpr4aHIpxMft65QIM','2026-02-12 03:06:40.635682','2026-02-13 03:06:40.000000',NULL,'51777e4cd0124317a098847387f49c23'),
(17,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTAwOTE1MiwiaWF0IjoxNzcwOTIyNzUyLCJqdGkiOiIzZWNhNmRlNDdjYzI0OGU1ODgxMWYwMmFhNDJiMGZmZiIsInVzZXJfaWQiOiIxMTkifQ.0_E92ozjILWTQuA-QLmjKC2S3CeXb8U3kWhKVCQll-E','2026-02-12 18:59:12.132705','2026-02-13 18:59:12.000000',119,'3eca6de47cc248e58811f02aa42b0fff'),
(18,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTM1NjUyNCwiaWF0IjoxNzcxMjcwMTI0LCJqdGkiOiI0N2U0ZTBkZjk3YzU0YTJlODA3YzdiMWQ4M2MyNTg5ZCIsInVzZXJfaWQiOiI2In0.g-5MilYPW1egkcfNk6SAoP37QPiNSTVsxDr8bwNkOc4','2026-02-16 19:28:44.746680','2026-02-17 19:28:44.000000',6,'47e4e0df97c54a2e807c7b1d83c2589d');
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
  `foto_fachada_domicilio` varchar(255) DEFAULT NULL,
  `ine_tutor` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_tutoradm_nombre_completo` (`apellido_paterno`,`apellido_materno`,`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=141 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user`
--

LOCK TABLES `users_user` WRITE;
/*!40000 ALTER TABLE `users_user` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `users_user` VALUES
(1,'pbkdf2_sha256$1200000$BdRdKPGB23ZwVKyaIokOhT$hqpR4oXNRfRoHnfitTcLbusdCZpgA8rKWD07GtbXpGo=',NULL,'adancpphack@gmail.com','HECTOR ADAN','estudiante',0,0,'adan',NULL,NULL,0),
(6,'pbkdf2_sha256$1200000$PYfy8QfRclfAEDompWnClV$LsWUIxjl1GT6mA+kwu9DAhVNelAA4tkgQS8h/cyh3PY=','2026-01-30 19:28:10.951371','hectorino2789@gmail.com','Adancito','administrador',1,1,'adanov21','154284','2026-02-16 19:30:44.761867',1),
(96,'',NULL,'test@student.com','','estudiante',1,0,'test_student',NULL,NULL,0),
(119,'pbkdf2_sha256$1200000$u6sHzPe1KYFWaHdu90vWNf$wGroISdKocrxDqhMhvAp8E/slexCvXoNGdRGmCoGNco=',NULL,'padilla@gmail.com','MAURICIO ANDRÉS PADILLA','estudiante',1,0,'LMHA047828HDGRRCC8',NULL,NULL,0),
(120,'pbkdf2_sha256$1200000$xbDpiL5GAxqCL0yqazOEiI$1yiVemT9K32xV/RNV6gfbIrkUM7BPwuJo6cVHMH7JqA=',NULL,'ramiro@gmail.com','RAMIRO PATADA','estudiante',1,0,'DJDK048592KRDUUFA9',NULL,NULL,0),
(121,'pbkdf2_sha256$1200000$tnLlVLisBcQIKqGeXLLxSg$LOD2nJ3VqSKnvMB5FUTZ2TG4t8uvuDzClm7huwxBVTQ=',NULL,'maestro0@sms.edu','Maestro 0','maestro',1,0,'maestro0',NULL,NULL,0),
(122,'pbkdf2_sha256$1200000$u0kAF7SbL241rDLiUDP10C$+W0r61BcONaPpbfGzOyiYiaSqEVDfvD3mWton+rzJxU=',NULL,'maestro1@sms.edu','Maestro 1','maestro',1,0,'maestro1',NULL,NULL,0),
(123,'pbkdf2_sha256$1200000$ZIyH5yCE4F7DuKOrEvbObz$+xkgZMMWKXhjQqXau3L63I13JCwU9s1d5y8Q8F+kFec=',NULL,'maestro2@sms.edu','Maestro 2','maestro',1,0,'maestro2',NULL,NULL,0),
(124,'pbkdf2_sha256$1200000$HbSR9vHgQ0ajlt5WGXtc0v$p29eOTUV4xupNutr6OxCd653Vko5VlNLYoGyKuugb10=',NULL,'maestro3@sms.edu','Maestro 3','maestro',1,0,'maestro3',NULL,NULL,0),
(125,'pbkdf2_sha256$1200000$YKADvXiUPLvSakJhXVlWmY$D2mE3bA7L+Jscm3v2YesvixQSyy/VYwpoe6MO5x7GUA=',NULL,'maestro4@sms.edu','Maestro 4','maestro',1,0,'maestro4',NULL,NULL,0),
(126,'pbkdf2_sha256$1200000$UZdBwiWjQoCr40bK5yutVc$Nw2rpwuR/BNbsxU74nSQlwXxF9gFdYIluXVSXv7dIes=',NULL,'maestro5@sms.edu','Maestro 5','maestro',1,0,'maestro5',NULL,NULL,0),
(127,'pbkdf2_sha256$1200000$y2WFz78lPfg1ALo3qMlt6x$CT/sbqo/EgKzmYR2En6CYcqq1OfnMeKD3PpDVhck/m8=',NULL,'maestro6@sms.edu','Maestro 6','maestro',1,0,'maestro6',NULL,NULL,0),
(128,'pbkdf2_sha256$1200000$RJuFkXKsRVlTjhPHztBsLa$Y2joaJseArK8CQSLFwXMKXq9iC2wGVckyldskb/jI6Y=',NULL,'maestro7@sms.edu','Maestro 7','maestro',1,0,'maestro7',NULL,NULL,0),
(129,'pbkdf2_sha256$1200000$8lcdoWGJBpphq5xfFl97eK$QXwT7U79hesXIbsFp9N2/IaxnyDSlWEKIgeE8rD6T2Y=',NULL,'maestro8@sms.edu','Maestro 8','maestro',1,0,'maestro8',NULL,NULL,0),
(130,'pbkdf2_sha256$1200000$2mouTESBeYIvhxLFuUbMOP$mSfB7P5IFE2nl0p8zrCqRaIoaZlAcQUkkLDlDgP/YQ4=',NULL,'maestro9@sms.edu','Maestro 9','maestro',1,0,'maestro9',NULL,NULL,0),
(131,'pbkdf2_sha256$1200000$hTt9J4w3oyjqmkjLckjubh$gX+UYMBAZotog0QzsuFj3HCeAAW9OiTXMPZkOZ35gpk=',NULL,'alumno0@sms.edu','Alumno 0','estudiante',1,0,'CURP00000ALUMNO',NULL,NULL,0),
(132,'pbkdf2_sha256$1200000$Zfo55cPe6kmmGZamHU7GNM$v99CzTNzJO6u03ybQ3vR3Cc0w2H2k9RJubYKdmHjTWM=',NULL,'alumno1@sms.edu','Alumno 1','estudiante',1,0,'CURP00001ALUMNO',NULL,NULL,0),
(133,'pbkdf2_sha256$1200000$9siwVsjow3J57zNw8de135$H+9g2P0BufzIlUq3S8j5ojMy6CbQqk+yJGBP2VI6sjw=',NULL,'alumno2@sms.edu','Alumno 2','estudiante',1,0,'CURP00002ALUMNO',NULL,NULL,0),
(134,'pbkdf2_sha256$1200000$Odcqq4uvaM3Vrce2cugKeo$ZJfSPXCRZbic/sf7kcL164NmLZEdMZPqvtKRUf9GyVk=',NULL,'alumno3@sms.edu','Alumno 3','estudiante',1,0,'CURP00003ALUMNO',NULL,NULL,0),
(135,'pbkdf2_sha256$1200000$5SFDN1EqtVeieV3ssNdyhO$ZY++d3N1vdNw+m3QoNFx6q5fer0ZqNlMs0C//SyYzLI=',NULL,'alumno4@sms.edu','Alumno 4','estudiante',1,0,'CURP00004ALUMNO',NULL,NULL,0),
(136,'pbkdf2_sha256$1200000$XoP2DqJ1hIZ8E4ZQ65MP1v$h9avPxqdAkaRP/WOKcsrzjBh6Z4KxxMSGJyB1suoifI=',NULL,'alumno5@sms.edu','Alumno 5','estudiante',1,0,'CURP00005ALUMNO',NULL,NULL,0),
(137,'pbkdf2_sha256$1200000$tauIppCBAcDRkQ70BPljAK$o5nPblWIs879Ry7kzIN2NCzVf8KMBR6ZejIZBTF4erQ=',NULL,'alumno6@sms.edu','Alumno 6','estudiante',1,0,'CURP00006ALUMNO',NULL,NULL,0),
(138,'pbkdf2_sha256$1200000$RzP03q3R3ETRdHVFewEGFI$A9wzMV+DUXFQOih0W6A1FBChpwieXkT72JPOs3ImktI=',NULL,'alumno7@sms.edu','Alumno 7','estudiante',1,0,'CURP00007ALUMNO',NULL,NULL,0),
(139,'pbkdf2_sha256$1200000$PGHEcxMF4QAftRNAcrzaeZ$XUxw4Xm/39EyRqw5rw/HCmi3Wb4XfngQ92zRktmWkgw=',NULL,'alumno8@sms.edu','Alumno 8','estudiante',1,0,'CURP00008ALUMNO',NULL,NULL,0),
(140,'pbkdf2_sha256$1200000$9C8hxELjhWrHoKitkBU1dD$2tVM7jSF3UHJiRYW6wPf7QDWx9ery0BR9gNKc8QDcbM=',NULL,'alumno9@sms.edu','Alumno 9','estudiante',1,0,'CURP00009ALUMNO',NULL,NULL,0);
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
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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

-- Dump completed on 2026-02-16 13:42:01
