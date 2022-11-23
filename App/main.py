import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
import os
import json

from kivy.uix.screenmanager import ScreenManager, Screen


from kivy import platform
if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE, 
Permission.READ_EXTERNAL_STORAGE])


def get_types(pokemonId):
    with open ('json/evolution-chain.json', "r") as f:
        data = json.loads(f.read())
        return [t.capitalize() for t in data[pokemonId - 1]["types"]]

def get_weaknesses(types):
    damage = {}
    with open ('json/types.json', "r") as f:
        data = json.loads(f.read())
        for t in types:
            entry = next(e for e in data if e["name"] == t)
            for v in entry["vulnerablities"]:
                if v in damage:
                    damage[v] = damage[v] * 2
                else:
                    damage[v] = 2
            for r in entry["resistant"]:
                if r in damage:
                    damage[r] = damage[r] * 0.5
                else:
                    damage[r] = 0
            for n in entry["noeffect"]:
                if n in damage:
                    damage[n] = damage[n] * 0
                else:
                    damage[n] = 0
    return [x[0] for x in damage.items() if x[1] >= 2]

def get_strengths(types):
    damage = {}
    with open ('json/types.json', "r") as f:
        data = json.loads(f.read())
        for t in types:
            entry = next(e for e in data if e["name"] == t)
            for s in entry["strengths"]:
                if s in damage:
                    damage[s] = damage[s] * 2
                else:
                    damage[s] = 2
            for w in entry["weaknesses"]:
                if w in damage:
                    damage[w] = damage[w] * 0.5
                else:
                    damage[w] = 0
            for i in entry["immunes"]:
                if i in damage:
                    damage[i] = damage[i] * 0
                else:
                    damage[i] = 0
    return [x[0] for x in damage.items() if x[1] >= 2]

def get_chain(pokemonId):
    froms = []
    tos = []
    with open ('json/evolution-chain.json', "r") as f:
        data = json.loads(f.read())
        pokemon = data[pokemonId - 1]
        prev = pokemon["from"]
        while prev != None:
            froms = [prev] + froms
            prev = data[prev - 1]["from"]
        next = pokemon["to"]
        while next != None:
            tos = tos + [next]
            next = data[next - 1]["to"]
    return froms + [pokemonId] + tos

def get_name(pokemonId):
    with open ('json/evolution-chain.json', "r") as f:
        data = json.loads(f.read())
        return data[pokemonId - 1]["name"]

def get_chain_names(pokemonId):
    return [get_name(x) for x in get_chain(pokemonId)]

def get_types_string(list):
    with open ('json/types.json', "r") as f:
        data = json.loads(f.read())
        tags = ["[color=" + next(c["color"] for c in data if c["name"] == t) + "]" + t + "[/color]" for t in list]
        return "   " + "   ".join(tags)


def get_moveset(pokemonId):
    with open ('json/preferred-moves.json', "r") as preferredFile:
        preferredJson = json.loads(preferredFile.read())
        movesetList = next(l for l in preferredJson if l["id"] == pokemonId)["moveset"]
        if len(movesetList) == 0:
            movesetList = [0, 1, 2, 3]
        with open ('json/' + str(pokemonId) + '.json', "r") as pokemonFile:
            pokemonJson = json.loads(pokemonFile.read())
            movesetNames = []
            for moveIndex in movesetList:
                movesetNames.append(pokemonJson["moves"][int(moveIndex)]["move"]["name"])
            return movesetNames

def get_abilities(pokemonId):
    with open ('json/' + str(pokemonId) + '.json', "r") as pokemonFile:
        pokemonJson = json.loads(pokemonFile.read())
        return [a["ability"]["name"].capitalize() for a in pokemonJson["abilities"]]

#[hp, attack, defense, sp. attack, sp. defense, speed]
def get_stats(pokemonId):
    with open ('json/' + str(pokemonId) + '.json', "r") as pokemonFile:
        pokemonJson = json.loads(pokemonFile.read())
        return [a["base_stat"] for a in pokemonJson["stats"]]

def get_description(pokemonId):
    with open ('json/descriptions.json', "r") as f:
        data = json.loads(f.read())
        return next(d for d in data if d["id"] == pokemonId)["description"]

def get_color_list(value):
    if value > 15 / 18:
        return [0, .65, .62, 1]
    if value > 12 / 18:
        return [.14, .8, .37, 1]
    if value > 9 / 18:
        return [.63, .9, .08, 1]
    if value > 6 / 18:
        return [1, .87, .34, 1]
    if value > 3 / 18:
        return [1, .5, .06, 1]
    return [.95, .27, .27, 1]


