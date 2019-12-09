import datetime

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

    def add_block(self, event, patient):
        self.blocks.append(Block(len(self.blocks), player=self.player, name=self.name, patient=patient.name,
                                 timestamp=datetime.datetime.utcnow(), kind=event.event, data=event.name,
                                 previous_hash=self.blocks[len(self.blocks) - 1].hash))

        if not self.verify()[0]:
            print(f"WARNING: {self.verify()[1]}")

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
        patient.add_block(event, doctor=self)
        event.add_block(patient, doctor=self)
        self.add_block(event, patient)
