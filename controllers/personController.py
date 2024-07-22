import logging
from models.person import Person
from models.rol import Rol
from models.account import Account
from app import db
import uuid
import re
import bcrypt

class PersonController:
    def listPersonAccount(self):
        persons = Person.query.all()
        person_List = []
        for person in persons:
            account = person.account
            rol = person.rol
            person_data = {
                "external_id": person.external_id,
                "name": person.name,
                "lastname": person.lastname,
                "email": account.email if account else None,
                "status": account.status if account else None,
                "rol": rol.rol if rol else None,
            }
            person_List.append(person_data)
        return person_List


    def validate_Email(self, email):
        format = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if re.match(format, email):
            return True
        else:
            return False

    def save_person(self, data):
        repeated_account = Account.query.filter_by(email=data["email"]).first()
        if repeated_account:
            return -2
        
        person = Person()

        if "rol" in data:
            rol_name = data["rol"]
            rol = Rol.query.filter_by(rol=rol_name).first()
            if not rol:
                return -1
        else:
            rol = Rol.query.filter_by(rol="Usuario").first()

        if not self.validate_Email(data["email"]):
            return -11

        person.name = data["name"]
        person.lastname = data["lastname"]
        person.external_id = uuid.uuid4()
        person.rol_id = rol.id
        db.session.add(person)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error committing person: {e}')
            return -4

        hashed_password = bcrypt.hashpw(
            data["password"].encode("utf-8"), bcrypt.gensalt()
        )
        account = Account()
        account.email = data["email"]
        account.password = hashed_password.decode("utf-8")
        account.person_id = person.id
        account.external_id = uuid.uuid4()
        account.status = 'activo' 
        db.session.add(account)

        try:
            db.session.commit()
            return 1
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error committing account: {e}')
            return -4

    def modify_person(self, external_id, data):
        print("-----------", external_id)
        person = Person.query.filter_by(external_id=external_id).first()
        if person:
            if not self.validate_Email(data["email"]):
                return -11
            existing_account = Account.query.filter(Account.email == data["email"], Account.person_id != person.id).first()

            if existing_account:
                return -2
            rol_name = data["rol"]
            rol = Rol.query.filter_by(rol=rol_name).first()
            if rol:
                person.name = data.get("name", person.name)
                person.lastname = data.get("lastname", person.lastname)
                person.rol_id = rol.id
                if 'email' in data or 'password' in data:
                    account = Account.query.filter_by(person_id=person.id).first()
                    if account:
                        account.email = data.get('email', account.email)
                        if 'password' in data and data['password']:
                            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
                            account.password = hashed_password.decode('utf-8')
                    else:
                        return -10
                db.session.commit()

                return person
            else:
                return -3
        else:
            return -3

    def deactivate_account(self, external_id):
        person = Person.query.filter_by(external_id=external_id).first()
        if person:
            account = person.account
            if account:
                if account.status == "activo":
                    account.status = "desactivo"
                else:
                    account.status = "activo"
                db.session.commit()
                return account.status 
            else:
                return False
        else:
            return False

    def all_rol(self):
        roles = Rol.query.all()
        roles_data = [
            {"name": role.rol, "external_id": role.external_id} for role in roles
        ]
        return roles_data
