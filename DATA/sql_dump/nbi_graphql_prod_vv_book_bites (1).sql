-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: localhost    Database: nbi_graphql_prod
-- ------------------------------------------------------
-- Server version	5.7.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `vv_book_bites`
--

DROP TABLE IF EXISTS `vv_book_bites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vv_book_bites` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `amazon_link` varchar(255) DEFAULT NULL,
  `audio` varchar(255) DEFAULT NULL,
  `audio_key` varchar(255) DEFAULT NULL,
  `duration` varchar(255) NOT NULL,
  `author_image` varchar(255) DEFAULT NULL,
  `author_image_key` varchar(255) DEFAULT NULL,
  `author_name` varchar(255) NOT NULL,
  `description` varchar(60000) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL,
  `updated_at` timestamp NOT NULL,
  `featured` tinyint(1) NOT NULL DEFAULT '0',
  `release_date` date NOT NULL,
  `is_premium` tinyint(1) NOT NULL DEFAULT '0',
  `type` varchar(255) DEFAULT NULL,
  `publish_date` date NOT NULL,
  `featured_start_date` date DEFAULT NULL,
  `featured_end_date` date DEFAULT NULL,
  `author_image_webp` varchar(255) DEFAULT NULL,
  `author_last_name` varchar(255) DEFAULT NULL,
  `featured_start_at` timestamp NULL DEFAULT NULL,
  `featured_end_at` timestamp NULL DEFAULT NULL,
  `publish_at` timestamp NULL DEFAULT NULL,
  `release_at` timestamp NULL DEFAULT NULL,
  `likes` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_vv_book_bites_id_type` (`id`,`type`),
  KEY `GLOBAL_SEARCH_OPTIMIZE` (`title`,`author_name`),
  KEY `index_release_date` (`release_date`),
  KEY `index_id` (`id`,`author_name`),
  KEY `idx_vv_book_bites_author_name` (`author_name`),
  KEY `Index_for_sorting` (`id`,`audio_key`,`created_at`,`updated_at`),
  KEY `idx_vv_book_bites_id_audio_key_created_at_type` (`id`,`audio_key`,`created_at`,`type`)
) ENGINE=InnoDB AUTO_INCREMENT=907 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-10 11:17:49
