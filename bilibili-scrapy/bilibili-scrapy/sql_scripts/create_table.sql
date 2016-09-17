CREATE TABLE `video` (
  `id` int(11) NOT NULL,
  `name` varchar(512) DEFAULT NULL,
  `av` int(11) DEFAULT NULL,
  `author` varchar(512) DEFAULT NULL,
  `plays` int(11) DEFAULT NULL,
  `barrages` int(11) DEFAULT NULL,
  `coins` int(11) DEFAULT NULL,
  `favorites` int(11) DEFAULT NULL,
  `replys` int(11) DEFAULT NULL,
  `category` varchar(512) DEFAULT NULL,
  `url` varchar(512) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `update_time_short` date DEFAULT NULL,
  `last_crawled` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`update_time_short`),
  KEY `author` (`author`),
  KEY `category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
