from patient import Patient
from event import Event
from doctor import Doctor

l = locals()


# --- PATIENTS --- #
Ann = Patient("R945MU")
Bob = Patient("C901UL")
Charlie = Patient("R396UZ")
Daniel = Patient("R371GE")
Eveline = Patient("F348KE")
Frank = Patient("A856EV")
George = Patient("N806DM")
Hilary = Patient("C936DA")
Ingrid = Patient("X622NL")
Juliet = Patient("R462TV")


# --- DISEASES --- #
arthritis = Event("disease", "arthritis", loc=l)
bulimia = Event("disease", "bulimia", loc=l)
celiac = Event("disease", "celiac", loc=l)
diabetes = Event("disease", "diabetes", loc=l)
ebola = Event("disease", "ebola", loc=l)
flatulence = Event("disease", "flatulence", loc=l)
gastroenteritis = Event("disease", "gastroenteritis", loc=l)
hemorrhoids = Event("disease", "hemorroids", loc=l)
insomnia = Event("disease", "insomnia", loc=l)
labyrinthitis = Event("disease", "labyrinthitis", loc=l)


# --- PRESCRIPTIONS --- #
"""To avoid misinformation, prescriptions will not take real names."""
prescription_1 = Event("prescription", "drug_1", loc=l, incompatibilities=None)
prescription_2 = Event("prescription", "drug_2", loc=l, incompatibilities=["hemorroids"])
prescription_3 = Event("prescription", "drug_3", loc=l, incompatibilities=["arthritis", "diabetes"])
prescription_4 = Event("prescription", "drug_4", loc=l, incompatibilities=["bulimia", "ebola", "insomnia"])
prescription_5 = Event("prescription", "drug_5", loc=l, incompatibilities=["arthritis", "ebola"])
prescription_6 = Event("prescription", "drug_6", loc=l, incompatibilities=["gastroenteritis"])
prescription_7 = Event("prescription", "drug_7", loc=l, incompatibilities=None)
prescription_8 = Event("prescription", "drug_8", loc=l, incompatibilities=["diabetes"])
prescription_9 = Event("prescription", "drug_9", loc=l, incompatibilities=["celiac", "insomnia"])
prescription_10 = Event("prescription", "drug_10", loc=l, incompatibilities=["bulimia", "celiac", "diabetes"])


# --- DOCTORS --- #
DrHouse = Doctor("D-T584JV")
DrZhivago = Doctor("D-U577UK")
DrJD = Doctor("D-M681TC")
DrTurk = Doctor("D-J421RY")
DrKelso = Doctor("D-M932XZ")
DrCox = Doctor("D-Y553BX")
DrEspinosa = Doctor("D-H821DM")
DrAdams = Doctor("D-Y553CX")
DrFrankenstein = Doctor("D-V676RT")
DrLecter = Doctor("D-C692VH")
