import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
import os

from kivy.uix.screenmanager import ScreenManager, Screen


class StartScreen(GridLayout):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.cols = 1 
        self.spacing = (0, 10)

        titleLabel = Label(text='[color=ff3333][b]Pokedex[/b]', font_size='40sp', halign='center', underline=True, markup=True)
        self.add_widget(titleLabel)

            
        subgrid = GridLayout(cols=2, size_hint_y=None)        
        #Create list of pokemon
        for filename in os.listdir('Pokemon UI Images'):
            file = os.path.join('Pokemon UI Images', filename)
            subgrid.add_widget( Image(source=file) )
            button = Button(text=str(filename)[:-4], background_color = (0.0, 0.7, 0.95, 0.5), color =(0, 0, 0, 1), size = (Window.width, 150), size_hint = (1, None))
            button.bind(on_press=self.show_statistics)
            subgrid.add_widget(button)
        
        subgrid.bind(minimum_height=subgrid.setter('height'))
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(subgrid) 
        self.add_widget(root)


        instructionsLabel = Label(text='[color=000000]Click below to scan a Pokemon', markup=True)
        self.add_widget(instructionsLabel)

        
        button = Button(text='Scan',
                        size_hint=(.5, .9),
                        pos_hint={'center_x': .5, 'center_y': .5},
                        background_color=(0, 0, 1, 1))
        button.bind(on_press = self.take_picture)
        self.add_widget(button)

    def take_picture(self, instance):
        #Take picture
        print('Opening camera')
    
    def show_statistics(self, instance):
        print('statistics')

class OutputScreen(GridLayout):
    def __init__(self, **kwargs):
        super(OutputScreen, self).__init__(**kwargs)
        self.cols = 1
        #Show statistics        
        

class PokedexApp(App):
    def build(self):
        #Set background color
        Window.clearcolor = (0, 0.85, 1, 0)
        
        self.screen_manager = ScreenManager()

        self.start_screen = StartScreen()
        screen = Screen(name='Start')
        screen.add_widget( self.start_screen )
        self.screen_manager.add_widget(screen)

        return self.screen_manager


#####################################
if __name__ == "__main__":
    app = PokedexApp()
    app.run()




