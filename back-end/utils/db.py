def get_init_schema_str():
    return """
--
-- File generated with SQLiteStudio v3.3.3 on Tue May 10 12:31:41 2022
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: influ_rel
CREATE TABLE influ_rel (path VARCHAR (256) PRIMARY KEY UNIQUE NOT NULL, image_path VARCHAR (256) NOT NULL);

-- Table: paired_set
CREATE TABLE paired_set (path VARCHAR (256) PRIMARY KEY UNIQUE NOT NULL, train_path VARCHAR (256) UNIQUE NOT NULL);

-- Table: proposed
CREATE TABLE proposed (path VARCHAR (256) PRIMARY KEY UNIQUE NOT NULL, train_path VARCHAR (256) NOT NULL);

-- Table: split
CREATE TABLE split (id INTEGER PRIMARY KEY UNIQUE NOT NULL, split_name VARCHAR (45) NOT NULL);

-- Table: test_set
CREATE TABLE test_set (path VARCHAR (256) PRIMARY KEY UNIQUE NOT NULL, classified INTEGER NOT NULL);

-- Table: train_set
CREATE TABLE train_set (path VARCHAR (256) PRIMARY KEY UNIQUE NOT NULL, paired_path VARCHAR (256));

-- Table: val_set
CREATE TABLE val_set (path VARCHAR (256) PRIMARY KEY UNIQUE NOT NULL, classified INTEGER NOT NULL);

-- Table: visu_rel
CREATE TABLE visu_rel (path VARCHAR (256) PRIMARY KEY UNIQUE NOT NULL, image_path VARCHAR (256) UNIQUE NOT NULL);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
    """