class StartScreen(GridLayout):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.cols = 1 
        self.spacing = (0, 50)

        self.add_widget(Label(text=' ', font_size='40sp', font_name = 'Peepo', halign='center', markup=True))
        titleLabel = Label(text='[color=ff3333]PokeScanner', font_size='40sp', font_name = 'Peepo', halign='center', markup=True)
        self.add_widget(titleLabel) #Title of the App
        self.add_widget(Label(text=' ', font_size='40sp', font_name = 'Peepo', halign='center', markup=True))

        instructionsLabel = Label(text='[color=000000]Click below to scan a Pokemon', font_name = 'Peepo', markup=True)
        self.add_widget(instructionsLabel)

        
        button = Button(text='Scan', font_name = 'Peepo',
                        size=(Window.width, 100),
                        size_hint=(1, None),
                        pos_hint={'center_x': 10.0, 'center_y': 50.0},
                        pos=(Window.width,900),
                        background_color=(0, 0, 1, 1))
        button.bind(on_press = self.take_picture)
        self.add_widget(button)
        
            
        subgrid = GridLayout(cols=2, size_hint_y=None)        
        #Create list of pokemon
        files = {}
        for filename in os.listdir('images'):
            file = os.path.join('images', filename)
            files[filename] = file
        #Add image of pokemon in order of filename
        for filename in sorted(files.keys()):
            file = files[filename] #get file path
            subgrid.add_widget( Image(source=file) )
            button = Button(text=str(filename)[:-4], font_name = 'Peepo', background_color = (0.0, 0.7, 0.95, 0.5), color =(0, 0, 0, 1), size = (Window.width, 150), size_hint = (1, None))
            button.bind(on_press=self.show_statistics)
            subgrid.add_widget(button)
        
        subgrid.bind(minimum_height=subgrid.setter('height'))
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(subgrid) 
        self.add_widget(root)



    def take_picture(self, instance):
        app.screen_manager.current = 'Camera'
        app.screen_manager.transition.direction = 'left'
        app.camera_screen.ids['camera'].play = True
        
    
    def show_statistics(self, instance):
        app.screen_manager.current = 'Output'
        app.screen_manager.transition.direction = 'left'
        app.output_screen.display_pokemon(instance.text)



Builder.load_string('''
<CameraScreen>:
    BoxLayout:
        orientation: 'vertical'
        Camera:
            id: camera
            resolution: (640, 480)
            allow_stretch: True
            keep_ratio: True
            play: False
            canvas.before:
                PushMatrix
                Rotate:
                    angle: -90
                    origin: self.center
            canvas.after:
                PopMatrix
        Button:
            text: 'Capture'
            font_name: 'Peepo'
            size_hint_y: None
            height: '48dp'
            background_color: 0, 0, 1, 1
            size: 
            on_press: root.capture()
''')

class CameraScreen(Screen):
    def capture(self, *args):

        cameraObject = self.ids['camera']

        #save image
        cameraObject.export_to_png('pokemonImage.png')
        
        #Close camera
        cameraObject.play = False
        
        #Return to start screen for now
        #Should be changed to output after YOLO runs
        app.screen_manager.current = 'Start'
        app.screen_manager.transition.direction = 'right'

        cameraObject.play = False
        

Builder.load_file('output.kv')
class OutputScreen(Screen):
    image = ObjectProperty(None)
    pname = ObjectProperty(None)
    description = ObjectProperty(None)
    type = ObjectProperty(None)
    strength = ObjectProperty(None)
    weakness = ObjectProperty(None)
    abilities = ObjectProperty(None)
    hp = ObjectProperty(None)
    attack = ObjectProperty(None)
    defense = ObjectProperty(None)
    sp_attack = ObjectProperty(None)
    sp_defense = ObjectProperty(None)
    speed = ObjectProperty(None)
    hp_label = ObjectProperty(None)
    attack_label = ObjectProperty(None)
    defense_label = ObjectProperty(None)
    sp_attack_label = ObjectProperty(None)
    sp_defense_label = ObjectProperty(None)
    speed_label = ObjectProperty(None)
    sp_attack_color = ObjectProperty(None)
    moveset = ObjectProperty(None)
    evolutions = ObjectProperty(None)
    
    def display_pokemon(self, name):
        self.image.source = os.path.join('images', name + '.png')
        self.pname.text = name
        pokemonId = int(name[1:4])
        self.description.text = get_description(pokemonId)
        types = get_types(pokemonId)
        self.type.text = get_types_string(types)
        self.strength.text = get_types_string(get_strengths(types))
        self.weakness.text = get_types_string(get_weaknesses(types))
        self.abilities.text = "\n".join(["   " + a for a in get_abilities(pokemonId)])
        stats = get_stats(pokemonId)
        self.hp_label.text = "HP " + str(stats[0])
        self.hp.value = stats[0] / 180
        self.hp.color_list = get_color_list(self.hp.value)
        self.attack_label.text = "Attack " + str(stats[1])
        self.attack.value = stats[1] / 180
        self.attack.color_list = get_color_list(self.attack.value)
        self.defense_label.text = "Defense " + str(stats[2])
        self.defense.value = stats[2] / 180
        self.defense.color_list = get_color_list(self.defense.value)
        self.sp_attack_label.text = "Sp. Attack " + str(stats[3])
        self.sp_attack.value = stats[3] / 180
        self.sp_attack.color_list = get_color_list(self.sp_attack.value)
        self.sp_defense_label.text = "Sp. Defense " + str(stats[4])
        self.sp_defense.value = stats[4] / 180
        self.sp_defense.color_list = get_color_list(self.sp_defense.value)
        self.speed_label.text = "Speed " + str(stats[5])
        self.speed.value = stats[5] / 180
        self.speed.color_list = get_color_list(self.speed.value)
        self.moveset.text = "\n".join(["   " + m.capitalize() for m in get_moveset(pokemonId)])
        self.evolutions.text = " -> ".join(get_chain_names(pokemonId))
        

class PokedexApp(App):
    def build(self):
        #Set background color
        Window.clearcolor = (0, 0.85, 1, 0)
        
        self.screen_manager = ScreenManager()

        self.start_screen = StartScreen()
        screen = Screen(name='Start')
        screen.add_widget(self.start_screen )
        
        self.camera_screen = CameraScreen(name='Camera')
        self.output_screen = OutputScreen(name='Output')

        self.screen_manager.add_widget(screen)
        self.screen_manager.add_widget(self.camera_screen)
        self.screen_manager.add_widget(self.output_screen)

        return self.screen_manager


#####################################
if __name__ == "__main__":
    app = PokedexApp()
    app.run()