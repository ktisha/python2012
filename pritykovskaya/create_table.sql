CREATE DATABASE `goods_db` CHARACTER SET utf8

DROP TABLE IF EXISTS `items`;
CREATE TABLE `items` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(1024) NOT NULL DEFAULT '',
  `description` varchar(2048) NOT NULL DEFAULT '',
  `category` varchar(1024) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

mysql -u root -p goods_db < /home/pritykovskaya/Desktop/python_project/insert_script.sql
