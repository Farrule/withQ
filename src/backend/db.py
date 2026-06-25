import os
import sqlite3
import json
import logging

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "withq.db")

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS active_sessions (
                session_id TEXT PRIMARY KEY,
                title TEXT,
                recruitment_num INTEGER,
                in_queue_member_dict TEXT,
                recruiter_id INTEGER,
                recruiter_global_name TEXT,
                mention_target TEXT,
                is_feedback_on_recruitment INTEGER,
                deadline_time TEXT,
                is_deadline INTEGER,
                guild_id INTEGER,
                channel_id INTEGER,
                message_id INTEGER,
                expire_at TEXT
            )
        """)
        conn.commit()
        conn.close()
        logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")

def save_session(
    session_id: str,
    title: str,
    recruitment_num: int,
    in_queue_member_dict: dict,
    recruiter_id: int,
    recruiter_global_name: str,
    mention_target: str,
    is_feedback_on_recruitment: bool,
    deadline_time: str,
    is_deadline: bool,
    guild_id: int,
    channel_id: int,
    message_id: int,
    expire_at: str = None
):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO active_sessions (
                session_id, title, recruitment_num, in_queue_member_dict,
                recruiter_id, recruiter_global_name, mention_target,
                is_feedback_on_recruitment, deadline_time, is_deadline,
                guild_id, channel_id, message_id, expire_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            title,
            recruitment_num,
            json.dumps(in_queue_member_dict),
            recruiter_id,
            recruiter_global_name,
            mention_target,
            1 if is_feedback_on_recruitment else 0,
            deadline_time,
            1 if is_deadline else 0,
            guild_id,
            channel_id,
            message_id,
            expire_at
        ))
        conn.commit()
        conn.close()
        logging.info(f"[DB] Session {session_id} saved/updated.")
    except Exception as e:
        logging.error(f"[DB] Failed to save session {session_id}: {e}")

def update_session_members(session_id: str, in_queue_member_dict: dict):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE active_sessions
            SET in_queue_member_dict = ?
            WHERE session_id = ?
        """, (json.dumps(in_queue_member_dict), session_id))
        conn.commit()
        conn.close()
        logging.info(f"[DB] Session members updated for {session_id}.")
    except Exception as e:
        logging.error(f"[DB] Failed to update session members for {session_id}: {e}")

def delete_session(session_id: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM active_sessions WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()
        logging.info(f"[DB] Session {session_id} deleted.")
    except Exception as e:
        logging.error(f"[DB] Failed to delete session {session_id}: {e}")

def get_active_sessions():
    try:
        conn = sqlite3.connect(DB_PATH)
        # Use Row factory to access columns by name
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM active_sessions")
        rows = cursor.fetchall()
        sessions = []
        for row in rows:
            sessions.append({
                "session_id": row["session_id"],
                "title": row["title"],
                "recruitment_num": row["recruitment_num"],
                "in_queue_member_dict": json.loads(row["in_queue_member_dict"]),
                "recruiter_id": row["recruiter_id"],
                "recruiter_global_name": row["recruiter_global_name"],
                "mention_target": row["mention_target"],
                "is_feedback_on_recruitment": bool(row["is_feedback_on_recruitment"]),
                "deadline_time": row["deadline_time"],
                "is_deadline": bool(row["is_deadline"]),
                "guild_id": row["guild_id"],
                "channel_id": row["channel_id"],
                "message_id": row["message_id"],
                "expire_at": row["expire_at"]
            })
        conn.close()
        return sessions
    except Exception as e:
        logging.error(f"[DB] Failed to get active sessions: {e}")
        return []
