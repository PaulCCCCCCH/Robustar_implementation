import sqlite3
from datetime import datetime

conn = sqlite3.connect("/Users/monica/Robustar2/data.db")
cursor = conn.cursor()

# Insert data into `models` table
cursor.executemany(
    """
    INSERT INTO models (architecture, class_name, create_time, epoch, nickname, description, predefined, code_path, weight_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""",
    [
        (
            "Sample Architecture 1",
            "SimpleCNN",
            datetime.strptime("11/20/1999 10:00", "%m/%d/%Y %H:%M"),
            10,
            "SimpleCNN",
            "This is an example model 1.",
            "0",
            "/Users/monica/Robustar2/generated/models/code/SimpleCNN.py",
            "/Users/monica/Robustar2/generated/models/ckpt/SimpleCNN.py",
        ),
    ],
)

conn.commit()
conn.close()
