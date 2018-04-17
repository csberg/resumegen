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
            'start_date' TEXT NOT NULL,\
            'end_date' TEXT,\
            'name' TEXT NOT NULL\
        );\
        CREATE TABLE IF NOT EXISTS 'company_role' (\
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
        c.execute('SELECT * from basic_information')
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
        c.execute('SELECT * from val_item_type')
        records = c.fetchall()
        c.close()
        return records

    def get_item_type(self, id=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('SELECT * from val_item_type where id=?', (id,))
        records = c.fetchall()
        c.close()
        return records[0]


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

class ItemTypeList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(ItemTypeList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record,
            "^B": self.parent.parentApp.switchFormPrevious
        })

    def display_value(self, vl):
        return "%s" % (vl[1])

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EditItemType').value = act_on_this[0]
        self.parent.parentApp.switchForm('EditItemType')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EditItemType').value = None
        self.parent.parentApp.switchForm('EditItemType')

    def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.myDatabase.delete_item_type(self.values[self.cursor_line][0])
        self.parent.update_list()

    def change_forms(self, *args, **keywords):
        if self.name == "Review Item Types":
            change_to = "ItemTypes"
        elif self.name == "Review Personal Information":
            change_to = "Personal"
        else:
            change_to = "MAIN"

        # Tell the MyTestApp object to change forms.
        self.parent.parentApp.change_form(change_to)



class ItemTypeListDisplay(npyscreen.FormMuttActiveWithMenus):
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




class MainMenu(npyscreen.Form):
    def create(self):
        #self.add(npyscreen.TitleText, name="Main Menu")
        self.add(npyscreen.TitleFixedText, editable=False, name="Welcome to ResumeGen!")
        self.add(npyscreen.ButtonPress, name="Personal Information",
                 when_pressed_function=lambda: self.parentApp.switchForm("Personal"))
        self.add(npyscreen.ButtonPress, name="Item Types",
                 when_pressed_function=lambda: self.parentApp.switchForm("ItemTypes"))
        self.add(npyscreen.ButtonPress, name="Quit (Q)", when_pressed_function=lambda: self.parentApp.switchForm(None))
        self.add_handlers({"q": lambda x: self.parentApp.switchForm(None),
                           "Q": lambda x: self.parentApp.switchForm(None)})
        # self.add(self.mainMenu, name="Main Menu")
        #self.mainMenu = self.add_menu(name="Main Menu")

# Menu items
# Resume Items
# Resume Item Classes
# Personal Information
# Certifications
# Company and Role Information
# Generate a Resume



class ResumeGenApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.myDatabase = ResumeDatabase()
        self.addForm("Personal", EditPersonalInformation, "Review Personal Information")
        self.addForm("MAIN", MainMenu)
        self.addForm("ItemTypes", ItemTypeListDisplay, "View Item Types")
        self.addForm("EditItemType", EditItemTypes, "Edit Item Types")

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

