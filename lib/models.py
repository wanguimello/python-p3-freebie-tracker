from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    founding_year = Column(Integer, nullable=False)

    # Relationship with Freebie
    freebies = relationship('Freebie', backref='company', lazy='dynamic')

    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
        """Creates a new Freebie associated with this company and a given dev."""
        return Freebie(dev=dev, company=self, item_name=item_name, value=value)

    @classmethod
    def oldest_company(cls, session):
        """Returns the company with the earliest founding year."""
        return session.query(cls).order_by(cls.founding_year).first()


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationship with Freebie
    freebies = relationship('Freebie', backref='dev', lazy='dynamic')

    def __repr__(self):
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        """Returns True if the dev has received a freebie with the given item_name."""
        return self.freebies.filter(Freebie.item_name == item_name).count() > 0

    def give_away(self, dev, freebie):
        """Transfers ownership of a freebie to another dev if the freebie belongs to the current dev."""
        if freebie.dev == self:
            freebie.dev = dev


class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    def __repr__(self):
        return f'<Freebie {self.item_name} - Value: {self.value}>'

    def print_details(self):
        """Returns a string showing the dev's ownership of the freebie from a company."""
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
