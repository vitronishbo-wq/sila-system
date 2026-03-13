from __future__ import annotations
from app.modules.resources.ambiente.application.services.cadastro_service import CadastroService
from app.modules.resources.ambiente.application.services.condicionante_service import CondicionanteService
from app.modules.resources.ambiente.application.services.estudo_service import EstudoService
from app.modules.resources.ambiente.application.services.fiscalizacao_service import FiscalizacaoService
from app.modules.resources.ambiente.application.services.licenciamento_service import LicenciamentoService
from app.modules.resources.ambiente.application.services.penalidade_service import PenalidadeService
from app.modules.resources.ambiente.infrastructure.repositories import SQLAlchemyAutoInfracaoRepository, SQLAlchemyCARRepository, SQLAlchemyCondicionanteRepository, SQLAlchemyEmbargoRepository, SQLAlchemyEstudoRepository, SQLAlchemyFiscalizacaoRepository, SQLAlchemyImovelRepository, SQLAlchemyLicencaRepository, SQLAlchemyMultaRepository, SQLAlchemyProprietarioRepository
proprietario_repo_singleton = SQLAlchemyProprietarioRepository()
imovel_repo_singleton = SQLAlchemyImovelRepository()
car_repo_singleton = SQLAlchemyCARRepository()
licenca_repo_singleton = SQLAlchemyLicencaRepository()
estudo_repo_singleton = SQLAlchemyEstudoRepository()
condicionante_repo_singleton = SQLAlchemyCondicionanteRepository()
fiscalizacao_repo_singleton = SQLAlchemyFiscalizacaoRepository()
auto_infracao_repo_singleton = SQLAlchemyAutoInfracaoRepository()
embargo_repo_singleton = SQLAlchemyEmbargoRepository()
multa_repo_singleton = SQLAlchemyMultaRepository()
cadastro_service_singleton = CadastroService(proprietario_repo=proprietario_repo_singleton, imovel_repo=imovel_repo_singleton, car_repo=car_repo_singleton)
licenciamento_service_singleton = LicenciamentoService(car_repo=car_repo_singleton, licenca_repo=licenca_repo_singleton)
estudo_service_singleton = EstudoService(licenca_repo=licenca_repo_singleton, estudo_repo=estudo_repo_singleton)
condicionante_service_singleton = CondicionanteService(licenca_repo=licenca_repo_singleton, condicionante_repo=condicionante_repo_singleton)
fiscalizacao_service_singleton = FiscalizacaoService(licenca_repo=licenca_repo_singleton, fiscalizacao_repo=fiscalizacao_repo_singleton)
penalidade_service_singleton = PenalidadeService(fiscalizacao_repo=fiscalizacao_repo_singleton, auto_infracao_repo=auto_infracao_repo_singleton, embargo_repo=embargo_repo_singleton, multa_repo=multa_repo_singleton)

def get_cadastro_service() -> CadastroService:
    return cadastro_service_singleton

def get_licenciamento_service() -> LicenciamentoService:
    return licenciamento_service_singleton

def get_estudo_service() -> EstudoService:
    return estudo_service_singleton

def get_condicionante_service() -> CondicionanteService:
    return condicionante_service_singleton

def get_fiscalizacao_service() -> FiscalizacaoService:
    return fiscalizacao_service_singleton

def get_penalidade_service() -> PenalidadeService:
    return penalidade_service_singleton