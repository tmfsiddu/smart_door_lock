class User:
    
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password


class Fingerprint:

    def __init__(self, id, user_id, fingerprint_id):
        self.id = id
        self.user_id = user_id
        self.fingerprint_id = fingerprint_id


class OTP:

    def __init__(self, email, otp):
        self.email = email
        self.otp = otp


class AccessLog:

    def __init__(self, id, user_id, access_time, status):
        self.id = id
        self.user_id = user_id
        self.access_time = access_time
        self.status = status