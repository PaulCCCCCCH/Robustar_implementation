--
-- File generated with SQLiteStudio v3.4.4 on Sun Oct 22 22:52:25 2023
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: eval_results
CREATE TABLE IF NOT EXISTS eval_results (model_id VARCHAR, img_path VARCHAR, result INTEGER, PRIMARY KEY (model_id, img_path));

-- Table: influ_rel
CREATE TABLE IF NOT EXISTS influ_rel (model_id BIGINT UNIQUE NOT NULL, image_path VARCHAR UNIQUE NOT NULL, influ_path VARCHAR, PRIMARY KEY (model_id, image_path));

-- Table: models
CREATE TABLE IF NOT EXISTS models (model_id BIGINT PRIMARY KEY UNIQUE NOT NULL, model_name VARCHAR, description VARCHAR, architecture VARCHAR, tags VARCHAR, create_time TIME, weight_path VARCHAR, code_path VARCHAR, epoch INTEGER, train_accuracy DOUBLE, val_accuracy DOUBLE, test_accuracy DOUBLE, last_eval_on_dev_set TIME, last_eval_on_test_set TIME);

-- Table: paired_set
CREATE TABLE IF NOT EXISTS paired_set (path VARCHAR PRIMARY KEY UNIQUE NOT NULL, train_path VARCHAR);

-- Table: proposed
CREATE TABLE IF NOT EXISTS proposed (path VARCHAR PRIMARY KEY UNIQUE NOT NULL, train_path VARCHAR);

-- Table: test_set
CREATE TABLE IF NOT EXISTS test_set (path VARCHAR PRIMARY KEY UNIQUE NOT NULL);

-- Table: train_set
CREATE TABLE IF NOT EXISTS train_set (path VARCHAR PRIMARY KEY UNIQUE, paired_path VARCHAR);

-- Table: val_set
CREATE TABLE IF NOT EXISTS val_set (path VARCHAR PRIMARY KEY UNIQUE NOT NULL);

-- Table: visuals
CREATE TABLE IF NOT EXISTS visuals (image_path VARCHAR, model_id BIGINT, visual_path VARCHAR, PRIMARY KEY (image_path, model_id, visual_path));

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
