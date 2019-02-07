-- MySQL dump 10.16  Distrib 10.1.37-MariaDB, for debian-linux-gnueabihf (armv8l)
--
-- Host: localhost    Database: bhash
-- ------------------------------------------------------
-- Server version	10.1.37-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bh_posts`
--

DROP TABLE IF EXISTS `bh_posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bh_posts` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `bh_user` int(10) unsigned DEFAULT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `content` longtext,
  PRIMARY KEY (`id`),
  KEY `k_fresh` (`created`),
  KEY `k_user` (`bh_user`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bh_posts_tags`
--

DROP TABLE IF EXISTS `bh_posts_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bh_posts_tags` (
  `bh_post` int(10) unsigned NOT NULL,
  `bh_tag` varchar(128) NOT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`bh_tag`,`bh_post`),
  KEY `k_fresh` (`created`),
  KEY `k_post` (`bh_post`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bh_sessions`
--

DROP TABLE IF EXISTS `bh_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bh_sessions` (
  `bh_user` int(10) unsigned DEFAULT NULL,
  `token` varchar(64) NOT NULL,
  `outofdate` datetime DEFAULT NULL,
  UNIQUE KEY `token` (`token`),
  KEY `i_session` (`bh_user`,`outofdate`),
  CONSTRAINT `c_user` FOREIGN KEY (`bh_user`) REFERENCES `bh_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bh_tags`
--

DROP TABLE IF EXISTS `bh_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bh_tags` (
  `tag` varchar(128) NOT NULL,
  `lastUsed` datetime DEFAULT CURRENT_TIMESTAMP,
  `lastTrend` datetime DEFAULT CURRENT_TIMESTAMP,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `hot` int(10) unsigned DEFAULT '1',
  PRIMARY KEY (`tag`),
  KEY `k_fresh` (`lastUsed`),
  KEY `k_hot` (`hot`),
  KEY `k_trend` (`lastTrend`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bh_users`
--

DROP TABLE IF EXISTS `bh_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bh_users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(32) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `verified` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-04 16:17:59
