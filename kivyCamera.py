from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (1000, 480)
        allow_strech: True
        play: True
    #ToggleButton:
    #    text: 'Play'
    #    on_press: camera.play = not camera.play
    #    size_hint_y: None
    #    height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: '40dp'
        height: '96dp'
        on_press: root.capture()
''')

class CameraClick(BoxLayout):
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


class TestCamera(App):
    def build(self):
        return CameraClick()

TestCamera().run()