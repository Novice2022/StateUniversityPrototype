def check_auth(
    session: dict[str, str] = {}
) -> tuple[bool, dict[str, str]]:
    session_user_instance = {
        "user_id": session.get("user_id", None),
        "user_type": session.get("user_type", None),
        "user_name": session.get("user_name", None),
        "user_surname": session.get("user_surname", None),
        "student_group_id": session.get("student_group_id", None),
        "teacher_phone": session.get("teacher_phone", None),
    }

    authorised = False

    if sum([
        bool(key) for key in session_user_instance.values()
    ]) == 5:
        authorised = True
    
    return authorised, session_user_instance
