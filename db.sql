-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: localhost    Database: web
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES UTF8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `author`
--

DROP TABLE IF EXISTS `author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `profile` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `author`
--

LOCK TABLES `author` WRITE;
/*!40000 ALTER TABLE `author` DISABLE KEYS */;
INSERT INTO `author` VALUES (1,'egoing','developer','a59b62a99fbd7ef95764938d84da1dda982c47ce6472190f914619a81ebb8e7b'),(2,'duru','database administrator','4347387e3d00dad3c0243cc440d090e2da18941d3f93974edd064db967b879a5'),(3,'taeho','data scientist, developer','c26140f0e41bb57687f9c58d4b25875e0c1e4d25f31cf91efb39a0fc9ab7dace'),(4,'sookbu ','data engineer, developer','82b6fba55af363a284dd6c6bbca588ad6116f08bbd9d3d2b2aa9c1e0815c66c3'),(6,'sumin','engineer','111111'),(7,'duru','engineer','bcb15f821479b4d5772bd0ca866c00ad5f926e3580720659cc80d39c9d09802a'),(8,'duru','engineer','bcb15f821479b4d5772bd0ca866c00ad5f926e3580720659cc80d39c9d09802a'),(9,'duru','engineer','bcb15f821479b4d5772bd0ca866c00ad5f926e3580720659cc80d39c9d09802a'),(10,'duru','engineer','bcb15f821479b4d5772bd0ca866c00ad5f926e3580720659cc80d39c9d09802a');
/*!40000 ALTER TABLE `author` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `page`
--

DROP TABLE IF EXISTS `page`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `page` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `page`
--

LOCK TABLES `page` WRITE;
/*!40000 ALTER TABLE `page` DISABLE KEYS */;
/*!40000 ALTER TABLE `page` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES (1,'dd','ee'),(2,'노랭이','노래요'),(3,'NEW','새거'),(4,'초록','초록색이다아'),(5,'모나미룩','제가 싸인펜이 된 것 같아요'),(6,'옷장 옷','너무 낡았는데요?'),(7,'NEW','새거요요요'),(8,'점프슈트','이뻐요'),(9,'맥코드','색깔이 마음에 드네요'),(10,'옷이','이뻐요'),(11,'블라우스','모델이 입어서 이쁜것 같아요');
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topic`
--

DROP TABLE IF EXISTS `topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `created` datetime NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic`
--

LOCK TABLES `topic` WRITE;
/*!40000 ALTER TABLE `topic` DISABLE KEYS */;
INSERT INTO `topic` VALUES (1,'MySQL','MySQL is...','2018-01-01 12:10:11',1),(2,'Oracle','Oracle is ...','2018-01-03 13:01:10',1),(3,'SQL Server','SQL Server is ...','2018-01-20 11:01:10',2),(4,'PostgreSQL','PostgreSQL is ...','2018-01-23 01:03:03',3),(5,'MongoDB','MongoDB is ...','2018-01-30 12:31:03',1),(6,'Python','Python is ...','2020-04-20 12:31:03',4),(7,'Flask','Flask is ...','2020-04-21 12:31:03',4),(10,'노랭이','너무 밝아요 ','2020-04-27 10:32:12',4),(11,'노랭이','너무 밝아요','2020-04-27 10:32:20',4),(12,'dd','ㄹㄹㄹ','2020-04-27 10:33:35',4),(13,'','','2020-04-27 10:33:35',4),(14,'','','2020-04-27 10:33:36',4),(15,'ㄹㄹㄹ','ㄹㄹㄹ','2020-04-27 10:33:39',4),(16,'','','2020-04-27 10:33:39',4),(17,'','','2020-04-27 10:33:40',4),(18,'노랭이','너무 밝아요','2020-04-27 10:34:43',4),(19,'노랭이','ddd','2020-04-27 10:38:24',4);
/*!40000 ALTER TABLE `topic` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-27 16:02:43
