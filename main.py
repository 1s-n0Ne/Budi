import random

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.progressindicator import MDLinearProgressIndicator
from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image

from kivy.core.window import Window
from kivy_garden.mapview import MapView

Window.size = (540, 960)


class StatisticsTable(MDGridLayout):
    def __init__(self, **kwargs):
        super(StatisticsTable, self).__init__(**kwargs)
        self.cols = 5
        grid_dict = {1: 'Día', 2: 'Semana', 3: 'Mes', 4: 'Año'}
        transport_icons = {5: 'car', 10: 'bus', 15: 'bike', 20: 'pedestrian'}

        for i in range(5*5):
            if i in grid_dict:
                label = MDLabel(text=grid_dict[i],
                                font_style='Headline',
                                role='small',
                                halign="center")
            else:
                if i == 0:
                    label = MDLabel(text='', halign="center")

                elif i % 5 == 0 and i > 0:
                    label = Image(source=f'icons/{transport_icons[i]}.png',
                                  pos_hint={"center_x": .5, 'center_y': .5},
                                  size=(10, 10))
                else:
                    label = MDLabel(text='--', halign="center")

            self.add_widget(label)


class MainScreen(MDScreen):
    pass


class MapScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MapScreen, self).__init__(**kwargs)
        self.add_widget(MapView(zoom=16, lat=20.653, lon=-103.391))


class MissionCard(MDCard):
    def __init__(self, **kwargs):
        super(MissionCard, self).__init__(**kwargs)
        self.style = 'filled'
        missionData = MDBoxLayout(orientation='horizontal', padding=(10, 10))
        progress = MDBoxLayout(orientation='vertical', padding=(10, 10))
        progress.add_widget(MDLabel(text='Este es el texto de una mision'))
        progress.add_widget(MDLinearProgressIndicator(
            value=random.randint(25,100),
            size_hint_y=0.4
        ))
        missionData.add_widget(Image(source='icons/mission.png', size_hint_x=0.45))
        missionData.add_widget(progress)

        self.add_widget(missionData)

class ChallengeScreen(MDScreen):
    def __init__(self, **kwargs):
        super(ChallengeScreen, self).__init__(**kwargs)
        missions = MDBoxLayout(orientation='vertical', spacing=10, padding=(10, 10))
        for i in range(4):
            missions.add_widget(MissionCard())
        self.add_widget(missions)


class MainApp(MDApp):
    def open_menu(self, item):
        menu_items = [
            {
                "text": f"{i}",
                "on_release": lambda x=f"Item {i}": self.menu_callback(x),
            } for i in range(5)
        ]
        MDDropdownMenu(caller=item, items=menu_items).open()

    def menu_callback(self, text_item):
        self.root.ids.drop_text.text = text_item

    def on_switch_tabs(
            self,
            bar: MDNavigationBar,
            item: MDNavigationItem,
            item_icon: str,
            item_text: str,
    ):
        self.root.ids.screen_manager.current = item_text

    def build(self):
        return Builder.load_file('budi.kv')

    def on_start(self):
        super().on_start()


if __name__ == "__main__":
    MainApp().run()

# Realiza un viaje a pie
# Camina 500 metros
# Realiza un viaje en autobus
# No relizes unn viaje en coche