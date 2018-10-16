import npyscreen
from models.musician import Musician, Status


class MusicianEdit(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.wgName = self.add(npyscreen.TitleText, name="Name:")
        self.wgMembers = self.add(npyscreen.TitleText, name="Members:")
        self.wgStatus = self.add(npyscreen.TitleSelectOne,
                                 name="Status:",
                                 values=Status.get_all())
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        self.statuses = Status.get_all()
        if self.value:
            musician = self.parentApp.database.get_musician_by_id(self.value)
            self.name = "Edit"
            self.record_id = musician["id"]
            self.wgName.value = musician["name"]
            self.wgMembers.value = ','.join(map(str, musician["members"]))
            self.wgStatus.value = self.statuses.index(musician["status"])
            # f = open("log.txt", "w")
            # f.write(f'record : {record}')
        else:
            self.name = "New Musician"
            self.record_id = ''
            self.wgName.value = ''
            self.wgMembers.value = ''
            self.wgStatus.value = ''

    def on_ok(self):
        status = self.wgStatus.values[self.wgStatus.value[0]]
        musician = Musician(self.wgName.value, status, self.wgMembers.value.split(','))
        if self.record_id: # We are editing an existing record
            self.parentApp.database.update_musician_by_id(self.record_id, musician)
        else: # We are adding a new record.
            self.parentApp.database.create_new_musician(musician)
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()
