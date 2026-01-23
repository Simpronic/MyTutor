
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Argon2 hasher (config di default sicura)

pwd_hasher = PasswordHasher()

def hash_password(plain_password: str) -> str:
    """
    Crea hash Argon2 da password in chiaro.
    (Usalo in fase di registrazione o seed DB)
    """
    return pwd_hasher.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Verifica password in chiaro contro hash Argon2.
    """
    try:
        return pwd_hasher.verify(password_hash, plain_password)
    except VerifyMismatchError:
        return False
    except Exception:
        # hash corrotto o formato sconosciuto
        return False
    