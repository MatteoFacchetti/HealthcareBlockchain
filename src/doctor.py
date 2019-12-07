from blockchain import BlockChain, Block


class Doctor(BlockChain):
    """
    Doctor object.
    """
    def __init__(self, name, *args, **kw):
        super(BlockChain, self).__init__(*args, **kw)
        self.name = name
        self.player = "doctor"
        self.blocks = [self.get_genesis_block()]

    def add_event(self, event, patient):
        """
        Add an event to the patient blockchain. This will in turn add the patient itself to the blockchain of the event.

        Parameters
        ----------
        event : :obj:`Event`
            The Blockchain relative to the event that the patient faces.
        patient : :obj:`Patient`
            The BlockChain relative to the patient that faces the event.
        """
        event.add_block(patient, doctor=self.name)
        patient.add_block(event, doctor=self.name)


def get_block(patient, n):
    return patient.get_block(n)


def get_chain(patient):
    return patient.get_chain()
