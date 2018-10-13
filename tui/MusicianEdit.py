import npyscreen
from models.musician import Musician


class MusicianEdit(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.wgName = self.add(npyscreen.TitleText, name="Name:",)
        self.wgMembers = self.add(npyscreen.TitleText, name="Members:")

    def beforeEditing(self):
        if self.value:
            musician = self.parentApp.database.get_musician_by_id(self.value)
            self.name = "Edit"
            self.record_id = musician["id"]
            self.wgName.value = musician["name"]
            self.wgMembers.value = ','.join(map(str, musician["members"]))
            # f = open("log.txt", "w")
            # f.write(f'record : {record}')
        else:
            self.name = "New Musician"
            self.record_id = ''
            self.wgName.value = ''
            self.wgMembers.value = ''

    def on_ok(self):
        if self.record_id: # We are editing an existing record
            musician = Musician(self.wgName.value, self.wgMembers.value.split(','))
            self.parentApp.database.update_musician_by_id(self.record_id, musician)
        else: # We are adding a new record.
            musician = Musician(self.wgName.value, self.wgMembers.value.split(','))
            self.parentApp.database.create_new_musician(musician)
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()