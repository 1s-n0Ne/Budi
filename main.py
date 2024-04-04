import random

import requests
import polyline
from kivy.lang import Builder
from kivy.properties import ObjectProperty

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
from kivy.graphics import Color, Line
from kivy.graphics.transformation import Matrix
from kivy.graphics.context_instructions import Translate, Scale
from kivy_garden.mapview import MapView, MapLayer

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


class LineMapLayer(MapLayer):
    def __init__(self, **kwargs):
        super(LineMapLayer, self).__init__(**kwargs)
        self.zoom = 0

    def reposition(self):
        mapview = self.parent

        #: Must redraw when the zoom changes
        #: as the scatter transform resets for the new tiles
        if (self.zoom != mapview.zoom):
            self.draw_line()

    def draw_line(self, *args):
        mapview = self.parent
        self.zoom = mapview.zoom
        res = requests.get('https://budiserver-h4gt44kccq-uc.a.run.app/alternateRouter')
        candidates = res.json()

        lines = []
        for method in candidates:
            line = polyline.decode(candidates[method]['polyline'])

            point_list = []
            for point in line:
                screen_point = mapview.get_window_xy_from(point[0], point[1], mapview.zoom)
                point_list.append(screen_point)

            lines.append(point_list)

            # When zooming we must undo the current scatter transform
            # or the animation makes the line misplaced
        scatter = mapview._scatter
        x,y,s = scatter.x, scatter.y, scatter.scale

        with self.canvas:
            self.canvas.clear()
            Scale(1/s,1/s,1)
            Translate(-x,-y)
            colors = [(1.,0.,0.,.6),
                      (1.,1.,0.,.6),
                      (0.,0.,1.,.6),
                      (0.,0.,0.,.6)]

            for i, line in enumerate(lines):
                Color(colors[i][0], colors[i][1], colors[i][2], colors[i][3])
                Line(points=line, width=5, joint="bevel")


class MapScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MapScreen, self).__init__(**kwargs)
        map_view = MapView(zoom=13, lat=20.5931, lon=-103.3789)
        map_view.add_layer(LineMapLayer())

        self.add_widget(map_view)


class MissionCard(MDCard):
    def __init__(self, **kwargs):
        super(MissionCard, self).__init__(**kwargs)
        self.style = 'filled'
        mission_data = MDBoxLayout(orientation='horizontal', padding=(10, 10))
        progress = MDBoxLayout(orientation='vertical', padding=(10, 10))
        res = requests.get('https://budiserver-h4gt44kccq-uc.a.run.app/getMissions')
        if res.status_code == 200:
            mission_text = res.text.replace('"', '')
            mission_text = mission_text.replace('\\', '')
            mission_text = mission_text.replace('*', '')
            progress.add_widget(MDLabel(text=mission_text))
        progress.add_widget(MDLinearProgressIndicator(
            value=random.randint(25,100),
            size_hint_y=0.4
        ))
        mission_data.add_widget(Image(source='icons/mission.png', size_hint_x=0.45))
        mission_data.add_widget(progress)

        self.add_widget(mission_data)


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