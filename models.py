import re
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value or not str(value).strip():
            raise ValueError('Name cannot be empty.')
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not (isinstance(new_value, str) and len(new_value) == 10 and new_value.isdigit()):
            raise ValueError('Phone number must be exactly 10 digits.')
        self._value = new_value


class Email(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', new_value):
            raise ValueError('Invalid email format.')
        self._value = new_value


class Address(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        try:
            date_obj = datetime.strptime(value, '%d.%m.%Y').date()
            super().__init__(date_obj)
        except ValueError:
            raise ValueError('Invalid date format. Use DD.MM.YYYY')

    def __str__(self):
        # Якщо потрібно буде вивести на екран
        return self.value.strftime('%d.%m.%Y') if self.value else ''


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.addresses = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        phone_obj = self.find_phone(phone_number)
        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise ValueError(f'Phone {phone_number} not found.')


    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)
        if not phone_obj:
            raise ValueError(f'Phone {old_phone} not found in record.')
        new_phone_obj = Phone(new_phone)
        index = self.phones.index(phone_obj)
        self.phones[index] = new_phone_obj

    def find_phone(self, phone_number):
        for p in self.phones:
            if p.value == phone_number:
                return p
        return None


    def add_email(self, email_address):
        self.emails.append(Email(email_address))

    def remove_email(self, email_address):
        email_obj = self.find_email(email_address)
        if email_obj:
            self.emails.remove(email_obj)
        else:
            raise ValueError(f'Email {email_address} not found.')

    def edit_email(self, old_email, new_email):
        email_obj = self.find_email(old_email)
        if not email_obj:
            raise ValueError(f'Email {old_email} not found in record.')
        new_email_obj = Email(new_email)
        index = self.emails.index(email_obj)
        self.emails[index] = new_email_obj

    def find_email(self, email_address):
        for e in self.emails:
            if e.value == email_address:
                return e
        return None


    def add_address(self, physical_address):
        self.addresses.append(Address(physical_address))

    def remove_address(self, physical_address):
        address_obj = self.find_address(physical_address)
        if address_obj:
            self.addresses.remove(address_obj)
        else:
            raise ValueError(f'Address {physical_address} not found.')

    def edit_address(self, old_address, new_address):
        address_obj = self.find_address(old_address)
        if not address_obj:
            raise ValueError(f'Address {old_address} not found in record.')
        new_address_obj = Address(new_address)
        index = self.addresses.index(address_obj)
        self.addresses[index] = new_address_obj

    def find_address(self, physical_address):
        for a in self.addresses:
            if a.value == physical_address:
                return a
        return None


    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones) if self.phones else 'No phones'
        parts = [f'Contact name: {self.name.value}', f'phones: {phones_str}']

        if self.birthday:
            parts.append(f'birthday: {self.birthday.value}')

        if self.emails:
            emails_str = '; '.join(e.value for e in self.emails)
            parts.append(f'emails: {emails_str}')

        if self.addresses:
            addresses_str = '; '.join(a.value for a in self.addresses)
            parts.append(f'addresses: {addresses_str}')

        return ', '.join(parts)
