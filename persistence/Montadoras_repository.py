from sqlmodel import Session, select
from persistence.Utils import get_engine
from models import Montadora

class MontadoraRepository:
    def __init__(self):
        self.session = Session(get_engine())

    def get_all(self):
        sttm = select(Montadora)
        return self.session.exec(sttm).all()

    def get(self, montadora_id: str):
        return self.session.get(Montadora, montadora_id)

    def save(self, montadora: Montadora):
        self.session.add(montadora)
        self.session.commit()
        self.session.refresh(montadora)
        return montadora

    def delete(self, montadora_id: str):
        montadora = self.session.get(Montadora, montadora_id)
        if montadora:
            self.session.delete(montadora)
            self.session.commit()

    def update(self, montadora_id: str, montadora_data: Montadora):
        montadora = self.session.get(Montadora, montadora_id)
        if montadora:
            montadora.nome = montadora_data.nome
            montadora.pais = montadora_data.pais
            montadora.ano_fundacao = montadora_data.ano_fundacao
            self.session.commit()
            self.session.refresh(montadora)
        return montadora

    def filter_by_name_or_country(self, query: str):
        sttm = select(Montadora).where(Montadora.nome.contains(query) | Montadora.pais.contains(query))
        return self.session.exec(sttm).all()

    def order_by_attribute(self, attribute: str, order: str = 'asc'):
        if attribute == 'ano_fundacao':
            sttm = select(Montadora).order_by(Montadora.ano_fundacao.asc() if order == 'asc' else Montadora.ano_fundacao.desc())
        else:
            sttm = select(Montadora).order_by(attribute if order == 'asc' else f"-{attribute}")
        return self.session.exec(sttm).all()
