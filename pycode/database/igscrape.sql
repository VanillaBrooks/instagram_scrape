-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema igscrape
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `igscrape` ;

-- -----------------------------------------------------
-- Schema igscrape
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `igscrape` DEFAULT CHARACTER SET utf8mb4 ;
SHOW WARNINGS;
USE `igscrape` ;

-- -----------------------------------------------------
-- Table `user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `user` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `user` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`username` VARCHAR(30) NULL,
	`screenname` VARCHAR(45) NULL,
	`original_user` TINYINT(1) NULL,
	PRIMARY KEY (`id`),
	UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `scrape`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scrape` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `scrape` (
	`user_id` INT NOT NULL,
	`scrape_id` INT NOT NULL AUTO_INCREMENT,
	`post_count` INT NOT NULL,
	`follow_count` INT NOT NULL,
	`follower_count` INT NOT NULL,
	`scrape_date` DATETIME NOT NULL,
	`original_user` TINYINT(1) NOT NULL,
	INDEX `fk_scrape_users_idx` (`user_id` ASC) VISIBLE,
	PRIMARY KEY (`scrape_id`),
	CONSTRAINT `fk_scrape_users`
		FOREIGN KEY (`user_id`)
		REFERENCES `user` (`id`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `similarity`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `similarity` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `similarity` (
	`similarity_id` INT NOT NULL AUTO_INCREMENT,
	`user_id` INT NOT NULL,
	`user_id_followed` INT NULL,
	`cos_sim_value` DECIMAL(4,4) NULL,
	`calculation_date` DATETIME NULL,
	INDEX `fk_similarity_user1_idx` (`user_id` ASC) VISIBLE,
	PRIMARY KEY (`similarity_id`),
	CONSTRAINT `fk_similarity_user1`
		FOREIGN KEY (`user_id`)
		REFERENCES `user` (`id`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `post`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `post` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `post` (
	`post_id` INT NOT NULL AUTO_INCREMENT,
	`user_id` INT NOT NULL,
	`post_id_str` VARCHAR(45) NOT NULL,
	`caption_text` TEXT NOT NULL,
	`post_date` DATETIME NOT NULL,
	`like_count` INT NOT NULL,
	`scrape_scrape_id` INT NOT NULL,
	INDEX `fk_post_user1_idx` (`user_id` ASC) VISIBLE,
	PRIMARY KEY (`post_id`),
	INDEX `fk_post_scrape1_idx` (`scrape_scrape_id` ASC) VISIBLE,
	CONSTRAINT `fk_post_user1`
		FOREIGN KEY (`user_id`)
		REFERENCES `user` (`id`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION,
	CONSTRAINT `fk_post_scrape1`
		FOREIGN KEY (`scrape_scrape_id`)
		REFERENCES `scrape` (`scrape_id`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `comment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `comment` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `comment` (
	`comment_id` INT NOT NULL AUTO_INCREMENT,
	`post_id` INT NOT NULL,
	`comment_text` TEXT NOT NULL,
	`user_id` INT NOT NULL,
	PRIMARY KEY (`comment_id`),
	INDEX `fk_comment_post1_idx` (`post_id` ASC) VISIBLE,
	INDEX `fk_comment_user1_idx` (`user_id` ASC) VISIBLE,
	CONSTRAINT `fk_comment_post1`
		FOREIGN KEY (`post_id`)
		REFERENCES `post` (`post_id`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION,
	CONSTRAINT `fk_comment_user1`
		FOREIGN KEY (`user_id`)
		REFERENCES `user` (`id`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
-- SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
