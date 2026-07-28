import hashlib


def get_file_hash(file_path):
    """
    Generate SHA-256 hash for a file.
    Used to detect duplicate uploads.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:

        while True:

            chunk = f.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()