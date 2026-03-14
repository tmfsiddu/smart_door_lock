def add_fingerprint(user_id, fingerprint_id, conn):

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO fingerprints(user_id,fingerprint_id) VALUES (?,?)",
        (user_id,fingerprint_id)
    )

    conn.commit()


def remove_fingerprint(fingerprint_id, conn):

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM fingerprints WHERE fingerprint_id=?",
        (fingerprint_id,)
    )

    conn.commit()