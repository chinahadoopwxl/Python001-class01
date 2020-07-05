CREATE TABLE IF NOT EXISTS `movie`(
   `movie_id` INT UNSIGNED AUTO_INCREMENT,
   `movie_name` VARCHAR(50) NOT NULL,
   `movie_type` VARCHAR(50) NOT NULL,
   `movie_time` VARCHAR(10) NOT NULL,
   PRIMARY KEY ( `movie_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
