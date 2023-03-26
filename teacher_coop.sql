-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema teacher_coop
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `teacher_coop` ;

-- -----------------------------------------------------
-- Schema teacher_coop
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `teacher_coop` DEFAULT CHARACTER SET utf8 ;
USE `teacher_coop` ;

-- -----------------------------------------------------
-- Table `teacher_coop`.`teachers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `teacher_coop`.`teachers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `grade` VARCHAR(45) NULL,
  `subject` VARCHAR(45) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `teacher_coop`.`plans`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `teacher_coop`.`plans` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NULL,
  `subject` VARCHAR(45) NULL,
  `grade_level` VARCHAR(45) NULL,
  `topic` VARCHAR(45) NULL,
  `materials` TEXT NULL,
  `description` TEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `teacher_id` INT NOT NULL,
  PRIMARY KEY (`id`, `teacher_id`),
  INDEX `fk_plans_teachers_idx` (`teacher_id` ASC) VISIBLE,
  CONSTRAINT `fk_plans_teachers`
    FOREIGN KEY (`teacher_id`)
    REFERENCES `teacher_coop`.`teachers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `teacher_coop`.`comments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `teacher_coop`.`comments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content` TEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `teacher_id` INT NOT NULL,
  `plan_id` INT NOT NULL,
  `plan_teacher_id` INT NOT NULL,
  PRIMARY KEY (`id`, `teacher_id`, `plan_id`, `plan_teacher_id`),
  INDEX `fk_comments_teachers1_idx` (`teacher_id` ASC) VISIBLE,
  INDEX `fk_comments_plans1_idx` (`plan_id` ASC, `plan_teacher_id` ASC) VISIBLE,
  CONSTRAINT `fk_comments_teachers1`
    FOREIGN KEY (`teacher_id`)
    REFERENCES `teacher_coop`.`teachers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comments_plans1`
    FOREIGN KEY (`plan_id` , `plan_teacher_id`)
    REFERENCES `teacher_coop`.`plans` (`id` , `teacher_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
