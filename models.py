"""
    Define a base de dados
"""

from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://local:local@192.168.100.196/employees', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Departments(Base):
    __tablename__ = 'departments'
    dept_no   = Column('dept_no', String(4), primary_key=True, nullable=False, doc="Número do departamento.")
    dept_name = Column('dept_name', String(40), unique=True, nullable=False, doc="Nome do departamento.")


class Employees(Base):
    __tablename__ = 'employees'
    emp_no     = Column('emp_no', Integer, primary_key=True, nullable=False)
    birth_date = Column('birth_date', Date, nullable=False, doc="Data de aniversário do funcionário")
    first_name = Column('first_name', String(14), nullable=False, doc="Primeiro nome")
    last_name  = Column('last_name', String(16), nullable=False, doc="Sobrenome")
    gender     = Enum('M', 'F')
    hire_date  = Column('hire_date', Date, nullable=False, doc="Data de contratação")


class DeptEmp(Base):
    __tablename__ = 'dept_emp'
    dept_no = Column('dept_no', String(4), ForeignKey('departments.dept_no'), primary_key=True, nullable=False)
    emp_no = Column('emp_no', Integer, ForeignKey('employees.emp_no'), primary_key=True, nullable=False)
    from_date = Column('from_date', Date, nullable=False)
    to_date = Column('to_date', Date, nullable=False)


class DeptManager(Base):
    __tablename__ = 'dept_manager'
    dept_no = Column('dept_no', String(4), ForeignKey('departments.dept_no'), primary_key=True, nullable=False)
    emp_no = Column('emp_no', Integer, ForeignKey('employees.emp_no'), primary_key=True, nullable=False)
    from_date = Column('from_date', Date, nullable=False)
    to_date = Column('to_date', Date, nullable=False)


class Salaries(Base):
    __tablename__ = 'salaries'
    emp_no    = Column('emp_no', Integer, ForeignKey('employees.emp_no'), primary_key=True, nullable=False)
    salary    = Column('salary', Integer, nullable=False)
    from_date = Column('from_date', Date, primary_key=True,  nullable=False)
    to_date   = Column('to_date', Date, nullable=False)


class Titles(Base):
    __tablename__ = 'titles'
    emp_no    = Column('emp_no', Integer, ForeignKey('employees.emp_no'), primary_key=True, nullable=False)
    title    = Column('title', String(50), primary_key=True, nullable=False)
    from_date = Column('from_date', Date, primary_key=True,  nullable=False)
    to_date   = Column('to_date', Date, nullable=False)

