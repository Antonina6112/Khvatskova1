import argparse
import json
import re

class Node:
    """Interface"""
    email: str
    weight: str
    inn: str
    passport_series: str
    university: str
    work_experience: str
    academic_degree: str
    worldview: str
    address: str


class Validator:
    """Validator class"""
    nodes: list[Node]

    def __init__(self, nodes: list[Node]):
        """Validator constructor"""
        self.nodes = []

        for i in nodes:
            self.nodes.append(i)

    def parse_bad(self) -> dict:
        """Get good nodes"""
        bad_nodes = {
            "email": 0,
            "weight": 0,
            "inn": 0,
            "passport_series": 0,
            "university": 0,
            "work_experience": 0,
            "academic_degree": 0,
            "worldview": 0,
            "address": 0
        }

        for i in self.nodes:
            illkeys = self.parse_node(i)
            keys = illkeys.keys()

            for key in keys:
                bad_nodes[key] += illkeys[key]

        return bad_nodes

    def parse_good(self) -> list[Node]:
        """Get bad nodes"""
        good_nodes: list[Node] = []

        for i in self.nodes:
            bad_keys = self.parse_node(i)
            keys = bad_keys.keys()
            flag = 0

            for key in keys:
                if bad_keys[key] > 0:
                    flag += 1
                    break

            if flag == 0:
                good_nodes.append(i)

        return good_nodes

    def parse_node(self, node: Node) -> dict[str, int]:
        """Parse one element"""
        bad_keys = {
            "email": 0,
            "weight": 0,
            "inn": 0,
            "passport_series": 0,
            "university": 0,
            "work_experience": 0,
            "academic_degree": 0,
            "worldview": 0,
            "address": 0
        }

        if not self.check_email(node['email']):
            bad_keys['email'] += 1
        if not self.check_inn(node['inn']):
            bad_keys['inn'] += 1
        if not self.check_passport(node['passport_series']):
            bad_keys['passport_series'] += 1
        if not self.check_weight(node['weight']):
            bad_keys['weight'] += 1
        if not self.check_work_experience(node['work_experience']):
            bad_keys['work_experience'] += 1
        if not self.check_address(node['address']):
            bad_keys['address'] += 1
        if not self.check_university(node['university']):
            bad_keys['university'] += 1
        if not self.check_degree(node['academic_degree']):
            bad_keys['academic_degree'] += 1
        if not self.check_worldview(node['worldview']):
            bad_keys['worldview'] += 1

        return bad_keys

    def check_email(self, email: str) -> bool:

        pattern = "[^\\s@]+@([^\\s@.,]+\\.)+[^\\s@.,]{2,}"
        if re.match(pattern, email):
            return True
        return False

    def check_inn(self, inn: str) -> bool:

        pattern = '^\\d{12}$'

        if re.match(pattern, inn):
            return True
        return False

    def check_passport(self, passport: str) -> bool:
        pattern = '[0-9]+\s[0-9]+'

        if re.match(pattern, passport):
            return True
        return False

    def check_weight(self, weight: str) -> bool:
        try:
            int_w = int(weight)
        except ValueError:
            return False

        return 300 > int_w > 30

    def check_work_experience(self, work_experience: str) -> bool:
        try:
            int_exp = int(work_experience)
        except ValueError:
            return False

        return 50 > int_exp > 0

    def check_address(self, address: str) -> bool:

        pattern = ".+[0-9]+"

        if re.match(pattern, address):
            return True
        return False

    def check_university(self, university: str) -> bool:

        pattern = "[а-яА-Я]+"

        if re.match(pattern, university):
            return True
        return False

    def check_degree(self, degree: str) -> bool:

        pattern = "(Специалист)|(Кандидат наук)|(Магистр)|(Бакалавр)|(Доктор наук)"

        if re.match(pattern, degree):
            return True
        return False

    def check_worldview(self, worldview: str) -> bool:

        pattern = "(^[а-яА-Я]+$)|(^[а-яА-Я]+\s[а-я]+$)"

        if re.match(pattern, worldview):
            return True
        return False


class FileReader:
    """Reads file data"""
    data: list[Node]

    def __init__(self, path) -> None:
        """Reader contstructor"""
        self.data = json.load(open(path, encoding='windows-1251'))

    def get_data(self) -> list[Node]:
        """Get all nodes"""
        return self.data


def create_parser():
    pars = argparse.ArgumentParser()

    pars.add_argument('--input', default='input.txt')
    pars.add_argument('--output', default='output.txt')

    return pars


parser = create_parser()
namespace = parser.parse_args()

input_path = namespace.input
output_path = namespace.output

file = FileReader(input_path)
validator = Validator(FileReader(input_path).get_data())
print(validator.parse_bad())

f = open(output_path, 'w')
for i in validator.parse_good():
    f.write(str(i) + '\n')
