import npyscreen
from models.listener import Listener


class SubscribeToRelease(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.wgText = self.add(npyscreen.TitleText)
        self.wgReleases = self.add(npyscreen.TitleMultiSelect, name="Release:", max_height=4)
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        self.wgReleases.add_handlers({
            "^D": self.unset_select
        })
        self.wgReleases.values = self.parentApp.database.get_all_releases()
        subscribed = self.parentApp.database.get_releases_by_listener_id(self.value)

        values = []
        for release in subscribed:
            index = subscribed.index(release)
            if index != -1:
                values.append(index)

        self.wgReleases.value = values

        # names = list(map(lambda x: {"name": x['name'], "id": x['id']}, releases))
        #
        # value = list(map(lambda x: {"name": x['name'], "id": x['id']}, subscribed))
        # raise (Exception(names, value))
        # if self.value:
        #     self.name = "Edit"
        #     self.wgText.value = f"Subscribe listener to"
        #     self.wgText.editable = False
        #     self.wgRelease.values = names
        #     self.wgRelease.value = value
        #     # f = open("log.txt", "w")
        #     # f.write(f'record : {record}')
        # else:
        #     return None

    def on_ok(self):
        if len(self.wgReleases.value) != 0:
            releases = self.wgReleases.value
            releases_id = []
            for release in releases:
                releases_id.append(self.wgReleases.values[release][0])

            self.parentApp.database.update_all_subscriptions_by_listener_id(self.value, releases_id)

            # for i in releases:
            #     releases_id.append(i['id'])

                # try:
                #     self.parentApp.database.delete_all_subscriptions_by_listener_id(self.value)
                #     self.parentApp.database.add_listener_release(int(self.value), int(release["id"]))
                # except:
                #     ...

            self.parentApp.switchFormPrevious()
        else:
            # TODO make popup
            self.is_error = True
            self.spawn_notify_popup(self.wgMusicianName.value)


    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()

    def unset_select(self, *args, **keywords):
        self.wgReleases.value = []

