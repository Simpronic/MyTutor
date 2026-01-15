# Importa TUTTO qui così Base.metadata vede tutte le tabelle/classi.
# Questo è comodo per Alembic (autogenerate) e per evitare mapper incompleti.

from backend.model.links import ruolo_permesso, materia_argomento

from backend.model.permesso import Permesso
from backend.model.ruolo import Ruolo
from backend.model.utente import Utente, UtenteRuolo

from backend.model.materia import Materia, TutorMateria
from backend.model.argomento import Argomento

from backend.model.disponibilita_tutor import DisponibilitaTutor

from backend.model.lezione import Lezione
from backend.model.lezione_stato_storia import LezioneStatoStoria

from backend.model.pagamento import Pagamento
from backend.model.utente_note import UtenteNote

__all__ = [
    # pure links (Table)
    "ruolo_permesso",
    "materia_argomento",

    # auth/anagrafica
    "Permesso",
    "Ruolo",
    "Utente",
    "UtenteRuolo",

    # didattica
    "Materia",
    "TutorMateria",
    "Argomento",

    # disponibilità / lezioni
    "DisponibilitaTutor",
    "Lezione",
    "LezioneStatoStoria",

    # pagamenti / note
    "Pagamento",
    "UtenteNote",
]
