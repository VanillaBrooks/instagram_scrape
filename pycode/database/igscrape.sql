-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema igscrape
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema igscrape
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `igscrape` DEFAULT CHARACTER SET utf8mb4 ;
USE `igscrape` ;

-- -----------------------------------------------------
-- Table `igscrape`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `igscrape`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(30) NULL,
  `screenname` VARCHAR(45) NULL,
  `original_user` TINYINT(1) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `igscrape`.`scrape`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `igscrape`.`scrape` (
  `user_id` INT NOT NULL,
  `id` INT NOT NULL AUTO_INCREMENT,
  `post_count` INT NOT NULL,
  `follow_count` INT NOT NULL,
  `follower_count` INT NOT NULL,
  `scrape_date` DATETIME NOT NULL,
  `original_user` TINYINT(1) NOT NULL,
  INDEX `fk_scrape_users_idx` (`user_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_scrape_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `igscrape`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `igscrape`.`similarity`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `igscrape`.`similarity` (
  `user_id` INT NOT NULL,
  `user_id_followed` INT NULL,
  `cos_sim_value` DECIMAL(4,4) NULL,
  INDEX `fk_similarity_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_similarity_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `igscrape`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `igscrape`.`post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `igscrape`.`post` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `post_id_str` VARCHAR(45) NOT NULL,
  `caption_text` TEXT NOT NULL,
  `post_date` DATETIME NOT NULL,
  `like_count` INT NOT NULL,
  `scrape_id` INT NOT NULL,
  INDEX `fk_post_user1_idx` (`user_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  INDEX `fk_post_scrape1_idx` (`scrape_id` ASC) VISIBLE,
  CONSTRAINT `fk_post_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `igscrape`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_post_scrape1`
    FOREIGN KEY (`scrape_id`)
    REFERENCES `igscrape`.`scrape` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `igscrape`.`comment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `igscrape`.`comment` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `post_id` INT NOT NULL,
  `comment_text` TEXT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comment_post1_idx` (`post_id` ASC) VISIBLE,
  INDEX `fk_comment_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_comment_post1`
    FOREIGN KEY (`post_id`)
    REFERENCES `igscrape`.`post` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comment_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `igscrape`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
