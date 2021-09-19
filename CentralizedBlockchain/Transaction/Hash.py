import hashlib, json

def hashMe(msg=""):
    if type(msg)!=str:
        msg = json.dumps(msg, sort_keys=True)  # If we don't sort keys, we can't guarantee repeatability!
    return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()
