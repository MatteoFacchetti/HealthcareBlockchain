from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from patient import Patient


def get_block(chain, n, key=None):
    """
    Get a specific block in the `chain`. If the chain is a `Patient` object, then a key is also required.

    Parameters
    ----------
    chain : BlockChain
        BlockChain containing the block to be returned.
    n : int
        Index of the block to be returned.
    key : _RSAPrivateKey, default None
        Key to unlock the Patient BlockChain.

    Returns
    -------
    A pandas DataFrame.
    """
    if isinstance(chain, Patient):
        check_keys(key, chain)
        refresh_keys(chain)
    return chain.get_block(n)


def get_chain(chain, key=None):
    """
    Return a whole BlockChain. If the chain is a `Patient` object, then a key is also required.

    Parameters
    ----------
    chain : BlockChain
        BlockChain to be returned.
    key : _RSAPrivateKey, default None
        Key to unlock the Patient BlockChain.

    Returns
    -------
    A pandas DataFrame.
    """
    if isinstance(chain, Patient):
        check_keys(key, chain)
        refresh_keys(chain)
    return chain.get_chain()


def add_event(doctor, event, patient, key):
    """
    Add a new event to the BlockChains. Only the doctors can mine new blocks, provided that they have the permission.

    Parameters
    ----------
    doctor : Doctor
        Doctor who is adding the event.
    event : Event
        Event that is being added.
    patient : Patient
        Patient that is facing this event.
    key : _RSAPrivateKey, default None
        Key to unlock the Patient BlockChain.
    """
    if doctor.player != "doctor":
        raise PermissionError("Only doctors can add events.")
    check_keys(key, patient)
    doctor.add_event(event, patient)
    print(f"{event.name} {event.event} added successfully to patient {patient.name}")
    refresh_keys(patient)


def verify(chain):
    """
    Verify data integrity of the BlockChain.

    Parameters
    ----------
    chain : BlockChain
    """
    return chain.verify()


def get_chain_size(chain):
    """
    Return the length of the chain, excluding the genesis block.

    Parameters
    ----------
    chain : BlockChain
    """
    return chain.get_chain_size()


def load_private_key(key):
    """
    Load a private key.

    Parameters
    ----------
    key : str
        Path to the key file.

    Returns
    -------
    private_key : _RSAPrivateKey
    """
    with open(key, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key


def load_public_key(key):
    """
    Load a public key.

    Parameters
    ----------
    key : str
        Path to the key file.

    Returns
    -------
    public_key : _RSAPublicKey
    """
    with open(key, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key


def check_keys(key, patient):
    """
    Check that private and public keys match.

    Parameters
    ----------
    key : _RSAPrivateKey
    patient : Patient

    Raises
    ------
    AttributeError
        If `key` is None.
    PermissionError
        If private and public keys do not match.
    """
    if key is None:
        raise AttributeError("Please insert a valid key.")
    key = key.public_key()
    key = key.public_bytes(encoding=serialization.Encoding.PEM,
                           format=serialization.PublicFormat.SubjectPublicKeyInfo)
    public_key = load_public_key(f'../public_keys/{patient.name}_public_temp.pem')
    public_key = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                         format=serialization.PublicFormat.SubjectPublicKeyInfo)
    permanent_key = load_public_key(f'../public_keys/{patient.name}_public_perm.pem')
    permanent_key = permanent_key.public_bytes(encoding=serialization.Encoding.PEM,
                                               format=serialization.PublicFormat.SubjectPublicKeyInfo)
    if key != public_key and key != permanent_key:
        raise PermissionError("You do not have access to the BlockChain of this patient.")


def refresh_keys(patient):
    """
    Refresh temporary keys of the patient.

    Parameters
    ----------
    patient : Patient
    """
    patient.generate_keys(permanent=False)
    print("Temporary keys have been refreshed. Old keys have been destroyed and will not work.")
