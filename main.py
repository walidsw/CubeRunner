from kivy.app import App 
from kivy.uix.widget import Widget 
from random import randint 
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import time


wallmovespeed = 5
birdmovespeed = 5
ff_score = 0

class DemonWall(Widget):
    v = NumericProperty(1)

    def move_wall(self,player):

        global wallmovespeed
        global birdmovespeed
        global ff_score

        if self.pos[0]+52<self.parent.x:
            #When ball goes to the left completely


            #Generating Wall of random size in random distances
            a = randint(1,40)
            b = randint(1,150)
            self.size[0] = 20 + a
            self.size[1] = 50 + b
            self.pos[0] = self.parent.x + self.parent.width + 50+randint(1,600)
            ff_score += self.v

            #Speed Conrtrolling
            if ff_score>=15:
                wallmovespeed *= 1.001
                birdmovespeed *= 1.001
            elif ff_score>=10:
                wallmovespeed *= 1.1
                birdmovespeed *= 1.1
            elif ff_score>=5:
                wallmovespeed *= 1.1
                birdmovespeed *= 1.1

            
        if self.collide_widget(player):
            #Game Over Condition ------GAME OVER-----
            ff_score = -1
            wallmovespeed = 0
            birdmovespeed = 0

        self.pos[0] = self.pos[0] - wallmovespeed
        return ff_score

    




class Bird(Widget):

    def move_uw(self):
        global birdmovespeed
        self.pos[1] = self.pos[1] + birdmovespeed

        #260 wall max height
        if (self.pos[1]>=400): #give it 400
            birdmovespeed*=-1
        if (self.pos[1]<=100):
            birdmovespeed*=-1
            self.pos[1]=100
            return 1
        return 0
        
        


class FlappyBirdGame(Widget):

    def __init__(self, **kwargs):
        super(FlappyBirdGame, self).__init__(**kwargs)

        #load sound
        self.sound1 = SoundLoader.load('sound/gameover_sound.mp3')
        self.jump_sound = SoundLoader.load('sound/jump_sound.mp3')
        self.update_event = None 
        self.is_game_over = False
        self.popup = None

    fwall = ObjectProperty(None)
    player= ObjectProperty(None)
    jump_flag = NumericProperty(0)
    score = NumericProperty(0)
    prev = NumericProperty(0)
    flag_sound1 = NumericProperty(1)


    def start_game(self):
        self.update_event = Clock.schedule_interval(self.update, 1.0/60.0)

    
    def update(self,dt):

        if self.is_game_over:
            self.stop_game()
        else:
            self.score = self.fwall.move_wall(self.player)
            
            if self.jump_flag:
                ret = self.player.move_uw()
                if ret == 1:
                    self.jump_flag = 0
                    
            if self.score!=-1:
                self.prev = self.score
                sc = str(self.score)
                self.ids._pt.text = sc
            else:
                prev = str(self.prev)
                self.ids._pt.text = prev
                self.ids._gameover.text = "Game Over"
                #Now Play Game Over Sound
                self.play_gameover()
                self.is_game_over = True

            


    def on_touch_down(self, touch):
        if self.is_game_over==False:
            self.jump_flag = 1
            if self.jump_sound:
                self.jump_sound.play()
        
    def play_gameover(self):
        if self.flag_sound1:
            if self.sound1:
                self.sound1.play()
                
    def stop_game(self):
        if self.update_event:
            self.update_event.cancel()
            time.sleep(3)
            self.replay_function()
        

    
    def replay_function(self):
        
        cont = BoxLayout(orientation='vertical',padding=10,spacing=10)
        lb = Label(text="Play Again?",font_size=20)

        cont2 = BoxLayout(orientation='horizontal',padding=10,spacing=10)
        bt1 = Button(text="YES", font_size=15)
        bt2 = Button(text="NO",font_size=15)
        
        bt1.bind(on_press=self.yes_button_press)
        bt2.bind(on_press=self.no_button_press)
        
        cont2.add_widget(bt1)
        cont2.add_widget(bt2)

        cont.add_widget(lb)
        cont.add_widget(cont2)

        self.popup = Popup(title='MESSAGE',content=cont, size_hint=(0.8,0.4), auto_dismiss=False)
        self.popup.open()
    
    def yes_button_press(self,dt):
        global wallmovespeed
        global birdmovespeed
        global ff_score

        if self.popup:
            self.popup.dismiss()

        #######################################
        #Renew all
        self.ids._gameover.text = ""
        wallmovespeed = 5
        birdmovespeed = 5
        self.update_event = None 
        self.is_game_over = False
        self.popup = None
        ff_score = 0
        self.jump_flag = 0

        self.score = 0
        sc = str(self.score)
        self.ids._pt.text = sc

        #position initial player and wall
      

        self.player.size = (50,50)
        self.player.pos = (0,100)
        self.player.center_x = (self.parent.width/3)

        self.fwall.size = (20, 50)
        self.fwall.pos = (0, 110)
        self.fwall.center_x = (self.parent.width+300)


        self.start_game()



    def no_button_press(self,dt):
        if self.popup:
            self.popup.dismiss()
        App.get_running_app().stop()

        
        

    
        


class GameApp(App):
    def build(self):
        game = FlappyBirdGame()
        game.start_game()
        return game 

if __name__=='__main__':
    GameApp().run()








