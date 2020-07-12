DROP TABLE `lagou_position`;
CREATE TABLE IF NOT EXISTS `lagou_position`(
   `position_id` INT UNSIGNED AUTO_INCREMENT,
   `city_name` VARCHAR(50) NOT NULL,
   `position_name` VARCHAR(50) NOT NULL,
   `salary` VARCHAR(50) NOT NULL,
   PRIMARY KEY ( `position_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
