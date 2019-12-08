from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from patient import Patient


# Methods that patients and doctors can use
def get_block(chain, n, key=None):
    """
    Get a specific block in the `chain`. If the chain is a `Patient` object, then a private key is also required.

    Parameters
    ----------
    chain
    n
    key

    Returns
    -------

    """
    if isinstance(chain, Patient):
        check_keys(key, chain)
        refresh_keys(chain)
    return chain.get_block(n)


def get_chain(patient, key):
    check_keys(key, patient)
    refresh_keys(patient)
    return patient.get_chain()


# Method that only the doctor can use
def add_event(doctor, event, patient, key):
    if doctor.player != "doctor":
        raise PermissionError("Only doctors can add events.")
    check_keys(key, patient)
    doctor.add_event(event, patient)
    refresh_keys(patient)


# Utils methods
def load_private_key(key):
    with open(key, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key


def load_public_key(key):
    with open(key, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key


def check_keys(key, patient):
    if key is None:
        raise AttributeError("Please insert a valid key.")
    key = key.public_key()
    key = key.public_bytes(encoding=serialization.Encoding.PEM,
                           format=serialization.PublicFormat.SubjectPublicKeyInfo)
    public_key = load_public_key(f'../public_keys/{patient.name}_public.pem')
    public_key = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                         format=serialization.PublicFormat.SubjectPublicKeyInfo)
    genesis_key = load_public_key(f'../public_keys/{patient.name}_public_gen.pem')
    genesis_key = genesis_key.public_bytes(encoding=serialization.Encoding.PEM,
                                           format=serialization.PublicFormat.SubjectPublicKeyInfo)
    if key != public_key and key != genesis_key:
        raise PermissionError("You do not have access to the BlockChain of this patient.")


def refresh_keys(patient):
    patient.generate_keys(genesis=False)
    print("Keys have been refreshed. Old keys have been destroyed and will not work.")
