import os, re
def sanitize_filename(name):
    return re.sub(r'[^\w\-. ]','_', name)
def ensure_dirs(*paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)
