import sqlite3

def init_db():
    conn = sqlite3.connect("project.db")
    cursor = conn.cursor()

    # ------------------- USERS TABLE -------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        full_name TEXT,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        password TEXT NOT NULL
    )
    """)

    # ------------------- DISCUSSIONS TABLE -------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS discussions (
        discussion_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_email) REFERENCES users(email)
    )
    """)

    # ------------------- DISCUSSION REPLIES -------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS discussion_replies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        discussion_id INTEGER NOT NULL,
        user_email TEXT NOT NULL,
        reply TEXT NOT NULL,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (discussion_id) REFERENCES discussions(discussion_id),
        FOREIGN KEY (user_email) REFERENCES users(email)
    )
    """)

    # ------------------- CAREERS TABLE -------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS careers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL,
        full_name TEXT NOT NULL,
        job_title TEXT NOT NULL,
        resume_link TEXT,
        cover_letter TEXT,
        submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY (user_email) REFERENCES users(email)
    )
    """)

    # ------------------- CONTACT MESSAGES TABLE -------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL,
        sent_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ------------------- CONTACT TABLE -------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        topic TEXT,
        message TEXT NOT NULL
    )
    """)

    # ------------------- SUBSCRIPTIONS TABLE -------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL,
        plan TEXT NOT NULL,
        start_date TEXT DEFAULT CURRENT_TIMESTAMP,
        expiration_date TEXT,
        payment_method TEXT,
        FOREIGN KEY (user_email) REFERENCES users(email)
    )
    """)

    # ------------------- APPOINTMENTS TABLE -------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL,
        appointment_date TEXT,
        appointment_time TEXT,
        appointment_service TEXT NOT NULL,
        appointment_description TEXT NOT NULL,
        FOREIGN KEY (user_email) REFERENCES users(email)
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
