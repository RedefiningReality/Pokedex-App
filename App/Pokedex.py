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
import os

from kivy.uix.screenmanager import ScreenManager, Screen

from Data import *

LabelBase.register(name='Peepo',
                   fn_regular='Peepo.ttf')

class StartScreen(GridLayout):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.cols = 1 
        self.spacing = (0, 50)

        self.add_widget(Label(text=' ', font_size='40sp', font_name = 'Peepo', halign='center', markup=True))

        titleLabel = Label(text='[color=ff3333]PokeScanner', font_size='40sp', font_name = 'Peepo', halign='center', markup=True)
        self.add_widget(titleLabel)

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
        for filename in os.listdir('Pokemon UI Images'):
            file = os.path.join('Pokemon UI Images', filename)
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
        #Take picture
        print('Opening camera')
    
    def show_statistics(self, instance):
        app.screen_manager.current = 'Output'
        app.screen_manager.transition.direction = 'left'
        app.output_screen.display_pokemon(instance.text)


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
        self.image.source = os.path.join('Pokemon UI Images', name + '.png')
        self.pname.text = name
        pokemonId = int(name[1:4])
        self.description.text = get_description(pokemonId)
        types = get_types(pokemonId)
        self.type.text = get_types_string(types)
        self.strength.text = get_types_string(get_strengths(types))
        self.weakness.text = get_types_string(get_weaknesses(types))
        self.abilities.text = "\n".join(["   " + a for a in get_abilities(pokemonId)])
        stats = get_stats(pokemonId)
        self.hp_label.text = str(stats[0])
        self.hp.value = stats[0] / 180
        self.hp.color_list = get_color_list(self.hp.value)
        self.attack_label.text = str(stats[1])
        self.attack.value = stats[1] / 180
        self.attack.color_list = get_color_list(self.attack.value)
        self.defense_label.text = str(stats[2])
        self.defense.value = stats[2] / 180
        self.defense.color_list = get_color_list(self.defense.value)
        self.sp_attack_label.text = str(stats[3])
        self.sp_attack.value = stats[3] / 180
        self.sp_attack.color_list = get_color_list(self.sp_attack.value)
        self.sp_defense_label.text = str(stats[4])
        self.sp_defense.value = stats[4] / 180
        self.sp_defense.color_list = get_color_list(self.sp_defense.value)
        self.speed_label.text = str(stats[5])
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
        
        self.output_screen = OutputScreen(name='Output')

        self.screen_manager.add_widget(screen)
        self.screen_manager.add_widget(self.output_screen)

        return self.screen_manager


#####################################
if __name__ == "__main__":
    app = PokedexApp()
    app.run()
