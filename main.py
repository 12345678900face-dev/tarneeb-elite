from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

class TarneebApp(App):
    def build(self):
        self.title = "Tarneeb Elite"
        
        # الحاوية الرئيسية الشاملة
        root = BoxLayout(orientation='vertical', padding=10, spacing=8)
        
        self.totals = [0, 0, 0, 0]
        self.name_inputs = []
        self.score_inputs = []
        self.total_labels = []
        
        # 1. عنوان التطبيق الفخم
        title_label = Label(
            text="[b]✦ TARNEEB ELITE ✦[/b]",
            markup=True,
            font_size=22,
            size_hint_y=None,
            height=38,
            color=(0.95, 0.77, 0.05, 1) # ذهبي
        )
        root.add_widget(title_label)
        
        # 2. رؤوس الأعمدة
        headers_layout = BoxLayout(size_hint_y=None, height=30, spacing=10)
        headers_layout.add_widget(Label(text="Player", bold=True, font_size=16, color=(0.8, 0.8, 0.8, 1)))
        headers_layout.add_widget(Label(text="Score", bold=True, font_size=16, color=(0.95, 0.77, 0.05, 1)))
        headers_layout.add_widget(Label(text="Total", bold=True, font_size=16, color=(0.18, 0.8, 0.44, 1)))
        root.add_widget(headers_layout)
        
        # 3. صفوف اللاعبين الأربعة
        for i in range(4):
            row = BoxLayout(size_hint_y=None, height=48, spacing=10)
            
            # تحديد لون الخط للاعبين (الاول والثالث أحمر، الثاني والرابع أبيض)
            name_color = (1, 0.25, 0.25, 1) if i in [0, 2] else (1, 1, 1, 1)
            
            # خانة الاسم
            n_input = TextInput(
                text=f"Player {i+1}",
                multiline=False,
                halign="center",
                font_size=18,
                foreground_color=name_color,
                background_color=(0.15, 0.17, 0.22, 1),
                cursor_color=(0.95, 0.77, 0.05, 1),
                padding_y=[10, 0]
            )
            self.name_inputs.append(n_input)
            row.add_widget(n_input)
            
            # خانة إدخال النقاط
            s_input = TextInput(
                text="",
                multiline=False,
                input_filter="int",
                halign="center",
                font_size=20,
                foreground_color=(0.95, 0.77, 0.05, 1),
                background_color=(0.15, 0.17, 0.22, 1),
                cursor_color=(0.95, 0.77, 0.05, 1),
                padding_y=[10, 0]
            )
            self.score_inputs.append(s_input)
            row.add_widget(s_input)
            
            # خانة المجموع الكلي
            t_label = Label(
                text="0",
                font_size=20,
                bold=True,
                color=(0.18, 0.8, 0.44, 1)
            )
            self.total_labels.append(t_label)
            row.add_widget(t_label)
            
            root.add_widget(row)
            
        # 4. أزرار التحكم
        btn_add = Button(
            text="ADD ROUND SCORE",
            font_size=16,
            bold=True,
            background_normal='',
            background_color=(0.12, 0.53, 0.9, 1),
            size_hint_y=None,
            height=45
        )
        btn_add.bind(on_press=self.add_score)
        root.add_widget(btn_add)
        
        btn_reset = Button(
            text="RESET GAME",
            font_size=15,
            bold=True,
            background_normal='',
            background_color=(0.85, 0.33, 0.1, 1),
            size_hint_y=None,
            height=38
        )
        btn_reset.bind(on_press=self.reset_game)
        root.add_widget(btn_reset)
        
        # 5. سجل الجولات (مكبر لأقصى حد ومساحة ضخمة)
        history_title = Label(
            text="--- ROUNDS HISTORY ---",
            bold=True,
            font_size=16,
            size_hint_y=None,
            height=30,
            color=(0.95, 0.77, 0.05, 1)
        )
        root.add_widget(history_title)
        
        scroll = ScrollView(size_hint=(1, 1))
        self.history_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=6)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        scroll.add_widget(self.history_layout)
        
        root.add_widget(scroll)
        
        return root

    def add_score(self, instance):
        scores = []
        for i in range(4):
            val = self.score_inputs[i].text
            scores.append(int(val) if val else 0)
            
        if all(s == 0 for s in scores):
            return
            
        winners = []
        for i in range(4):
            self.totals[i] += scores[i]
            self.total_labels[i].text = str(self.totals[i])
            
            if self.totals[i] >= 41:
                name = self.name_inputs[i].text or f"Player {i+1}"
                winners.append(name)
                
        n1 = self.name_inputs[0].text or "P1"
        n2 = self.name_inputs[1].text or "P2"
        n3 = self.name_inputs[2].text or "P3"
        n4 = self.name_inputs[3].text or "P4"
        
        # حجم خط ضخم وكبير جداً داخل السجل لضمان رؤية فائقة الوضوح
        history_text = f"• {n1}: {scores[0]}   |   {n2}: {scores[1]}   |   {n3}: {scores[2]}   |   {n4}: {scores[3]}"
        h_label = Label(
            text=history_text,
            font_size=22,
            bold=True,
            size_hint_y=None,
            height=50,
            color=(0.95, 0.98, 1, 1)
        )
        self.history_layout.add_widget(h_label)
        
        for s_input in self.score_inputs:
            s_input.text = ""
            
        if winners:
            winner_str = " & ".join(winners)
            content = BoxLayout(orientation='vertical', padding=15, spacing=10)
            content.add_widget(Label(
                text=f"[b]👑 CONGRATULATIONS 👑[/b]\n\n[color=f1c40f]{winner_str}[/color]\nWon the game with 41+ points!",
                markup=True,
                font_size=20,
                halign='center'
            ))
            close_btn = Button(
                text="GREAT!",
                font_size=18,
                bold=True,
                background_normal='',
                background_color=(0.18, 0.8, 0.44, 1),
                size_hint_y=None,
                height=50
            )
            content.add_widget(close_btn)
            
            popup = Popup(
                title='',
                separator_height=0,
                content=content,
                size_hint=(0.85, 0.38)
            )
            close_btn.bind(on_press=popup.dismiss)
            popup.open()

    def reset_game(self, instance):
        self.totals = [0, 0, 0, 0]
        for i in range(4):
            self.total_labels[i].text = "0"
            self.score_inputs[i].text = ""
        self.history_layout.clear_widgets()

if __name__ == '__main__':
    TarneebApp().run()

