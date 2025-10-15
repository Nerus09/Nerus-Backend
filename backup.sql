-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: localhost    Database: nerus
-- ------------------------------------------------------
-- Server version	8.0.43-0ubuntu0.24.04.2

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
-- Table structure for table `certificados`
--

DROP TABLE IF EXISTS `certificados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `solucao_id` int NOT NULL,
  `user_id` int NOT NULL,
  `problema_id` int NOT NULL,
  `empresa_id` int NOT NULL,
  `codigo_verificacao` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `titulo` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descricao` text COLLATE utf8mb4_unicode_ci,
  `url_certificado` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `data_emissao` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo_verificacao` (`codigo_verificacao`),
  KEY `solucao_id` (`solucao_id`),
  KEY `problema_id` (`problema_id`),
  KEY `empresa_id` (`empresa_id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_codigo` (`codigo_verificacao`),
  CONSTRAINT `certificados_ibfk_1` FOREIGN KEY (`solucao_id`) REFERENCES `solucoes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `certificados_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `certificados_ibfk_3` FOREIGN KEY (`problema_id`) REFERENCES `problemas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `certificados_ibfk_4` FOREIGN KEY (`empresa_id`) REFERENCES `empresas` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificados`
--

LOCK TABLES `certificados` WRITE;
/*!40000 ALTER TABLE `certificados` DISABLE KEYS */;
/*!40000 ALTER TABLE `certificados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empresas`
--

DROP TABLE IF EXISTS `empresas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empresas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `senha_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nif` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `setor_atuacao` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descricao` text COLLATE utf8mb4_unicode_ci,
  `logo_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email_verificado` tinyint(1) DEFAULT '0',
  `token_verificacao` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `tamanho_empresa` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nif` (`nif`),
  KEY `idx_email` (`email`),
  KEY `idx_setor` (`setor_atuacao`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empresas`
--

LOCK TABLES `empresas` WRITE;
/*!40000 ALTER TABLE `empresas` DISABLE KEYS */;
INSERT INTO `empresas` VALUES (1,'Tech Solutions h6hg1id2','tech.solutions.h6hg1id2@test.com','$argon2id$v=19$m=65536,t=3,p=4$ck6J0TonhHBubW0NYWxtbQ$qwJul7/54kSwo0zejimchx+BQT0L85JXLL7dSeMlNk8','500h6hg1id2','Tecnologia',NULL,NULL,0,'Y3uZDIPlD4Qe3OckIliJTfoiLvpc9NQe6_LDbDeDc-Y',1,'2025-10-15 10:41:57','2025-10-15 10:41:57','pequena'),(2,'Tech Solutions 0v0gkhl4','tech.solutions.0v0gkhl4@test.com','$argon2id$v=19$m=65536,t=3,p=4$/z8HAACAEIJQKgUgpFTKmQ$m2IleTZ3xU+jGCJCRQAyUKnr+vNMVMneY6xYR6SMj7Q','5000v0gkhl4','Tecnologia','Empresa de teste especializada em desenvolvimento de software e IA - ATUALIZADO',NULL,0,'FCBOgkehUCC7oP_tFtxaWk5J7WL8IGm-uKmD0VC-n6M',1,'2025-10-15 11:01:47','2025-10-15 11:01:54','pequena'),(3,'Tech Solutions a5pc9362','tech.solutions.a5pc9362@test.com','$argon2id$v=19$m=65536,t=3,p=4$YmzN2bv3vleK8d57j3FOKQ$mNaXhgKCuKU4WdJLGr4lpkR3XxeK1vIqQitv+ajyhiY','500a5pc9362','Tecnologia','Empresa de teste especializada em desenvolvimento de software e IA - ATUALIZADO',NULL,0,'2-vjl20MSA-jhA-IU8i2DhDNH1GMhUKyLxQgkZVRIL8',1,'2025-10-15 11:34:53','2025-10-15 11:35:00','pequena'),(4,'Tech Solutions r1b5adqx','tech.solutions.r1b5adqx@test.com','$argon2id$v=19$m=65536,t=3,p=4$kdL6vxfCGCOkFIKw1ppTig$brtSzeHUgpv20R0oX7GtHO2Wntw64+dDFC6WSpzHdjM','500r1b5adqx','Tecnologia','Empresa de teste especializada em desenvolvimento de software e IA - ATUALIZADO',NULL,0,'wMvlxs4pleiQfMxzhsDCsHcibib39vyNFGbISkqjHgE',1,'2025-10-15 11:42:15','2025-10-15 11:42:25','pequena'),(5,'Tech Solutions ijff4lez','tech.solutions.ijff4lez@test.com','$argon2id$v=19$m=65536,t=3,p=4$/v9fK0XIeQ/hfG/NGQPgfA$DgcnrXPyc2p5lfU2dOP2rbhPYusBbE+LmeQ8oDFBWV0','500ijff4lez','Tecnologia','Empresa de teste especializada em desenvolvimento de software e IA - ATUALIZADO',NULL,0,'PRiOrKemr_n2413pQuJxW7DWkHNji8Ui24Kz33tbfNU',1,'2025-10-15 11:51:10','2025-10-15 11:51:19','pequena'),(6,'Tech Solutions qzu644n9','tech.solutions.qzu644n9@test.com','$argon2id$v=19$m=65536,t=3,p=4$G0PoXasVonROKeX831uLMQ$PcHd1+gMxoB3K7/aVbderx5EA+K5nNNOTqiw87H3E/E','500qzu644n9','Tecnologia','Empresa de teste especializada em desenvolvimento de software e IA - ATUALIZADO',NULL,0,'UMKdiNIewrEgDgZvFlbmIhUO4xGIIDiQg24nh3bbUqU',1,'2025-10-15 12:28:32','2025-10-15 12:28:38','pequena');
/*!40000 ALTER TABLE `empresas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `habilidades`
--

DROP TABLE IF EXISTS `habilidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `habilidades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `categoria` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descricao` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `habilidades`
--

LOCK TABLES `habilidades` WRITE;
/*!40000 ALTER TABLE `habilidades` DISABLE KEYS */;
INSERT INTO `habilidades` VALUES (1,'Python','Programação',NULL,'2025-10-14 10:04:03'),(2,'JavaScript','Programação',NULL,'2025-10-14 10:04:03'),(3,'React','Programação',NULL,'2025-10-14 10:04:03'),(4,'Node.js','Programação',NULL,'2025-10-14 10:04:03'),(5,'Design Gráfico','Design',NULL,'2025-10-14 10:04:03'),(6,'UI/UX Design','Design',NULL,'2025-10-14 10:04:03'),(7,'Marketing Digital','Marketing',NULL,'2025-10-14 10:04:03'),(8,'SEO','Marketing',NULL,'2025-10-14 10:04:03'),(9,'Gestão de Projetos','Gestão',NULL,'2025-10-14 10:04:03'),(10,'Análise de Dados','Dados',NULL,'2025-10-14 10:04:03');
/*!40000 ALTER TABLE `habilidades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs_atividade`
--

DROP TABLE IF EXISTS `logs_atividade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs_atividade` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `empresa_id` int DEFAULT NULL,
  `tipo_usuario` enum('user','empresa') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `acao` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `detalhes` json DEFAULT NULL,
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_agent` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `empresa_id` (`empresa_id`),
  KEY `idx_data` (`created_at`),
  KEY `idx_acao` (`acao`),
  CONSTRAINT `logs_atividade_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `logs_atividade_ibfk_2` FOREIGN KEY (`empresa_id`) REFERENCES `empresas` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_atividade`
--

LOCK TABLES `logs_atividade` WRITE;
/*!40000 ALTER TABLE `logs_atividade` DISABLE KEYS */;
INSERT INTO `logs_atividade` VALUES (1,7,NULL,'user','visualizar_problema','{\"problema_id\": 2}',NULL,NULL,'2025-10-15 11:35:03'),(2,8,NULL,'user','visualizar_problema','{\"problema_id\": 3}',NULL,NULL,'2025-10-15 11:42:29'),(3,9,NULL,'user','visualizar_problema','{\"problema_id\": 4}',NULL,NULL,'2025-10-15 11:51:22'),(4,10,NULL,'user','visualizar_problema','{\"problema_id\": 5}',NULL,NULL,'2025-10-15 12:28:40');
/*!40000 ALTER TABLE `logs_atividade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notificacoes`
--

DROP TABLE IF EXISTS `notificacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notificacoes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `empresa_id` int DEFAULT NULL,
  `tipo_destinatario` enum('user','empresa') COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `titulo` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mensagem` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `link` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lida` tinyint(1) DEFAULT '0',
  `data_leitura` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user` (`user_id`,`lida`),
  KEY `idx_empresa` (`empresa_id`,`lida`),
  CONSTRAINT `notificacoes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `notificacoes_ibfk_2` FOREIGN KEY (`empresa_id`) REFERENCES `empresas` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificacoes`
--

LOCK TABLES `notificacoes` WRITE;
/*!40000 ALTER TABLE `notificacoes` DISABLE KEYS */;
/*!40000 ALTER TABLE `notificacoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `premios`
--

DROP TABLE IF EXISTS `premios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `premios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `problema_id` int NOT NULL,
  `user_id` int NOT NULL,
  `solucao_id` int NOT NULL,
  `tipo_premio` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descricao` text COLLATE utf8mb4_unicode_ci,
  `valor_monetario` decimal(10,2) DEFAULT NULL,
  `status` enum('pendente','entregue','cancelado') COLLATE utf8mb4_unicode_ci DEFAULT 'pendente',
  `data_atribuicao` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `data_entrega` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `problema_id` (`problema_id`),
  KEY `solucao_id` (`solucao_id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `premios_ibfk_1` FOREIGN KEY (`problema_id`) REFERENCES `problemas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `premios_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `premios_ibfk_3` FOREIGN KEY (`solucao_id`) REFERENCES `solucoes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `premios`
--

LOCK TABLES `premios` WRITE;
/*!40000 ALTER TABLE `premios` DISABLE KEYS */;
/*!40000 ALTER TABLE `premios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `problemas`
--

DROP TABLE IF EXISTS `problemas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `problemas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `empresa_id` int NOT NULL,
  `titulo` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descricao` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `contexto_empresa` text COLLATE utf8mb4_unicode_ci,
  `area` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nivel_dificuldade` enum('iniciante','intermediario','avancado') COLLATE utf8mb4_unicode_ci DEFAULT 'iniciante',
  `tipo` enum('free','premium') COLLATE utf8mb4_unicode_ci DEFAULT 'free',
  `tipo_avaliacao` enum('ai','manual') COLLATE utf8mb4_unicode_ci DEFAULT 'manual',
  `objetivos` text COLLATE utf8mb4_unicode_ci,
  `requisitos` text COLLATE utf8mb4_unicode_ci,
  `recursos_fornecidos` text COLLATE utf8mb4_unicode_ci,
  `prazo_dias` int DEFAULT '30',
  `pontos_recompensa` int DEFAULT '100',
  `oferece_certificado` tinyint(1) DEFAULT '0',
  `premio_descricao` text COLLATE utf8mb4_unicode_ci,
  `criterios_avaliacao` json DEFAULT NULL,
  `status` enum('ativo','fechado','arquivado') COLLATE utf8mb4_unicode_ci DEFAULT 'ativo',
  `data_inicio` date NOT NULL,
  `data_fim` date NOT NULL,
  `max_participantes` int DEFAULT '0',
  `visualizacoes` int DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_empresa` (`empresa_id`),
  KEY `idx_area` (`area`),
  KEY `idx_tipo` (`tipo`),
  KEY `idx_status` (`status`),
  KEY `idx_nivel` (`nivel_dificuldade`),
  FULLTEXT KEY `idx_fulltext_problemas` (`titulo`,`descricao`),
  CONSTRAINT `problemas_ibfk_1` FOREIGN KEY (`empresa_id`) REFERENCES `empresas` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `problemas`
--

LOCK TABLES `problemas` WRITE;
/*!40000 ALTER TABLE `problemas` DISABLE KEYS */;
INSERT INTO `problemas` VALUES (1,2,'Sistema de Recomendação de Produtos','Desenvolver um sistema de recomendação inteligente usando machine learning para sugerir produtos aos usuários baseado em seu histórico de compras e comportamento de navegação.','E-commerce de grande porte com milhões de produtos','Inteligência Artificial','avancado','free','manual','Criar sistema de ML que aumente conversão em 15%','Python, scikit-learn, pandas, API REST','Dataset de transações, documentação da API',30,500,1,'Certificado digital + possibilidade de contratação',NULL,'ativo','2025-10-15','2025-11-14',0,0,'2025-10-15 11:01:56','2025-10-15 11:01:56'),(2,3,'Sistema de Recomendação de Produtos','Desenvolver um sistema de recomendação inteligente usando machine learning para sugerir produtos aos usuários baseado em seu histórico de compras e comportamento de navegação.','E-commerce de grande porte com milhões de produtos','Inteligência Artificial','avancado','free','manual','Criar sistema de ML que aumente conversão em 15%','Python, scikit-learn, pandas, API REST','Dataset de transações, documentação da API',30,500,1,'Certificado digital + possibilidade de contratação',NULL,'ativo','2025-10-15','2025-11-14',0,1,'2025-10-15 11:35:01','2025-10-15 11:35:03'),(3,4,'Sistema de Recomendação de Produtos','Desenvolver um sistema de recomendação inteligente usando machine learning para sugerir produtos aos usuários baseado em seu histórico de compras e comportamento de navegação.','E-commerce de grande porte com milhões de produtos','Inteligência Artificial','avancado','free','manual','Criar sistema de ML que aumente conversão em 15%','Python, scikit-learn, pandas, API REST','Dataset de transações, documentação da API',30,500,1,'Certificado digital + possibilidade de contratação',NULL,'ativo','2025-10-15','2025-11-14',0,1,'2025-10-15 11:42:27','2025-10-15 11:42:29'),(4,5,'Sistema de Recomendação de Produtos','Desenvolver um sistema de recomendação inteligente usando machine learning para sugerir produtos aos usuários baseado em seu histórico de compras e comportamento de navegação.','E-commerce de grande porte com milhões de produtos','Inteligência Artificial','avancado','free','manual','Criar sistema de ML que aumente conversão em 15%','Python, scikit-learn, pandas, API REST','Dataset de transações, documentação da API',30,500,1,'Certificado digital + possibilidade de contratação',NULL,'ativo','2025-10-15','2025-11-14',0,1,'2025-10-15 11:51:20','2025-10-15 11:51:22'),(5,6,'Sistema de Recomendação de Produtos','Desenvolver um sistema de recomendação inteligente usando machine learning para sugerir produtos aos usuários baseado em seu histórico de compras e comportamento de navegação.','E-commerce de grande porte com milhões de produtos','Inteligência Artificial','avancado','free','manual','Criar sistema de ML que aumente conversão em 15%','Python, scikit-learn, pandas, API REST','Dataset de transações, documentação da API',30,500,1,'Certificado digital + possibilidade de contratação',NULL,'ativo','2025-10-15','2025-11-14',0,1,'2025-10-15 12:28:39','2025-10-15 12:28:40');
/*!40000 ALTER TABLE `problemas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ranking_mensal`
--

DROP TABLE IF EXISTS `ranking_mensal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ranking_mensal` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `mes` int NOT NULL,
  `ano` int NOT NULL,
  `pontos_mes` int DEFAULT '0',
  `problemas_resolvidos` int DEFAULT '0',
  `posicao_ranking` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_mes_ano` (`user_id`,`mes`,`ano`),
  KEY `idx_ranking` (`ano`,`mes`,`pontos_mes` DESC),
  CONSTRAINT `ranking_mensal_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ranking_mensal`
--

LOCK TABLES `ranking_mensal` WRITE;
/*!40000 ALTER TABLE `ranking_mensal` DISABLE KEYS */;
/*!40000 ALTER TABLE `ranking_mensal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recomendacoes`
--

DROP TABLE IF EXISTS `recomendacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recomendacoes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `empresa_id` int NOT NULL,
  `user_id` int NOT NULL,
  `score_compatibilidade` decimal(5,2) DEFAULT NULL,
  `razoes_recomendacao` json DEFAULT NULL,
  `areas_match` json DEFAULT NULL,
  `visualizado` tinyint(1) DEFAULT '0',
  `data_visualizacao` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `idx_empresa` (`empresa_id`),
  KEY `idx_score` (`score_compatibilidade` DESC),
  CONSTRAINT `recomendacoes_ibfk_1` FOREIGN KEY (`empresa_id`) REFERENCES `empresas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `recomendacoes_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recomendacoes`
--

LOCK TABLES `recomendacoes` WRITE;
/*!40000 ALTER TABLE `recomendacoes` DISABLE KEYS */;
/*!40000 ALTER TABLE `recomendacoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solucoes`
--

DROP TABLE IF EXISTS `solucoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solucoes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `problema_id` int NOT NULL,
  `user_id` int NOT NULL,
  `descricao_solucao` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `arquivos_anexos` json DEFAULT NULL,
  `link_repositorio` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `link_demo` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `analise_ai` json DEFAULT NULL,
  `pontuacao_ai` decimal(5,2) DEFAULT NULL,
  `feedback_ai` text COLLATE utf8mb4_unicode_ci,
  `criterios_atendidos` json DEFAULT NULL,
  `avaliacao_empresa` text COLLATE utf8mb4_unicode_ci,
  `pontuacao_empresa` decimal(5,2) DEFAULT NULL,
  `pontuacao_final` decimal(5,2) DEFAULT NULL,
  `pontos_ganhos` int DEFAULT '0',
  `status` enum('em_analise','aprovada','reprovada','revisao') COLLATE utf8mb4_unicode_ci DEFAULT 'em_analise',
  `certificado_emitido` tinyint(1) DEFAULT '0',
  `certificado_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `data_submissao` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `data_avaliacao` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_problema` (`user_id`,`problema_id`),
  KEY `idx_problema` (`problema_id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_pontuacao` (`pontuacao_final`),
  CONSTRAINT `solucoes_ibfk_1` FOREIGN KEY (`problema_id`) REFERENCES `problemas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `solucoes_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solucoes`
--

LOCK TABLES `solucoes` WRITE;
/*!40000 ALTER TABLE `solucoes` DISABLE KEYS */;
INSERT INTO `solucoes` VALUES (1,1,6,'\n            Desenvolvi um sistema de recomendação híbrido combinando:\n            \n            1. Filtragem Colaborativa usando SVD (Singular Value Decomposition)\n            2. Filtragem Baseada em Conteúdo com TF-IDF\n            3. Sistema de ponderação adaptativo\n            \n            Implementação:\n            - Backend em Python com FastAPI\n            - Modelo ML treinado com scikit-learn\n            - Cache Redis para performance\n            - API REST documentada com OpenAPI\n            \n            Resultados nos testes:\n            - Precisão: 87%\n            - Recall: 82%\n            - Tempo de resposta: <100ms\n            - Escalabilidade testada com 1M de produtos\n            \n            O código está documentado, testado (cobertura 85%) e pronto para produção.\n            ',NULL,'https://github.com/teste/recommendation-system','https://demo.recommendation-system.com','{\"model\": \"llama-3.1-8b-instant\", \"feedback\": \"A solução apresentada é boa e atende aos requisitos do problema. No entanto, há espaço para melhorias em termos de criatividade e inovação. O uso de SVD e TF-IDF é comum, mas a abordagem adaptativa de ponderação é interessante. A implementação em Python com FastAPI e o uso de cache Redis são boas escolhas. No entanto, a cobertura de testes é um pouco baixa e a documentação poderia ser melhorada.\", \"provider\": \"groq\", \"criterios\": {\"clareza\": 10.0, \"viabilidade\": 5.0, \"criatividade\": 15.0, \"qualidade_tecnica\": 20.0, \"adequacao_problema\": 25.0}, \"pontuacao\": 75.0, \"from_cache\": false, \"pontos_fortes\": [\"Uso de SVD e TF-IDF para filtragem colaborativa e baseada em conteúdo\", \"Implementação em Python com FastAPI e uso de cache Redis\", \"Abordagem adaptativa de ponderação\"], \"used_fallback\": true, \"fallback_reason\": \"Gemini API Error: 404 models/gemini-pro is not found for API version v1beta, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.\", \"pontos_melhoria\": [\"Melhorar a criatividade e inovação da solução\", \"Aumentar a cobertura de testes\", \"Melhorar a documentação\"], \"tempo_analise_ms\": 1970, \"status_recomendado\": \"revisao\", \"recomendacoes_especificas\": [\"Incluir mais experimentos e análises para melhorar a precisão da recomendação\", \"Considerar o uso de técnicas de aprendizado profundo para melhorar a qualidade da recomendação\"]}',75.00,'A solução apresentada é boa e atende aos requisitos do problema. No entanto, há espaço para melhorias em termos de criatividade e inovação. O uso de SVD e TF-IDF é comum, mas a abordagem adaptativa de ponderação é interessante. A implementação em Python com FastAPI e o uso de cache Redis são boas escolhas. No entanto, a cobertura de testes é um pouco baixa e a documentação poderia ser melhorada.',NULL,NULL,NULL,75.00,500,'aprovada',0,NULL,'2025-10-15 11:01:58','2025-10-15 11:02:02','2025-10-15 11:02:02'),(2,2,7,'\n            Desenvolvi um sistema de recomendação híbrido combinando:\n            \n            1. Filtragem Colaborativa usando SVD (Singular Value Decomposition)\n            2. Filtragem Baseada em Conteúdo com TF-IDF\n            3. Sistema de ponderação adaptativo\n            \n            Implementação:\n            - Backend em Python com FastAPI\n            - Modelo ML treinado com scikit-learn\n            - Cache Redis para performance\n            - API REST documentada com OpenAPI\n            \n            Resultados nos testes:\n            - Precisão: 87%\n            - Recall: 82%\n            - Tempo de resposta: <100ms\n            - Escalabilidade testada com 1M de produtos\n            \n            O código está documentado, testado (cobertura 85%) e pronto para produção.\n            ',NULL,'https://github.com/teste/recommendation-system','https://demo.recommendation-system.com','{\"model\": \"llama-3.1-8b-instant\", \"feedback\": \"A solução apresentada é boa e atende aos requisitos do problema. No entanto, há espaço para melhorias em termos de criatividade e inovação. O uso de SVD e TF-IDF é uma boa escolha, mas poderia ser mais avançado. Além disso, a implementação em Python com FastAPI é adequada, mas poderia ser mais escalável.\", \"provider\": \"groq\", \"criterios\": {\"clareza\": 15.0, \"viabilidade\": 5.0, \"criatividade\": 10.0, \"qualidade_tecnica\": 20.0, \"adequacao_problema\": 25.0}, \"pontuacao\": 75.0, \"from_cache\": false, \"pontos_fortes\": [\"Uso de SVD e TF-IDF para recomendação de produtos\", \"Implementação em Python com FastAPI\", \"Cache Redis para performance\"], \"used_fallback\": true, \"fallback_reason\": \"Gemini API Error: 404 models/gemini-pro is not found for API version v1beta, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.\", \"pontos_melhoria\": [\"Melhorar a criatividade e inovação na solução\", \"Aumentar a escalabilidade da implementação\", \"Incluir mais recursos de machine learning para melhorar a precisão\"], \"tempo_analise_ms\": 1043, \"status_recomendado\": \"revisao\", \"recomendacoes_especificas\": [\"Incluir uma abordagem mais avançada de recomendação de produtos, como o uso de redes neurais\", \"Aumentar a escalabilidade da implementação adicionando mais recursos de computação em nuvem\"]}',75.00,'A solução apresentada é boa e atende aos requisitos do problema. No entanto, há espaço para melhorias em termos de criatividade e inovação. O uso de SVD e TF-IDF é uma boa escolha, mas poderia ser mais avançado. Além disso, a implementação em Python com FastAPI é adequada, mas poderia ser mais escalável.',NULL,NULL,NULL,75.00,500,'aprovada',0,NULL,'2025-10-15 11:35:04','2025-10-15 11:35:06','2025-10-15 11:35:06'),(3,3,8,'\n            Desenvolvi um sistema de recomendação híbrido combinando:\n            \n            1. Filtragem Colaborativa usando SVD (Singular Value Decomposition)\n            2. Filtragem Baseada em Conteúdo com TF-IDF\n            3. Sistema de ponderação adaptativo\n            \n            Implementação:\n            - Backend em Python com FastAPI\n            - Modelo ML treinado com scikit-learn\n            - Cache Redis para performance\n            - API REST documentada com OpenAPI\n            \n            Resultados nos testes:\n            - Precisão: 87%\n            - Recall: 82%\n            - Tempo de resposta: <100ms\n            - Escalabilidade testada com 1M de produtos\n            \n            O código está documentado, testado (cobertura 85%) e pronto para produção.\n            ',NULL,'https://github.com/teste/recommendation-system','https://demo.recommendation-system.com','{\"model\": \"llama-3.1-8b-instant\", \"feedback\": \"A solução apresentada é boa e mostra um bom entendimento do problema. No entanto, há algumas melhorias que podem ser feitas para torná-la mais robusta e escalável. A combinação de filtragem colaborativa e filtragem baseada em conteúdo é uma boa abordagem, mas a escolha do algoritmo de ponderação adaptativo pode ser melhorada. Além disso, a documentação e os testes são bem feitos, mas a cobertura de testes pode ser aumentada.\", \"provider\": \"groq\", \"criterios\": {\"clareza\": 10.0, \"viabilidade\": 5.0, \"criatividade\": 15.0, \"qualidade_tecnica\": 20.0, \"adequacao_problema\": 25.0}, \"pontuacao\": 72.0, \"from_cache\": false, \"pontos_fortes\": [\"Combinação de filtragem colaborativa e filtragem baseada em conteúdo\", \"Escolha do algoritmo de ponderação adaptativo\", \"Documentação e testes bem feitos\"], \"used_fallback\": true, \"fallback_reason\": \"Gemini API Error: 404 models/gemini-pro is not found for API version v1beta, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.\", \"pontos_melhoria\": [\"Melhorar a escolha do algoritmo de ponderação adaptativo\", \"Aumentar a cobertura de testes\", \"Incluir mais métricas de desempenho para avaliar a precisão e recall\"], \"tempo_analise_ms\": 1254, \"status_recomendado\": \"revisao\", \"recomendacoes_especificas\": [\"Incluir uma análise de custo-benefício para avaliar a viabilidade da implementação\", \"Desenvolver um plano de escalabilidade para lidar com um grande número de produtos\", \"Incluir uma avaliação de desempenho contínua para monitorar a precisão e recall do sistema\"]}',72.00,'A solução apresentada é boa e mostra um bom entendimento do problema. No entanto, há algumas melhorias que podem ser feitas para torná-la mais robusta e escalável. A combinação de filtragem colaborativa e filtragem baseada em conteúdo é uma boa abordagem, mas a escolha do algoritmo de ponderação adaptativo pode ser melhorada. Além disso, a documentação e os testes são bem feitos, mas a cobertura de testes pode ser aumentada.',NULL,NULL,NULL,72.00,500,'aprovada',0,NULL,'2025-10-15 11:42:31','2025-10-15 11:42:33','2025-10-15 11:42:33'),(4,4,9,'\n            Desenvolvi um sistema de recomendação híbrido combinando:\n            \n            1. Filtragem Colaborativa usando SVD (Singular Value Decomposition)\n            2. Filtragem Baseada em Conteúdo com TF-IDF\n            3. Sistema de ponderação adaptativo\n            \n            Implementação:\n            - Backend em Python com FastAPI\n            - Modelo ML treinado com scikit-learn\n            - Cache Redis para performance\n            - API REST documentada com OpenAPI\n            \n            Resultados nos testes:\n            - Precisão: 87%\n            - Recall: 82%\n            - Tempo de resposta: <100ms\n            - Escalabilidade testada com 1M de produtos\n            \n            O código está documentado, testado (cobertura 85%) e pronto para produção.\n            ',NULL,'https://github.com/teste/recommendation-system','https://demo.recommendation-system.com','{\"model\": \"llama-3.1-8b-instant\", \"feedback\": \"A solução apresentada é boa e atende aos requisitos do problema. No entanto, há espaço para melhorias em termos de criatividade e inovação. O uso de SVD e TF-IDF é uma boa escolha, mas poderia ser mais explorado. Além disso, a implementação em FastAPI e o uso de Redis para cache são boas práticas.\", \"provider\": \"groq\", \"criterios\": {\"clareza\": 15.0, \"viabilidade\": 10.0, \"criatividade\": 12.0, \"qualidade_tecnica\": 20.0, \"adequacao_problema\": 25.0}, \"pontuacao\": 72.0, \"from_cache\": false, \"pontos_fortes\": [\"Uso de SVD e TF-IDF para filtragem colaborativa e baseada em conteúdo\", \"Implementação em FastAPI e uso de Redis para cache\", \"Código documentado e testado\"], \"used_fallback\": true, \"fallback_reason\": \"Gemini API Error: 404 models/gemini-pro is not found for API version v1beta, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.\", \"pontos_melhoria\": [\"Melhorar a criatividade e inovação na abordagem\", \"Explorar mais as características dos produtos e usuários\", \"Considerar a escalabilidade e a performance em larga escala\"], \"tempo_analise_ms\": 2128, \"status_recomendado\": \"revisao\", \"recomendacoes_especificas\": [\"Explorar a possibilidade de usar técnicas de aprendizado de máquina mais avançadas, como redes neurais\", \"Considerar a implementação de um sistema de recomendação híbrido que combine diferentes técnicas\", \"Realizar testes de performance e escalabilidade em larga escala\"]}',72.00,'A solução apresentada é boa e atende aos requisitos do problema. No entanto, há espaço para melhorias em termos de criatividade e inovação. O uso de SVD e TF-IDF é uma boa escolha, mas poderia ser mais explorado. Além disso, a implementação em FastAPI e o uso de Redis para cache são boas práticas.',NULL,NULL,NULL,72.00,500,'aprovada',0,NULL,'2025-10-15 11:51:23','2025-10-15 11:51:27','2025-10-15 11:51:27'),(5,5,10,'\n            Desenvolvi um sistema de recomendação híbrido combinando:\n            \n            1. Filtragem Colaborativa usando SVD (Singular Value Decomposition)\n            2. Filtragem Baseada em Conteúdo com TF-IDF\n            3. Sistema de ponderação adaptativo\n            \n            Implementação:\n            - Backend em Python com FastAPI\n            - Modelo ML treinado com scikit-learn\n            - Cache Redis para performance\n            - API REST documentada com OpenAPI\n            \n            Resultados nos testes:\n            - Precisão: 87%\n            - Recall: 82%\n            - Tempo de resposta: <100ms\n            - Escalabilidade testada com 1M de produtos\n            \n            O código está documentado, testado (cobertura 85%) e pronto para produção.\n            ',NULL,'https://github.com/teste/recommendation-system','https://demo.recommendation-system.com','{\"model\": \"llama-3.1-8b-instant\", \"feedback\": \"A solução apresentada é boa, mas precisa de ajustes para melhorar a qualidade técnica e a criatividade. O uso de SVD e TF-IDF é uma boa escolha, mas a ponderação adaptativa pode ser melhorada. Além disso, a documentação e os testes são bem feitos, mas a cobertura de testes pode ser melhorada.\", \"provider\": \"groq\", \"criterios\": {\"clareza\": 10.0, \"viabilidade\": 5.0, \"criatividade\": 15.0, \"qualidade_tecnica\": 20.0, \"adequacao_problema\": 25.0}, \"pontuacao\": 75.0, \"from_cache\": false, \"pontos_fortes\": [\"Uso de SVD e TF-IDF para recomendação de produtos\", \"Implementação bem feita em Python com FastAPI\", \"Cache Redis para melhorar a performance\"], \"used_fallback\": true, \"fallback_reason\": \"Gemini API Error: 404 models/gemini-pro is not found for API version v1beta, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.\", \"pontos_melhoria\": [\"Melhorar a criatividade e inovação na solução\", \"Ajustar a ponderação adaptativa para melhorar a precisão\", \"Melhorar a cobertura de testes\"], \"tempo_analise_ms\": 1251, \"status_recomendado\": \"revisao\", \"recomendacoes_especificas\": [\"Investigar e implementar técnicas de aprendizado de máquina mais avançadas, como redes neurais\", \"Melhorar a documentação e os testes para cobrir mais cenários\"]}',75.00,'A solução apresentada é boa, mas precisa de ajustes para melhorar a qualidade técnica e a criatividade. O uso de SVD e TF-IDF é uma boa escolha, mas a ponderação adaptativa pode ser melhorada. Além disso, a documentação e os testes são bem feitos, mas a cobertura de testes pode ser melhorada.',NULL,NULL,NULL,75.00,500,'aprovada',0,NULL,'2025-10-15 12:28:40','2025-10-15 12:28:42','2025-10-15 12:28:42');
/*!40000 ALTER TABLE `solucoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_habilidades`
--

DROP TABLE IF EXISTS `user_habilidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_habilidades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `habilidade_id` int NOT NULL,
  `nivel_proficiencia` enum('basico','intermediario','avancado','expert') COLLATE utf8mb4_unicode_ci DEFAULT 'basico',
  `comprovado` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_habilidade` (`user_id`,`habilidade_id`),
  KEY `habilidade_id` (`habilidade_id`),
  CONSTRAINT `user_habilidades_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `user_habilidades_ibfk_2` FOREIGN KEY (`habilidade_id`) REFERENCES `habilidades` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_habilidades`
--

LOCK TABLES `user_habilidades` WRITE;
/*!40000 ALTER TABLE `user_habilidades` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_habilidades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `senha_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `data_nascimento` date DEFAULT NULL,
  `nivel_educacao` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `palavras_chave` text COLLATE utf8mb4_unicode_ci,
  `foto_perfil` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pontos_totais` int DEFAULT '0',
  `nivel_atual` int DEFAULT '1',
  `patente` enum('iniciante','bronze','prata','ouro','platina','diamante') COLLATE utf8mb4_unicode_ci DEFAULT 'iniciante',
  `email_verificado` tinyint(1) DEFAULT '0',
  `token_verificacao` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  KEY `idx_email` (`email`),
  KEY `idx_pontos` (`pontos_totais`),
  KEY `idx_nivel` (`nivel_atual`),
  KEY `idx_username` (`username`),
  FULLTEXT KEY `idx_fulltext_users` (`nome`,`palavras_chave`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (3,'João Silva Teste Atualizado','joao_teste_ukajpb3t','joao.teste.ukajpb3t@test.com','$argon2id$v=19$m=65536,t=3,p=4$9z4HwHgvRYiRcm4t5ZyTMg$N/KgBGFzqele2oYcs8/okq+J3inM900WKBMwr5lHgA0','2000-01-15','superior','python, javascript, react, node.js, machine learning',NULL,0,1,'iniciante',0,'vKLPgsrfq5Q4gEErQXuTuNnkdU8A_rQgEShM79rsO_Y',1,'2025-10-15 10:20:44','2025-10-15 10:20:49'),(4,'João Silva Teste Atualizado','joao_teste_w4gfyeo4','joao.teste.w4gfyeo4@test.com','$argon2id$v=19$m=65536,t=3,p=4$GkNo7T2nNOZ8jzGG8F6rdQ$cdv8hXfVuT3r5El19VKaiAOirMU6VyfJ54f+EcMqack','2000-01-15','superior','python, javascript, react, node.js, machine learning',NULL,0,1,'iniciante',0,'vib0NoMlxXWOAGRISWcWGTKF5ftaj5_2nDcuR4LhXBs',1,'2025-10-15 10:32:02','2025-10-15 10:32:07'),(5,'João Silva Teste Atualizado','joao_teste_h6hg1id2','joao.teste.h6hg1id2@test.com','$argon2id$v=19$m=65536,t=3,p=4$Q8hZKwWA8B5DqHXOeY/x/g$oSM5QaNczSGKquZiqG6NCa1PuUqLRSj+297ar3m/Ews','2000-01-15','superior','python, javascript, react, node.js, machine learning',NULL,0,1,'iniciante',0,'rhu0_9Pu6MLPjWatyRfRq30t_mKd-e-2ZEmfykK4NmI',1,'2025-10-15 10:41:52','2025-10-15 10:42:03'),(6,'João Silva Teste Atualizado','joao_teste_0v0gkhl4','joao.teste.0v0gkhl4@test.com','$argon2id$v=19$m=65536,t=3,p=4$23vvHaMUwrh3bo1Rai2l1A$PyUCzdjkeJh4w6L0vaaoOsUu0nvg5TxmTWj3mgYfiL4','2000-01-15','superior','python, javascript, react, node.js, machine learning',NULL,500,1,'iniciante',0,'L0bO3hWJLIEZn846SHL0QoSt_uiUIrwoTlo30w-EOOw',1,'2025-10-15 11:01:42','2025-10-15 11:02:02'),(7,'João Silva Teste Atualizado','joao_teste_a5pc9362','joao.teste.a5pc9362@test.com','$argon2id$v=19$m=65536,t=3,p=4$Z2wNYSzFOAdAaO29V+odYw$LcM/kPKYw9mqONntZ9jFBHKOjkIISRSh0mtDF5wZtTQ','2000-01-15','superior','python, javascript, react, node.js, machine learning',NULL,1000,1,'iniciante',0,'KeTzvDT735ZNMdwQJ6vn2qnG3RXO-D6VhQmN4Zf4A8A',1,'2025-10-15 11:34:49','2025-10-15 11:35:06'),(8,'João Silva Teste Atualizado','joao_teste_r1b5adqx','joao.teste.r1b5adqx@test.com','$argon2id$v=19$m=65536,t=3,p=4$UErpPcc4x7h3bs25V4oR4g$w5mSUxeOiUaADj/rZvULMSdiUEpI9CEA6HCvnMkEzcw','2000-01-15','superior','python, javascript, react, node.js, machine learning',NULL,1000,1,'iniciante',0,'Er_zoVmTr8vYDsL9BnVsGWVrfvfix7G__mnbo0Fq5K4',1,'2025-10-15 11:41:54','2025-10-15 11:42:33'),(9,'João Silva Teste Atualizado','joao_teste_ijff4lez','joao.teste.ijff4lez@test.com','$argon2id$v=19$m=65536,t=3,p=4$hFCKEWLMuXcOwVjLOafUGg$Q2t4oIUnHmItDCW0G4FlW+EaHTaN7PoHl7jAsydaYkA','2000-01-15','superior','python, javascript, react, node.js, machine learning',NULL,1000,1,'iniciante',0,'-twJ9-ET5owb44X7Ni6GH1ZigzwsvysTfF443_fUPuU',1,'2025-10-15 11:51:05','2025-10-15 11:51:28'),(10,'João Silva Teste Atualizado','joao_teste_qzu644n9','joao.teste.qzu644n9@test.com','$argon2id$v=19$m=65536,t=3,p=4$Yozx3vvfW8u5F4KQUgrBOA$LJgEqLGYlp62SbAf0BvmsOPBrVOjrQL7V6vakbdsaJo','2000-01-15','superior','python, javascript, react, node.js, machine learning',NULL,1000,1,'iniciante',0,'pTY4C-qVruNAUPdeNUG90vsYbV6qfuv7x_lLKOjYDA8',1,'2025-10-15 12:28:28','2025-10-15 12:28:42');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `view_problemas_ativos`
--

DROP TABLE IF EXISTS `view_problemas_ativos`;
/*!50001 DROP VIEW IF EXISTS `view_problemas_ativos`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `view_problemas_ativos` AS SELECT 
 1 AS `id`,
 1 AS `empresa_id`,
 1 AS `titulo`,
 1 AS `descricao`,
 1 AS `contexto_empresa`,
 1 AS `area`,
 1 AS `nivel_dificuldade`,
 1 AS `tipo`,
 1 AS `tipo_avaliacao`,
 1 AS `objetivos`,
 1 AS `requisitos`,
 1 AS `recursos_fornecidos`,
 1 AS `prazo_dias`,
 1 AS `pontos_recompensa`,
 1 AS `oferece_certificado`,
 1 AS `premio_descricao`,
 1 AS `criterios_avaliacao`,
 1 AS `status`,
 1 AS `data_inicio`,
 1 AS `data_fim`,
 1 AS `max_participantes`,
 1 AS `visualizacoes`,
 1 AS `created_at`,
 1 AS `updated_at`,
 1 AS `empresa_nome`,
 1 AS `empresa_logo`,
 1 AS `total_solucoes`,
 1 AS `media_pontuacao_solucoes`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `view_problemas_ativos`
--

/*!50001 DROP VIEW IF EXISTS `view_problemas_ativos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_problemas_ativos` AS select `p`.`id` AS `id`,`p`.`empresa_id` AS `empresa_id`,`p`.`titulo` AS `titulo`,`p`.`descricao` AS `descricao`,`p`.`contexto_empresa` AS `contexto_empresa`,`p`.`area` AS `area`,`p`.`nivel_dificuldade` AS `nivel_dificuldade`,`p`.`tipo` AS `tipo`,`p`.`tipo_avaliacao` AS `tipo_avaliacao`,`p`.`objetivos` AS `objetivos`,`p`.`requisitos` AS `requisitos`,`p`.`recursos_fornecidos` AS `recursos_fornecidos`,`p`.`prazo_dias` AS `prazo_dias`,`p`.`pontos_recompensa` AS `pontos_recompensa`,`p`.`oferece_certificado` AS `oferece_certificado`,`p`.`premio_descricao` AS `premio_descricao`,`p`.`criterios_avaliacao` AS `criterios_avaliacao`,`p`.`status` AS `status`,`p`.`data_inicio` AS `data_inicio`,`p`.`data_fim` AS `data_fim`,`p`.`max_participantes` AS `max_participantes`,`p`.`visualizacoes` AS `visualizacoes`,`p`.`created_at` AS `created_at`,`p`.`updated_at` AS `updated_at`,`e`.`nome` AS `empresa_nome`,`e`.`logo_url` AS `empresa_logo`,count(distinct `s`.`id`) AS `total_solucoes`,avg(`s`.`pontuacao_final`) AS `media_pontuacao_solucoes` from ((`problemas` `p` join `empresas` `e` on((`p`.`empresa_id` = `e`.`id`))) left join `solucoes` `s` on((`p`.`id` = `s`.`problema_id`))) where ((`p`.`status` = 'ativo') and (`p`.`data_fim` >= curdate())) group by `p`.`id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-15 22:10:43
