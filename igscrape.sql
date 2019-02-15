-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`user` (
  `id` INT GENERATED ALWAYS AS () VIRTUAL,
  `username` VARCHAR(30) NULL,
  `screenname` VARCHAR(45) NULL,
  `original_user` TINYINT(1) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`scrape`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`scrape` (
  `user_id` INT NOT NULL,
  `scrape_id` INT GENERATED ALWAYS AS () VIRTUAL,
  `post_count` INT NOT NULL,
  `follow_count` INT NOT NULL,
  `follower_count` INT NOT NULL,
  `scrape_date` DATETIME NOT NULL,
  `original_user` TINYINT(1) NOT NULL,
  INDEX `fk_scrape_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_scrape_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`similarity`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`similarity` (
  `user_id` INT NOT NULL,
  `user_id_followed` INT NULL,
  `cos_sim_value` DECIMAL(4,4) NULL,
  `calculation_date` DATETIME NULL,
  INDEX `fk_similarity_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_similarity_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`post` (
  `user_id` INT NOT NULL,
  `post_id_str` VARCHAR(45) NOT NULL,
  `post_id` INT GENERATED ALWAYS AS () VIRTUAL,
  `caption_text` TEXT NOT NULL,
  `post_date` DATETIME NOT NULL,
  `like_count` INT NOT NULL,
  INDEX `fk_post_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_post_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`comment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`comment` (
  `user_id` INT NOT NULL,
  `comment_text` TEXT NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_comment_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
