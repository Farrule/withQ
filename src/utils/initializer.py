import logging
import datetime
import asyncio
import discord
import database.db as db
import components.row_view as row_view
import commands.withQ_command as WithQCommand

async def restore_sessions(client: discord.Client):
    """データベースからアクティブなセッションを復元する"""
    db.init_db()
    active_sessions = db.get_active_sessions()
    logging.info(f"Restoring {len(active_sessions)} active sessions...")

    for session in active_sessions:
        try:
            recruiter = client.get_user(session["recruiter_id"])
            if recruiter is None:
                try:
                    recruiter = await client.fetch_user(session["recruiter_id"])
                except Exception:
                    recruiter = discord.Object(id=session["recruiter_id"])

            display_deadline_time = session["deadline_time"]
            db_deadline_time = session["deadline_time"]
            if db_deadline_time:
                try:
                    # まず "YYYY/MM/DD/HH:MM:SS" としてパースを試みる
                    time_in_datetime = datetime.datetime.strptime(db_deadline_time, "%Y/%m/%d/%H:%M:%S")
                    now_datetime = datetime.datetime.now()
                    if time_in_datetime.date() == now_datetime.date():
                        display_deadline_time = time_in_datetime.strftime("%H:%M")
                    else:
                        display_deadline_time = time_in_datetime.strftime("%m/%d/%H:%M")
                except ValueError:
                    # 既存データなどでパース失敗した場合はそのまま使用
                    pass

            view = row_view.RowView(
                title=session["title"],
                recruitment_num=session["recruitment_num"],
                in_queue_member_dict=session["in_queue_member_dict"],
                recruiter=recruiter,
                mention_target=session["mention_target"],
                is_feedback_on_recruitment=session["is_feedback_on_recruitment"],
                deadline_time=display_deadline_time,
                is_deadline=session["is_deadline"],
                session_id=session["session_id"]
            )
            client.add_view(view)

            if session["expire_at"]:
                expire_datetime = datetime.datetime.fromisoformat(session["expire_at"])
                now_datetime = datetime.datetime.now()
                remaining_seconds = max((expire_datetime - now_datetime).total_seconds(), 0)

                asyncio.create_task(WithQCommand.monitor_deadline(
                    client=client,
                    session_id=session["session_id"],
                    view=view,
                    total_seconds=remaining_seconds,
                    title=session["title"],
                    deadline_time=display_deadline_time,
                    in_queue_member_dict=session["in_queue_member_dict"],
                    channel_id=session["channel_id"],
                    message_id=session["message_id"]
                ))
            logging.info(f"Restored session: {session['session_id']}")
        except Exception as e:
            logging.info(f"Failed to restore session {session.get('session_id')}: {e}")
