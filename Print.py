from prettytable import PrettyTable
from datetime import datetime, timedelta, date
import Domain


def people(repository):
    personTable = PrettyTable()
    personTable.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    print("Individuals:")
    for person in repository.getPeople():
        birthday = datetime.strptime(person.getBirthDate().replace(" ", "/"), "%d/%b/%Y").strftime('%m/%d/%Y')
        age = int((datetime.today().date() - datetime.strptime(birthday, '%m/%d/%Y').date()).days / 365)
        personTable.add_row([person.getIndiId(),
                             person.getName(),
                             person.getSex(),
                             birthday,
                             age,
                             person.getDeathDate() is None,
                             formatValue(person.getDeathDate()),
                             formatValue(person.getChildFamilyId()),
                             formatValue(person.getSpousalFamilyIds())])
    print(personTable)


def deadPeople(repository):
    deathTable = PrettyTable()
    deathTable.field_names = ["ID", "Name", "Death Date"]
    for person in repository.getPeople():
        if person.getDeathDate() is not None:
            deathTable.add_row([person.getIndiId(), person.getName(), person.getDeathDate()])
    print('US29: The following people are dead:')
    print(deathTable)


def livingMarriedPeople(repository):
    marriageTable = PrettyTable()
    marriageTable.field_names = ["ID", "Name", "Role", "Family ID"]
    for person in repository.getPeople():
        if person.getDeathDate() is None and person.getSpousalFamilyIds():
            for familyId in person.getSpousalFamilyIds():
                if repository.getFamily(familyId).getDivorceDate() is None:
                    if person.getSex() == Domain.Sex.MALE.value:
                        role = 'Husband'
                    else:
                        role = 'Wife'
                    marriageTable.add_row([person.getIndiId(), person.getName(), role, person.getSpousalFamilyIds()])
                    break
    print('US30: The following people are living and married:')
    print(marriageTable)


def families(repository):
    familyTable = PrettyTable()
    familyTable.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name",
                               "Children"]
    for family in repository.getFamilies():
        familyTable.add_row([family.getFamId(),
                             formatDate(family.getMarriageDate()),
                             formatDate(family.getDivorceDate()),
                             family.getHusbandId(),
                             repository.getPerson(family.getHusbandId()).getName(),
                             family.getWifeId(),
                             repository.getPerson(family.getWifeId()).getName(),
                             family.getChildrenIds()])
    print("Families:")
    print(familyTable)


def upcomingAnniversaries(repository):
    anniversaryTable = PrettyTable()
    thirtyDaysAgo = datetime.now().date() - timedelta(30)
    anniversaryTable.field_names = ["ID", "Anniversary Date", "Husband ID", "Husband Name", "Wife ID", "Wife Name"]
    for family in repository.getFamilies():
        if getDateFromString(family.getMarriageDate()) >= thirtyDaysAgo:
            anniversaryTable.add_row([family.getFamId(),
                                      formatDate(family.getMarriageDate()),
                                      family.getHusbandId(),
                                      repository.getPerson(family.getHusbandId()).getName(),
                                      family.getWifeId(),
                                      repository.getPerson(family.getWifeId()).getName()])
            print("Recent Anniversaries:")
            print(anniversaryTable)


def getDateFromString(string):
    return date(*map(int, formatDate(string).split('-')))


def formatDate(date):
    if date is None:
        return "NA"
    else:
        return datetime.strptime(date.replace(" ", "/"), "%d/%b/%Y").strftime('%Y-%m-%d')


def formatValue(value):
    if value is None or not value:
        return 'NA'
    else:
        return value
