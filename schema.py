"""
    Define os esquemas do GraphQL
"""

from models import Departments, Employees, DeptEmp, DeptManager, Titles, Salaries, db_session
import graphene
from graphene import Field,String
from sqlalchemy import or_
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField


class SalariesType(SQLAlchemyObjectType):
    class Meta:
        model = Salaries
        interfaces = (graphene.relay.Node, )


class EmployeesType(SQLAlchemyObjectType):
    class Meta:
        description = 'Todos os funcionários da empresa.'
        model = Employees
        interfaces = (graphene.relay.Node, )

    salary = Field(lambda: graphene.List(SalariesType)
                   ,min=graphene.Int(), max=graphene.Int(), description="Salários do empregado.")

    countSalary = graphene.Int(description="Total de salários registrados.")

    def resolve_salary(self, info, **args):
        where = Salaries.emp_no == self.emp_no
        if args.get('min'):
            where &= Salaries.salary >= args.get('min')
        if args.get('max'):
            where &= Salaries.salary <= args.get('max')

        query = SalariesType.get_query(info)
        return query.filter(where).all()

    def resolve_countSalary(self, info):
        where = Salaries.emp_no == self.emp_no
        query = SalariesType.get_query(info)
        return query.filter(where).count()




class DepartmentsType(SQLAlchemyObjectType):
    class Meta:
        description = 'Todos os departamentos da empresa.'
        model = Departments
        interfaces = (graphene.relay.Node, )

    employees = Field(lambda: graphene.List(EmployeesType, description="Empregrados relacionados ao departamento.")
                      ,limit=graphene.Int())

    def resolve_employees(self, info, **args):
        query = EmployeesType.get_query(info)
        if args.get('limit'):
            limit = args.get('limit')
        else:
            limit = 10
        return query.filter(DeptEmp.dept_no == self.dept_no).\
                     filter(DeptEmp.emp_no == Employees.emp_no).limit(limit).all()


class DeptManagerType(SQLAlchemyObjectType):
    class Meta:
        model = DeptManager
        interfaces = (graphene.relay.Node, )


class DeptEmpType(SQLAlchemyObjectType):
    class Meta:
        model = DeptEmp
        interfaces = (graphene.relay.Node, )


class TitlesType(SQLAlchemyObjectType):
    class Meta:
        model = Titles
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_titles      = SQLAlchemyConnectionField(TitlesType.connection)
    all_salaries    = SQLAlchemyConnectionField(SalariesType)
    all_employees   = SQLAlchemyConnectionField(EmployeesType)
    all_departments = SQLAlchemyConnectionField(DepartmentsType)

    employeeByName = Field(lambda: graphene.List(EmployeesType), name=String(required=True), description="Seleciona os funcionários pelo nome.")
    employeeByDept = Field(lambda: graphene.List(EmployeesType), dpto_no=String(required=True), description="Seleciona os funcionários pelo departamento.")
    departmentsByNo = Field(lambda: graphene.List(DepartmentsType), dept_no=String(required=True), description="Seleciona os departamentos pelo número.")

    def resolve_departmentsByNo(parent, info, dept_no):
        query = DepartmentsType.get_query(info)
        return query.filter(Departments.dept_no.contains(dept_no)).all()

    def resolve_employeeByName(parent, info, name):
        filters = (
                or_(Employees.first_name.contains(name),
                    Employees.last_name.contains(name))
            )
        query = EmployeesType.get_query(info)
        return query.filter(filters).all()

    def resolve_employeeByDept(parent, info, dpto_no):
        query = EmployeesType.get_query(info)
        return query.filter(DeptEmp.dept_no == dpto_no).\
                     filter(DeptEmp.emp_no == Employees.emp_no).limit(100).all()


class CreateDepartment(graphene.Mutation):
    dept_no = graphene.String(description="Número do departamento.")
    dept_name = graphene.String(description="Nome do departamento.")

    class Arguments:
        dept_no = graphene.String()
        dept_name = graphene.String()

    def mutate(self, info, dept_no, dept_name):
        department = Departments(dept_no=dept_no, dept_name=dept_name)
        db_session.add(department)
        db_session.commit()

        return CreateDepartment(
            dept_no=department.dept_no,
            dept_name=department.dept_name
        )


class Mutation(graphene.ObjectType):
    create_department = CreateDepartment.Field(description="Cria um novo departamento.")


schema = graphene.Schema(query=Query, mutation=Mutation)
