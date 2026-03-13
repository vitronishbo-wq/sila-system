from .ano_letivo import AnoLetivo
from .escola import CicloEnsino, Escola, TipoEscola
from .inscricao_basica import InscricaoBasica
from .inscricao_secundaria import InscricaoSecundaria
from .inscricao_superior import InscricaoSuperior
from .inscricao_tecnico import InscricaoTecnico
from .matricula import Matricula, StatusMatricula
from .turma import Turma, Turno
__all__ = ['Matricula', 'StatusMatricula', 'Escola', 'TipoEscola', 'CicloEnsino', 'Turma', 'Turno', 'AnoLetivo', 'InscricaoBasica', 'InscricaoSecundaria', 'InscricaoSuperior', 'InscricaoTecnico']