import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from blockchain import BlockChain, Block


class IncompatibilityError(Exception):
    """Raised when an event is not compatible with a previous one."""
    def __init__(self, message):
        super().__init__(message)


class Patient(BlockChain):
    """
    Patient object.
    """

    def __init__(self, name, *args, **kw):
        super(BlockChain, self).__init__(*args, **kw)
        self.name = name
        self.player = "patient"
        self.blocks = [self.get_genesis_block()]
        self.generate_keys(permanent=True)
        self.generate_keys(permanent=False)

    def add_block(self, event, doctor):
        """
        Add a new block to the chain.

        Parameters
        ----------
        event : Event
            BlockChain relative to the event that the patient faced.
        doctor : Doctor
            BlockChain relative to the doctor that adds the event to the chain of the patient.
        """
        # Prevent from adding prescriptions that are not compatible with previous diseases
        if event.event == "prescription":
            for ev in self.get_chain().Kind:
                if ev in event.incompatibilities:
                    raise IncompatibilityError(f"Past event {ev} is not compatible with {event.name} {event.event}")

        self.blocks.append(Block(len(self.blocks), player=self.player, name=self.name, doctor=doctor.name,
                                 timestamp=datetime.datetime.utcnow(), kind=event.event, data=event.name,
                                 previous_hash=self.blocks[len(self.blocks) - 1].hash))

        if not self.verify()[0]:
            print(f"WARNING: {self.verify()[1]}")

    def generate_keys(self, permanent=False):
        """
        Generate private and public keys of this specific patient and store them in the respective folders.

        Parameters
        ----------
        permanent : bool
            If True, the keys are stored as permanent keys, meaning that they will not be overwritten in future.
            Permanent keys should be always kept secret and only used by the patient.
            Doctors should not have access to the permanent private keys of the patients.
        """
        # Generate keys
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        private_key = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                format=serialization.PrivateFormat.PKCS8,
                                                encryption_algorithm=serialization.NoEncryption())
        public_key = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                             format=serialization.PublicFormat.SubjectPublicKeyInfo)

        # Store keys
        if not permanent:
            with open(f'../private_keys/{self.name}_temporary.pem', 'wb') as f:
                f.write(private_key)
            with open(f'../public_keys/{self.name}_public_temp.pem', 'wb') as f:
                f.write(public_key)
        else:
            with open(f'../private_keys/{self.name}_permanent.pem', 'wb') as f:
                f.write(private_key)
            with open(f'../public_keys/{self.name}_public_perm.pem', 'wb') as f:
                f.write(public_key)
