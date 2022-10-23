def historialModel(career, GPA, coursed_credits, approved_credits, reprobed_credits):
    historial = {
        "career": career,
        "GPA": GPA,
        "coursed_credits": coursed_credits,
        "approved_credits": approved_credits,
        "reprobed_credits": reprobed_credits,
    }
    return historial


def historialModelforUser(user_id, career, GPA, coursed_credits, approved_credits, reprobed_credits):
    historial = {
        "user_id": user_id,
        "career": career,
        "GPA": GPA,
        "coursed_credits": coursed_credits,
        "approved_credits": approved_credits,
        "reprobed_credits": reprobed_credits,
    }
    return historial
