# Importa TUTTO qui così Base.metadata vede tutte le tabelle/classi.
# Questo è comodo per Alembic (autogenerate) e per evitare mapper incompleti.

from backend.model.links import ruolo_permesso

from backend.model.permesso import Permesso
from backend.model.ruolo import Ruolo
from backend.model.utente import Utente, UtenteRuolo

from backend.model.materia import Materia, TutorMateria


from backend.model.lezione import Lezione
from backend.model.lezione_partecipante import LezionePartecipante
from backend.model.lezione_stato_storia import LezioneStatoStoria

from backend.model.pagamento import Pagamento
from backend.model.studente import Studente
from backend.model.utente_note import UtenteNote
from backend.model.paese import Paese
from backend.model.sessione import Sessione

__all__ = [
    # pure links (Table)
    "ruolo_permesso",

    # auth/anagrafica
    "Permesso",
    "Ruolo",
    "Utente",
    "UtenteRuolo",
    "Sessione",
    "Paese",

    # didattica
    "Materia",
    "TutorMateria",

    # disponibilità / lezioni
    "Lezione",
    "LezionePartecipante",
    "LezioneStatoStoria",

    # pagamenti / note
    "Pagamento",
    "Studente",
    "UtenteNote",
]
