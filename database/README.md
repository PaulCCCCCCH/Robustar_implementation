# Database Dev Guide

## Prep

Download `SQLiteStudio` from https://sqlitestudio.pl/ (which is a handy GUI-client for SQLite) and install it.

## Clean up

1. Delete `/Robustar/data.db`
2. Open `SQLiteStudio`. Remove the `robustar-latest` database if it already exists.

## Modifying Database Schema

1. In `SQLiteStudio`, hover on `Database` dropdown and click `Add a database`, select `database/robustar-latest.db` under the project folder. Name the new database `robustar-latest`.
2. Modify the db schema with the GUI as you wish.
3. When done, hover on `Database` dropdown and click `Export the database`.
4. Make sure all tables are checked and **uncheck** `Export data from tables` as we don't need any data in the generated SQL. Click `Next`.
5. Export format is SQL, output as file to `database/robustar-latest.sql` under the project folder folder.
6. Use utf-8 in `Export text encoding`. **Do not** include `DROP IF EXISTS` and **Do not** use SQL formatter.
7. Click `Finish`.

## Update Robustar To Use New Schema

1. Copy the content of newly generated `robustar-latest.sql` file into the `get_init_schema_str` function in `utils/db.py`.
2. Run the backend. A new `/Robustar/data.db` will be generated.
3. Replacing `database/robustar-latest.db` with the newly generated `/Robustar/data.db`.
4. Push the changes.
