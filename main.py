from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

# 🔥 Splash Screen Class
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Splash Screen Layout
        layout = BoxLayout(orientation='vertical', padding=50, spacing=30)
        
        with layout.canvas.before:
            Color(0.1, 0.1, 0.3, 1)  # Dark Blue Background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # App Logo/Icon
        self.logo = Label(
            text='🎩', 
            font_size='80sp'
        )
        layout.add_widget(self.logo)
        
        # Welcome Message
        self.welcome_label = Label(
            text='[b]MagicTrick[/b]\nမှ ကြိုဆိုပါတယ်!',
            font_size='28sp',
            markup=True,
            color=(1, 1, 1, 1)
        )
        layout.add_widget(self.welcome_label)
        
        # Loading Message
        self.loading_label = Label(
            text='မှော်ဂဏန်းလောကထဲသို့ ဝင်ရောက်နေပါသည်...',
            font_size='16sp',
            color=(0.8, 0.8, 1, 1)
        )
        layout.add_widget(self.loading_label)
        
        self.add_widget(layout)
        
        # Auto navigate to main screen after 3 seconds
        Clock.schedule_once(self.go_to_main, 3)
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    
    def go_to_main(self, dt):
        self.manager.current = 'main'

# 🔥 Main Screen Class
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MainAppLayout())

# 🔥 Main App Layout
class MainAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        # Background
        with self.canvas.before:
            Color(0.25, 0.15, 0.55, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Header
        self.logo = Label(text='🎩', font_size='50sp')
        self.add_widget(self.logo)
        
        self.title_label = Label(
            text='[b]MagicTrick - မှော် ၉ ဂဏန်း[/b]',
            font_size='24sp',
            markup=True,
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.title_label)
        
        # Important Notice
        self.notice = Label(
            text='[color=#FFDD00][b]သတိပြုရန်: 0 (သို့) 9 ချန်ထားပါက 0/9 ဟုပြသမည်[/b][/color]',
            font_size='14sp',
            markup=True,
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.notice)
        
        # Input
        self.input_box = TextInput(
            hint_text='ကျန်ဂဏန်းများ space ခြားထည့်ပါ...',
            multiline=False,
            font_size='18sp',
            size_hint=(1, None),
            height=50,
            background_color=(1, 1, 1, 0.9),
            foreground_color=(0, 0, 0, 1)
        )
        self.add_widget(self.input_box)
        
        # Result
        self.result_label = Label(
            text='', 
            font_size='20sp', 
            markup=True, 
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=80
        )
        self.add_widget(self.result_label)
        
        # Buttons
        self.btn_box = BoxLayout(spacing=10, size_hint=(1, None), height=50)
        
        self.magic_btn = Button(
            text='🔮 မှော်ဂဏန်းရှာမယ်', 
            background_color=(0.6, 0.2, 0.8, 1)
        )
        self.magic_btn.bind(on_press=self.simple_magic)
        self.btn_box.add_widget(self.magic_btn)
        
        self.clear_btn = Button(
            text='🔄 ရှင်းမယ်', 
            background_color=(0.8, 0.4, 0.2, 1)
        )
        self.clear_btn.bind(on_press=self.clear_all)
        self.btn_box.add_widget(self.clear_btn)
        
        self.add_widget(self.btn_box)
        
        # How to use
        self.instructions = Label(
            text='[color=#AAAAFF]အသုံးပြုနည်း:\n၁. သူငယ်ချင်းကိုဂဏန်းရေးခိုင်းပါ\n၂. ၉ နဲ့မြှောက်ခိုင်းပါ\n၃. ဂဏန်းတစ်လုံးချန်ခိုင်းပါ\n၄. ကျန်ဂဏန်းများထည့်ပါ[/color]',
            font_size='13sp',
            markup=True,
            size_hint=(1, None),
            height=100
        )
        self.add_widget(self.instructions)
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    
    def simple_magic(self, instance):
        try:
            digits_text = self.input_box.text.strip()
            if not digits_text:
                self.result_label.text = '[color=#FF5555]ကျေးဇူးပြု၍ ဂဏန်းများထည့်ပါ[/color]'
                return
            
            digits = list(map(int, digits_text.split()))
            
            if len(digits) < 2:
                self.result_label.text = '[color=#FF5555]အနည်းဆုံး ဂဏန်း ၂ လုံးထည့်ပါ[/color]'
                return
            
            # ဝေယံမှော်နည်း
            total = sum(digits)
            
            # Digital Root
            digital_root = total
            while digital_root > 9:
                digital_root = sum(int(d) for d in str(digital_root))
            
            missing = 9 - digital_root
            
            # 0/9 ချွင်းချက်ကိုသတ်မှတ်ခြင်း
            if missing == 0:
                result = "0/9"
                reason = "0 သို့မဟုတ် 9 ချန်ထားနိုင်ပါသည်"
                color = "#FF9900"
            else:
                result = str(missing)
                reason = f"ကျန်ဂဏန်းများပေါင်းလဒ်: {total} → {digital_root}"
                color = "#00FFAA"
            
            self.result_label.text = f'[b][color={color}]မှော်ဂဏန်း: {result}[/color][/b]\n[color=#AAAAFF]{reason}[/color]'
            
        except ValueError:
            self.result_label.text = '[color=#FF5555]ကျေးဇူးပြု၍ ဂဏန်းမှန်မှန်ထည့်ပါ (0-9)[/color]'
    
    def clear_all(self, instance):
        self.input_box.text = ''
        self.result_label.text = ''

# 🔥 Main App Class
class MagicTrickApp(App):
    def build(self):
        self.title = 'MagicTrick - မှော် ၉ ဂဏန်း'
        
        # Screen Manager
        sm = ScreenManager()
        
        # Add Screens
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MainScreen(name='main'))
        
        return sm

if __name__ == '__main__':
    MagicTrickApp().run()