# Model for Profile documents in Profile Collection
def profileModel(user_id, name, lastname, email, birthdate, phone_number, address, historials):
    profile = {
        'user_id': user_id,
        'name': name,
        'lastname': lastname,
        'email': email,
        'birthdate': birthdate,
        'phone_number': phone_number,
        'address': address,
        'historials': historials
    }
    return profile
