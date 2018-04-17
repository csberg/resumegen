#!/usr/bin/env python
# encoding: utf-8

import npyscreen, curses, sqlite3

class ResumeDatabase(object):
    def __init__(self, filename="resume.db"):
        self.dbfilename = filename
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.executescript(
        "CREATE TABLE IF NOT EXISTS 'certifications' (\
            'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
            'start_date' TEXT NOT NULL,\
            'end_date' TEXT,\
            'name' TEXT NOT NULL\
        );\
        CREATE TABLE IF NOT EXISTS 'company_role' (\
            'id' INTEGER PRIMARY KEY AUTOINCREMENT,\
            'start_date' TEXT NOT NULL,\
            'end_date' TEXT NOT NULL,\
            'company' TEXT NOT NULL,\
            'role' TEXT,\
            'description' TEXT\
        );\
        CREATE TABLE IF NOT EXISTS 'val_item_class' (\
            'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
            'name' TEXT NOT NULL\
        );\
        CREATE TABLE IF NOT EXISTS 'val_item_type' (\
            'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
            'name' TEXT\
        );\
        CREATE TABLE IF NOT EXISTS 'item_class' (\
            'item_id' INTEGER NOT NULL,\
            'item_class_id' TEXT NOT NULL\
        );\
        CREATE TABLE IF NOT EXISTS 'items' (\
            'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
            'item_type_id' REAL NOT NULL,\
            'company_id' INTEGER NOT NULL,\
            'description' TEXT\
        );\
        CREATE TABLE IF NOT EXISTS 'basic_information' (\
            'name' TEXT NOT NULL,\
            'email' TEXT NOT NULL,\
            'location' TEXT NOT NULL,\
            'phone_number' TEXT NOT NULL);"
            )
        db.commit()
        c.close()

    def add_basic_info(self, name='', email='', phone='', location=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('INSERT INTO basic_information(name, email, location, phone_number) \
                    VALUES(?,?,?,?)', (name, email, location, phone))
        db.commit()
        c.close()

    def update_basic_info(self, name = '', email='', phone='', location=''):
        self.delete_basic_info()
        self.add_basic_info(name, email, phone, location)

    def delete_basic_info(self):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('DELETE FROM basic_information')
        db.commit()
        c.close()

    # Figure out why I need that blank ID and why I can't call without it on both ends.
    def get_basic_info(self, id=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('SELECT * FROM basic_information')
        records = c.fetchone()
        c.close()
        return records

    # Start val_item_type
    def add_item_type(self, item_type=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('INSERT INTO val_item_type(name) \
                    VALUES(?)', (item_type,))
        db.commit()
        c.close()

    def update_item_type(self, id='', item_type=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('UPDATE val_item_type SET name=? WHERE id=?', (item_type, id))
        db.commit()
        c.close()

    def delete_item_type(self, id=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('DELETE FROM val_item_type WHERE id=?', (id,))
        db.commit()
        c.close()

    def get_all_item_types(self):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('SELECT * FROM val_item_type ORDER BY name')
        records = c.fetchall()
        c.close()
        return records

    def get_item_type(self, id=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('SELECT * FROM val_item_type WHERE id=?', (id,))
        records = c.fetchall()
        c.close()
        return records[0]

    # Start certifications
    def add_cert(self, start_date='', end_date='', name=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('INSERT INTO certifications(start_date, end_date, name) \
                    VALUES(?,?,?)', (start_date, end_date, name,))
        db.commit()
        c.close()

    def update_cert(self, id='', start_date='', end_date='', name=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('UPDATE certifications SET start_date=?, end_date=?, name=? WHERE id=?',
                  (id, start_date, end_date, name,))
        db.commit()
        c.close()

    def delete_cert(self, id=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('DELETE FROM certifications WHERE id=?', (id,))
        db.commit()
        c.close()

    def get_all_certs(self):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('SELECT * FROM certifications ORDER BY name')
        records = c.fetchall()
        c.close()
        return records

    def get_cert(self, id=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('SELECT * FROM certifications WHERE id=?', (id,))
        records = c.fetchone()
        c.close()
        return records

    # Start CLASSES
    def add_class(self, name=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('INSERT INTO val_item_class(name) \
                    VALUES(?)', (name,))
        db.commit()
        c.close()

    def update_class(self, id='', name=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('UPDATE val_item_class SET name=? WHERE id=?',
                  (name, id,))
        db.commit()
        c.close()

    def delete_class(self, id=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('DELETE FROM val_item_class WHERE id=?', (id,))
        db.commit()
        c.close()

    def get_all_class(self):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('SELECT * FROM val_item_class ORDER BY name')
        records = c.fetchall()
        c.close()
        return records

    def get_class(self, id=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('SELECT * FROM val_item_class WHERE id=?', (id,))
        records = c.fetchone()
        c.close()
        return records
    # END CLASSES

    # START COMPANY/ROLE INFO
    def add_company_role(self, start_date='', end_date='', company='', role='', description=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('INSERT INTO company_role(start_date, end_date, company, role, description) \
                    VALUES(?, ?, ?, ?, ?)', (start_date, end_date, company, role, description,))
        db.commit()
        c.close()

    def update_company_role(self, id='', start_date='', end_date='', company='', role='', description=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('UPDATE company_role SET start_date=?, end_date=?, company=?, role=?, description=? WHERE id=?',
                  (start_date, end_date, company, role, description, id,))
        db.commit()
        c.close()

    def delete_company_role(self, id=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('DELETE FROM company_role WHERE id=?', (id,))
        db.commit()
        c.close()

    def get_all_company_role(self):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('SELECT * FROM company_role ORDER BY end_date')
        records = c.fetchall()
        c.close()
        return records

    def get_company_role(self, id=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('SELECT * FROM company_role WHERE id=?', (id,))
        records = c.fetchone()
        c.close()
        return records
    # END COMPANY/ROLE INFO

class EditPersonalInformation(npyscreen.ActionForm):
    def create(self):
        self.value = None

        if (self.parentApp.myDatabase.get_basic_info(self.value)):
            self.value = True

        self.piPersonName = self.add(npyscreen.TitleText, name='Name:')
        self.piEmail      = self.add(npyscreen.TitleText, name='E-mail:')
        self.piLocation   = self.add(npyscreen.TitleText, name='Location:')
        self.piPhone      = self.add(npyscreen.TitleText, name='Phone Number:')

    def beforeEditing(self):
        if self.value:
            record = self.parentApp.myDatabase.get_basic_info(self.value)
            self.name = "Editing Existing Information"
            self.piPersonName.value = record[0]
            self.piEmail.value      = record[1]
            self.piLocation.value   = record[2]
            self.piPhone.value      = record[3]
        else:
            self.name = "New Personal Information"
            self.piPersonName.value = ''
            self.piEmail.value      = ''
            self.piLocation.value   = ''
            self.piPhone.value      = ''

    def on_ok(self):
        if self.value: # We are editing an existing record
            self.parentApp.myDatabase.update_basic_info(name        = self.piPersonName.value,
                                                        email       = self.piEmail.value,
                                                        location    = self.piLocation.value,
                                                        phone       = self.piPhone.value
                                            )
        else: # We are adding a new record.
            self.parentApp.myDatabase.add_basic_info(name            = self.piPersonName.value,
                                                         email       = self.piEmail.value,
                                                         location    = self.piLocation.value,
                                                         phone       = self.piPhone.value
            )
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

# START CERTS
class CertList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(CertList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record,
            "^B": self.go_back
        })

    def display_value(self, vl):
        return "%s, %s, %s, %s" % (vl[0], vl[1], vl[2], vl[3])

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EditCerts').value = act_on_this[0]
        self.parent.parentApp.switchForm('EditCerts')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EditCerts').value = None
        self.parent.parentApp.switchForm('EditCerts')

    def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.myDatabase.delete_cert(self.values[self.cursor_line][0])
        self.parent.update_list()

    def go_back(self, *args, **keywords):
        self.parent.parentApp.switchForm("MAIN")


class CertListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = CertList

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wStatus1.value = 'Certifications'
        self.wMain.values = self.parentApp.myDatabase.get_all_certs()
        self.wMain.display()


class EditCerts(npyscreen.ActionForm):
    def create(self):
        self.value          = None
        self.certName       = self.add(npyscreen.TitleText, name="Certification:", )
        self.certStartDate  = self.add(npyscreen.TitleText, name="Start Date:", )
        self.certEndDate    = self.add(npyscreen.TitleText, name="End Date:", )

    def beforeEditing(self):
        if self.value:
            record = self.parentApp.myDatabase.get_cert(self.value)
            self.name = "Certification ID : %s" % record[0]
            self.record_id              = record[0]
            self.certStartDate.value    = record[1]
            self.certEndDate.value      = record[2]
            self.certName.value         = record[3]
        else:
            self.name = "New Certification (Good for you!)"
            self.record_id              = ''
            self.certStartDate.value    = ''
            self.certEndDate.value      = ''
            self.certName.value         = ''

    def on_ok(self):
        if self.record_id:  # We are editing an existing record
            self.parentApp.myDatabase.update_cert(self.record_id,
                                                  start_date        = self.certStartDate.value,
                                                  end_date          = self.certEndDate.value,
                                                  name              = self.certName.value,
                                                )
        else:  # We are adding a new record.
            self.parentApp.myDatabase.add_cert(   start_date        = self.certStartDate.value,
                                                  end_date          = self.certEndDate.value,
                                                  name              = self.certName.value,
                                                  )

        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
# END CERTS


# START CLASSES
class ClassList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(ClassList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record,
            "^B": self.go_back
        })

    def display_value(self, vl):
        return "%s, %s" % (vl[0], vl[1])

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EditClass').value = act_on_this[0]
        self.parent.parentApp.switchForm('EditClass')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EditClass').value = None
        self.parent.parentApp.switchForm('EditClass')

    def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.myDatabase.delete_class(self.values[self.cursor_line][0])
        self.parent.update_list()

    def go_back(self, *args, **keywords):
        self.parent.parentApp.switchForm("MAIN")


class ClassListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = ClassList

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wStatus1.value = 'Classifications'
        self.wMain.values = self.parentApp.myDatabase.get_all_class()
        self.wMain.display()


class EditClass(npyscreen.ActionForm):
    def create(self):
        self.value          = None
        self.className      = self.add(npyscreen.TitleText, name="Classification:", )

    def beforeEditing(self):
        if self.value:
            record = self.parentApp.myDatabase.get_class(self.value)
            self.name = "Classification ID : %s" % record[0]
            self.record_id          = record[0]
            self.className.value    = record[1]
        else:
            self.name = "New Classification"
            self.record_id          = ''
            self.className.value    = ''

    def on_ok(self):
        if self.record_id:  # We are editing an existing record
            self.parentApp.myDatabase.update_class( self.record_id,
                                                    name            = self.className.value,)
        else:  # We are adding a new record.
            self.parentApp.myDatabase.add_class(name = self.className.value,)

        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
# END CLASSES

# BEGIN COMPANY/ROLE
class CompanyRoleList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(CompanyRoleList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record,
            "^B": self.go_back
        })

    def display_value(self, vl):
        return "%s, %s, %s, %s, %s, %s" % (vl[0], vl[1], vl[2], vl[3], vl[4], vl[5])

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EditCompanyRole').value = act_on_this[0]
        self.parent.parentApp.switchForm('EditCompanyRole')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EditCompanyRole').value = None
        self.parent.parentApp.switchForm('EditCompanyRole')

    def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.myDatabase.delete_company_role(self.values[self.cursor_line][0])
        self.parent.update_list()

    def go_back(self, *args, **keywords):
        self.parent.parentApp.switchForm("MAIN")


class CompanyRoleListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = CompanyRoleList

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wStatus1.value = 'Company / Role Information'
        self.wMain.values = self.parentApp.myDatabase.get_all_company_role()
        self.wMain.display()


class EditCompanyRole(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.crStartDate    = self.add(npyscreen.TitleText, name="Start Date:", )
        self.crEndDate      = self.add(npyscreen.TitleText, name="End Date:", )
        self.crCompany      = self.add(npyscreen.TitleText, name="Company:", )
        self.crRole         = self.add(npyscreen.TitleText, name="Role:", )
        self.crDescText     = self.add(npyscreen.FixedText, value="Description:")
        self.crDescription  = self.add(npyscreen.MultiLineEdit, name="Description:", )

    def beforeEditing(self):
        if self.value:
            record = self.parentApp.myDatabase.get_company_role(self.value)
            self.name = "Company / Role ID : %s" % record[0]
            self.record_id              = record[0]
            self.crStartDate.value      = record[1]
            self.crEndDate.value        = record[2]
            self.crCompany.value        = record[3]
            self.crRole.value           = record[4]
            self.crDescription.value    = record[5]
        else:
            self.name = "New Company / Role"
            self.record_id              = ''
            self.crStartDate.value      = ''
            self.crEndDate.value        = ''
            self.crCompany.value        = ''
            self.crRole.value           = ''
            self.crDescription.value    = ''

    def on_ok(self):
        if self.record_id:  # We are editing an existing record
            self.parentApp.myDatabase.update_company_role(self.record_id,
                                                            start_date   = self.crStartDate.value,
                                                            end_date     = self.crEndDate.value,
                                                            company      = self.crCompany.value,
                                                            role         = self.crRole.value,
                                                            description  = self.crDescription.value,
                                                            )
        else:  # We are adding a new record.
            self.parentApp.myDatabase.add_company_role(start_date       = self.crStartDate.value,
                                                       end_date         = self.crEndDate.value,
                                                       company          = self.crCompany.value,
                                                       role             = self.crRole.value,
                                                       description      = self.crDescription.value,
                                                       )

        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
# END COMPANY/ROLE


# BEGIN ITEMTYPES
class ItemTypeList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(ItemTypeList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record,
            "^B": self.go_back
        })

    def display_value(self, vl):
        return "%s, %s" % (vl[0], vl[1])

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EditItemType').value = act_on_this[0]
        self.parent.parentApp.switchForm('EditItemType')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EditItemType').value = None
        self.parent.parentApp.switchForm('EditItemType')

    def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.myDatabase.delete_item_type(self.values[self.cursor_line][0])
        self.parent.update_list()

    def go_back(self, *args, **keywords):
        self.parent.parentApp.switchForm("MAIN")


class ItemTypeListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = ItemTypeList

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wStatus1.value = 'Item Types'
        self.wMain.values = self.parentApp.myDatabase.get_all_item_types()
        self.wMain.display()



class EditItemTypes(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.itTypeName = self.add(npyscreen.TitleText, name="Item Type:", )

    def beforeEditing(self):
        if self.value:
            record = self.parentApp.myDatabase.get_item_type(self.value)
            self.name = "Item Type ID : %s" % record[0]
            self.record_id = record[0]
            self.itTypeName.value = record[1]
        else:
            self.name = "New Item Type"
            self.record_id = ''
            self.itTypeName.value = ''

    def on_ok(self):
        if self.record_id:  # We are editing an existing record
            self.parentApp.myDatabase.update_item_type(self.record_id,
                                                    item_type=self.itTypeName.value,
                                                    )
        else:  # We are adding a new record.
            self.parentApp.myDatabase.add_item_type(item_type=self.itTypeName.value,)

        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
# END ITEMTYPES


class MainMenu(npyscreen.Form):
    def create(self):
        #self.add(npyscreen.TitleText, name="Main Menu")
        self.add(npyscreen.TitleFixedText, editable=False, name="Welcome to ResumeGen!")
        self.add(npyscreen.ButtonPress, name="Item Types",
                 when_pressed_function=lambda: self.parentApp.switchForm("ItemTypes"))
        self.add(npyscreen.ButtonPress, name="Item Classes",
                 when_pressed_function=lambda: self.parentApp.switchForm("Classes"))
        self.add(npyscreen.ButtonPress, name="Personal Information",
                 when_pressed_function=lambda: self.parentApp.switchForm("Personal"))
        self.add(npyscreen.ButtonPress, name="Certifications",
                 when_pressed_function=lambda: self.parentApp.switchForm("Certifications"))
        self.add(npyscreen.ButtonPress, name="Company and Role Information",
                 when_pressed_function=lambda: self.parentApp.switchForm("CompanyRole"))
        self.add(npyscreen.ButtonPress, name="Quit (Q)", when_pressed_function=lambda: self.parentApp.switchForm(None))
        self.add_handlers({"q": lambda x: self.parentApp.switchForm(None),
                           "Q": lambda x: self.parentApp.switchForm(None)})

# Resume Items
# Generate a Resume


class ResumeGenApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.myDatabase = ResumeDatabase()
        self.addForm("MAIN", MainMenu)
        self.addForm("Personal", EditPersonalInformation, "Review Personal Information")
        self.addForm("ItemTypes", ItemTypeListDisplay, "View Item Types")
        self.addForm("EditItemType", EditItemTypes, "Edit Item Types")
        self.addForm("Certifications", CertListDisplay, "View Certifications")
        self.addForm("EditCerts", EditCerts, "Edit Certifications")
        self.addForm("Classes", ClassListDisplay, "View Item Classes")
        self.addForm("EditClass", EditClass, "Edit Item Class")
        self.addForm("CompanyRole", CompanyRoleListDisplay, "View Company and Role Information")
        self.addForm("EditCompanyRole", EditCompanyRole, "Edit Company and Role Information")

    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")

    def change_form(self, name):
        # Switch forms.  NB. Do *not* call the .edit() method directly (which
        # would lead to a memory leak and ultimately a recursion error).
        # Instead, use the method .switchForm to change forms.
        self.switchForm(name)

        # By default the application keeps track of every form visited.
        # There's no harm in this, but we don't need it so:
        self.resetHistory()




'''
def main():
    TA = ResumeGenerator()
    TA.run()
'''


if __name__ == '__main__':
    resumeGen = ResumeGenApp()
    resumeGen.run()

