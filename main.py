from kivy.app import App

from kivy.uix.widget import Widget

from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import ScreenManager, Screen

from random import randint

class ScreenMan(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_screen = BoxLayoutExample.name

class MythicApp(App):
    pass

class MainWidget(Widget):
    pass

class BoxLayoutExample(BoxLayout, Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.difficulties = ["impossible", "nearly impossible", "very unlikely", "unlikely", "likely", "very likely", "nearly certain", "certain"]

        self.roll_odds_30 = [[i for i in range(0, 2)], [i for i in range(2, 6)], [i for i in range(6, 11)], [i for i in range(11, 16)], [i for i in range(16, 21)], [i for i in range(21, 26)], [i for i in range(26, 30)], [i for i in range(30, 100)]]

        self.chaos_modifier = {"impossible":[
            [0, 1, 81], 
            [0, 1, 81], 
            [0, 1, 81], 
            [1, 5, 82], 
            [2, 10, 83], 
            [3, 15, 84], 
            [5, 25, 86],
            [7, 35, 88],
            [10, 50, 91]], 
            "nearly impossible":[
            [0, 1, 81],
            [0, 1, 81],
            [1, 5, 82],
            [2, 10, 83],
            [3, 15, 84],
            [5, 25, 86],
            [7, 35, 88],
            [10, 50, 91],
            [13, 65, 94]],
            "very unlikely":[
            [0, 1, 81],
            [1, 5, 82],
            [2, 10, 83],
            [3, 15, 84],
            [5, 25, 86],
            [7, 35, 88],
            [10, 50, 91],
            [13, 65, 94],
            [15, 75, 96],
            [17, 85, 98]
            ],
            "unlikely":[
            [1, 5, 82],
            [2, 10, 83],
            [3, 15, 84],
            [5, 25, 86],
            [7, 35, 88],
            [10, 50, 91],
            [13, 65, 94],
            [15, 75, 96],
            [17, 85, 98]
            ],
            "50/50":[
            [2, 10, 83],
            [3, 15, 84],
            [5, 25, 86],
            [7, 35, 88],
            [10, 50, 91],
            [13, 65, 94],
            [15, 75, 96],
            [17, 85, 98],
            [18, 90, 99]
            ],
            "likely":[
            [3, 15, 84],
            [5, 25, 86],
            [7, 35, 88],
            [10, 50, 91],
            [13, 65, 94],
            [15, 75, 96],
            [17, 85, 98],
            [18, 90, 99],
            [19, 95, 100]
            ],
            "very likely":[
            [5, 25, 86],
            [7, 35, 88],
            [10, 50, 91],
            [13, 65, 94],
            [15, 75, 96],
            [17, 85, 98],
            [18, 90, 99],
            [19, 95, 101],
            [20, 99, 101] 
            ],
            "nearly certain":[
            [7, 35, 88],
            [10, 50, 91],
            [13, 65, 94],
            [15, 75, 96],
            [17, 85, 98],
            [18, 90, 99],
            [19, 95, 100],
            [20, 99, 101],
            [20, 99, 101]
            ],
            "certain":[
            [10, 50, 91],
            [13, 65, 94],
            [15, 75, 96],
            [17, 85, 98],
            [18, 90, 99],
            [19, 95, 100],
            [20, 99, 101],
            [20, 99, 101],
            [20, 99, 101]
            ]}
        
        self.random_events_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44, 55, 66, 77, 88, 99]

        self.current_diff = ""
    
    def determine_diff(self, skill, dice = 30):
        odds = self.roll_odds_30
        roll = randint(1, dice)
        roll += int(skill)

        for i in range(len(odds)):
            if roll in odds[i]:
                self.current_diff = self.difficulties[i]
                
                print(self.difficulties[i])
                print("Succes in diff!")
                print(f"{roll} diff roll")

                self.ids.result_text.text = "Diff is determined, roll for question"
                return None
        
        print("Some mistake when determening diff")
    
    def check_ranges(self, start, end, roll):
        ranges = [i for i in range(start, end)]

        return roll in ranges
    
    def determine_answer(self):
        chaos_factor = self.ids.chaos_slider.value
        
        roll = randint(1, 100)
        answer = ""

        random_event_text = "Some random event occured!"

        if roll in self.random_events_nums and int(str(roll)[0]) <= chaos_factor:
            print("Random event")

            if roll % 2 == 0:
                answer += random_event_text + "Interrupted scene." + ' '            
            else:
                answer += random_event_text + "Altered scene" + ' '

        chaos = self.chaos_modifier[self.current_diff][chaos_factor - 1]
        
        
        if self.check_ranges(0, chaos[0], roll):
           answer += "Exceptional yes" 
        
        elif self.check_ranges(chaos[0], chaos[1], roll):
            answer += "Yes"
        
        elif self.check_ranges(chaos[1], chaos[2], roll):
            answer += "No"
        
        elif self.check_ranges(chaos[2], 200, roll):
            answer += "Exceptional no"
        else:
            answer = "Some mistake"
        
        print(f"{chaos} chaos odds")
        print(f"{roll} chaos roll")
        self.ids.result_text.text = answer
    
    def get_user_diff(self):
        input = self.ids.skill_roll.text

        if input in self.difficulties:
            self.current_diff = self.ids.skill_roll.text
            self.ids.result_text.text = "Diff is set, roll for answer"
        else:
            self.ids.result_text.text = f"Wrong input, you need to write something out of this {self.difficulties}" 
    
    def new_scene_chaos_roll(self):
        chaos_factor = self.ids.chaos_slider.value

        roll = randint(1, 10)

        if roll <= chaos_factor:
            if roll % 2 == 0:
                self.ids.result_text.text = "Random Event! Interupted scene"
            else:
                self.ids.result_text.text = "Random Event! Altered scene"
        else:
            self.ids.result_text.text= "No random events"

MythicApp().run()
