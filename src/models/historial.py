def historialModel(career, GPA, coursed_credits, approved_credits, reprobed_credits, enrollment_id):
    historial = {
        "career": career,
        "GPA": GPA,
        "coursed_credits": coursed_credits,
        "approved_credits": approved_credits,
        "reprobed_credits": reprobed_credits,
        "enrollment_id": enrollment_id,
    }
    return historial

def historialModelforUser(user_id, career, GPA, coursed_credits, approved_credits, reprobed_credits, enrollment_id):
    historial = {
        "user_id": user_id,
        "career": career,
        "GPA": GPA,
        "coursed_credits": coursed_credits,
        "approved_credits": approved_credits,
        "reprobed_credits": reprobed_credits,
        "enrollment_id": enrollment_id,
    }
    return historial