SHOW DATABASES;
CREATE DATABASE IF NOT EXISTS `nasmas` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `nasmas`;
SHOW TABLES;
CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
SELECT * FROM `accounts`;
DELETE FROM accounts WHERE id ="24";
