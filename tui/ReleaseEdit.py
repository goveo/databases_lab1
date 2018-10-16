import npyscreen
import numpy as np
from models.release import Release


class ReleaseEdit(npyscreen.ActionForm):
    # TODO create quit handlers
    def create(self):
        self.value = None
        self.wgName = self.add(npyscreen.TitleText, name="Name:", value="")
        self.wgStyle = self.add(npyscreen.TitleText, name="Style:", value="")
        self.wgDate = self.add(npyscreen.TitleDateCombo, name="Date:", value="")
        self.wgIsVideo = self.add(npyscreen.RoundCheckBox, name="Is video:", value=False)
        self.wgMusicianName = self.add(npyscreen.TitleSelectOne, name="Author:", max_height=4)
        self.is_error = False
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        musicians = self.parentApp.database.get_all_musicians()
        names = list(map(lambda x: x['name'], musicians))
        self.wgMusicianName.values = names
        self.wgIsVideo.add_handlers({
            "^V": self.unset_video
        })

        if self.value:
            release = self.parentApp.database.get_release_by_id(self.value)
            mus_id = release["musicianid"]
            musician = self.parentApp.database.get_musician_by_id(mus_id)
            self.name = "Edit"
            self.record_id = release["id"]
            self.wgName.value = release["name"]
            self.wgStyle.value = release["style"]
            self.wgDate.value = release["date"]
            self.wgMusicianName.value = names.index(musician["name"])
        elif self.is_error is True:
            self.is_error = False
            # Try again
        else:
            self.name = "New Release"
            self.record_id = None
            self.wgMusicianName.value = None
            self.wgName.value = ''
            self.wgStyle.value = ''
            self.wgDate.value = ''
            self.wgIsVideo.value = False

    def on_ok(self):
        if self.wgMusicianName.value:
            musician_name = self.wgMusicianName.values[self.wgMusicianName.value[0]]
            musician = self.parentApp.database.get_musician_by_name(musician_name)
            release = Release(self.wgName.value,
                              self.wgDate.value,
                              self.wgStyle.value,
                              self.wgIsVideo.value,
                              musician["id"])

            # We are editing an existing record
            if self.record_id is not None:
                self.parentApp.database.update_release_by_id(self.record_id, release)
            # We are adding a new record
            else:
                self.parentApp.database.create_new_release(release)
            self.parentApp.switchFormPrevious()
        else:
            # TODO make popup
            self.is_error = True
            self.spawn_notify_popup(self.wgMusicianName.value)

    def on_cancel(self):
        self.is_error = False
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()

    def spawn_notify_popup(self, entity):
        message_to_display = f'Please select author'
        notify_result = npyscreen.notify_confirm(message_to_display, title='Error')

    def unset_video(self, *args, **keywords):
        self.wgIsVideo.value = False

