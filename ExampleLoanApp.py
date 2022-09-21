import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.screenmanager import ScreenManager, Screen



class InputScreen(GridLayout):
    def __init__(self, **kwargs):
        super(InputScreen, self).__init__(**kwargs)
        self.cols = 2 #1 label, 1 input. For every 2nd widget we add, the app will go to the next line

        self.add_widget(Label(text='Tuition'))
        self.tuition = TextInput(multiline=False)
        self.add_widget(self.tuition)

        self.add_widget(Label(text='Years of School'))
        self.years = TextInput(multiline=False)
        self.add_widget(self.years)

        self.add_widget(Label(text='Interest Rate'))
        self.interest = TextInput(multiline=False)
        self.add_widget(self.interest)

        button = Button(text='CalculateMonthly Payment',
                        size_hint=(.5, .5),
                        pos_hint={'center_x': .5, 'center_y': .5})
        button.bind(on_press = self.on_press_button)
        self.add_widget(button)

    def on_press_button(self, instance):
        #store variables
        app.tuition = float(self.tuition.text)
        app.years = float(self.years.text)
        app.interest = float(self.interest.text)

        #create and switch to output screen
        output_screen = OutputScreen()
        screen = Screen(name='Output')
        screen.add_widget( output_screen )
        app.screen_manager.add_widget(screen)
        app.screen_manager.current = 'Output'

class OutputScreen(GridLayout):
    def __init__(self, **kwargs):
        super(OutputScreen, self).__init__(**kwargs)
        self.cols = 1

        payment = (app.tuition * app.years) / 10.0 #yearly payment
        payment = payment / 12.0
        payment = (payment * app.interest) + payment
        self.add_widget(Label( text=str(payment) ))        
        

class LoanApp(App):
    def build(self):
        tuition = 0.0
        years = 0.0
        interest = 0.0
        self.screen_manager = ScreenManager()

        self.input_screen = InputScreen()
        screen = Screen(name='Input')
        screen.add_widget( self.input_screen )
        self.screen_manager.add_widget(screen)

        return self.screen_manager


#####################################
if __name__ == "__main__":
    app = LoanApp()
    app.run()




