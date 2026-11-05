-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: agriculture_db
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `crop_records`
--

DROP TABLE IF EXISTS `crop_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crop_records` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `crop_id` int NOT NULL,
  `region_id` int NOT NULL,
  `year` int NOT NULL,
  `cultivated_area_ha` decimal(12,2) NOT NULL,
  `production_tonnes` decimal(12,2) NOT NULL,
  `rainfall_mm` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`record_id`),
  KEY `crop_id` (`crop_id`),
  KEY `region_id` (`region_id`),
  CONSTRAINT `crop_records_ibfk_1` FOREIGN KEY (`crop_id`) REFERENCES `crops` (`crop_id`),
  CONSTRAINT `crop_records_ibfk_2` FOREIGN KEY (`region_id`) REFERENCES `regions` (`region_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crop_records`
--

LOCK TABLES `crop_records` WRITE;
/*!40000 ALTER TABLE `crop_records` DISABLE KEYS */;
INSERT INTO `crop_records` VALUES (1,1,1,2021,1000.00,4000.00,850.00),(2,1,1,2022,1100.00,4620.00,900.00),(3,1,1,2023,1200.00,5040.00,880.00),(4,1,2,2021,800.00,3200.00,780.00),(5,1,2,2022,850.00,3570.00,820.00),(6,1,2,2023,900.00,3870.00,800.00),(7,2,3,2021,600.00,1800.00,650.00),(8,2,3,2022,650.00,2080.00,680.00),(9,2,3,2023,700.00,2310.00,700.00),(10,3,2,2021,700.00,1400.00,720.00),(11,3,2,2022,750.00,1575.00,760.00),(12,3,2,2023,800.00,1680.00,740.00),(13,4,4,2021,500.00,2500.00,900.00),(14,4,4,2022,550.00,2860.00,920.00),(15,4,4,2023,600.00,3180.00,910.00),(16,5,5,2021,400.00,28000.00,1000.00),(17,5,5,2022,420.00,30240.00,1050.00),(18,5,5,2023,450.00,33300.00,1020.00);
/*!40000 ALTER TABLE `crop_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crops`
--

DROP TABLE IF EXISTS `crops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crops` (
  `crop_id` int NOT NULL AUTO_INCREMENT,
  `crop_name` varchar(100) NOT NULL,
  PRIMARY KEY (`crop_id`),
  UNIQUE KEY `crop_name` (`crop_name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crops`
--

LOCK TABLES `crops` WRITE;
/*!40000 ALTER TABLE `crops` DISABLE KEYS */;
INSERT INTO `crops` VALUES (3,'Cotton'),(4,'Maize'),(1,'Rice'),(5,'Sugarcane'),(2,'Wheat');
/*!40000 ALTER TABLE `crops` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `regions`
--

DROP TABLE IF EXISTS `regions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `regions` (
  `region_id` int NOT NULL AUTO_INCREMENT,
  `region_name` varchar(100) NOT NULL,
  PRIMARY KEY (`region_id`),
  UNIQUE KEY `region_name` (`region_name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regions`
--

LOCK TABLES `regions` WRITE;
/*!40000 ALTER TABLE `regions` DISABLE KEYS */;
INSERT INTO `regions` VALUES (1,'Andhra Pradesh'),(3,'Karnataka'),(5,'Maharashtra'),(4,'Tamil Nadu'),(2,'Telangana');
/*!40000 ALTER TABLE `regions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-25 13:27:12
