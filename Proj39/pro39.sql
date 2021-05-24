CREATE DATABASE IF NOT EXISTS `pro39` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pro39`;

CREATE TABLE IF NOT EXISTS `faculty` (
	`userid` varchar(10) NOT NULL,
    `username` varchar(100) NOT NULL,
    `department` varchar(100) NOT NULL,
    `mobile` varchar(10) NOT NULL,
  	`password` varchar(255) NOT NULL,
    PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

select * from faculty;



CREATE TABLE IF NOT EXISTS `issuecategory` (
    `type` varchar(255) NOT NULL,
    `offname` varchar(255) NOT NULL,
    `offemail` varchar(100) NOT NULL,
  	
    PRIMARY KEY (`type`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;




INSERT INTO `issuecategory`  VALUES ('water','waterman','water@test.com');
INSERT INTO `issuecategory`  VALUES ('electricity','powerman','power@test.com');
INSERT INTO `issuecategory`  VALUES ('woodwork','carpenter','wood@test.com');

select * from issuecategory;




CREATE TABLE IF NOT EXISTS `complaintstable` (
	`compid` varchar(255) NOT NULL,
    `facultyid` varchar(10) NOT NULL,
    `department` varchar(255) NOT NULL,
    `type` varchar(255) NOT NULL,
    `desc` varchar(255) NOT NULL,
    `offname` varchar(255) NOT NULL,
    `offemail` varchar(100) NOT NULL,
    `status` varchar(255) NOT NULL,
  	
    PRIMARY KEY (`compid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

select * from complaintstable;



CREATE TABLE IF NOT EXISTS `admin` (
    `email` varchar(255) NOT NULL,
    `name` varchar(255) NOT NULL,
    `password` varchar(100) NOT NULL,
  	
    PRIMARY KEY (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

select * from admin;
insert into admin values('test@gmail.com','Taruni','test123');
