import sqlite3
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.core.window import Window
from kivy.effects.scroll import ScrollEffect
from kivy.metrics import dp


class ResultItem(RecycleDataViewBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super(ResultItem, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(70)
        self.padding = [dp(10), dp(5)]
        self.orientation = 'vertical'

    def update_view(self, data):
        self.code = data['code']
        self.name = data['name']
        
        self.clear_widgets()
        title = Label(text=f"[b]{self.code}[/b]", markup=True, size_hint_y=None, height=dp(35), text_size=(self.width, None), color=(0, 0, 1, 1))
        desc = Label(text=self.name, size_hint_y=None, height=dp(35), text_size=(self.width, None), color=(0, 0, 0, 1))
        
        self.add_widget(title)
        self.add_widget(desc)


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.viewclass = ResultItem
        self.data = []
        self.effect_cls = ScrollEffect


class HSApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 默认路径为APP所在的当前目录，方便你把db文件放在和APK同级位置
        self.db_path = "hs_code.db" 

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        self.text_input = TextInput(hint_text='输入商品名称（如：猪肉）', multiline=False, size_hint_y=None, height=dp(50))
        search_button = Button(text='搜索', size_hint_y=None, height=dp(50), background_color=(0.2, 0.6, 0.2, 1))
        search_button.bind(on_press=self.search)
        
        self.rv = RV()
        
        layout.add_widget(self.text_input)
        layout.add_widget(search_button)
        layout.add_widget(self.rv)
        
        return layout

    def search(self, *args):
        keyword = self.text_input.text.strip()
        
        if not keyword:
            return

        if not os.path.exists(self.db_path):
            self.rv.data = [{"code": "错误", "name": f"找不到数据库文件: {self.db_path}"}]
            self.rv.refresh_from_data()
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        sql = "SELECT 商品编码, 商品名称 FROM hs_codes WHERE 商品名称 LIKE ? LIMIT 50"
        params = (f'%{keyword}%',)
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()

        results = []
        for row in rows:
            results.append({"code": row[0], "name": row[1]})
        
        self.rv.data = results
        self.rv.refresh_from_data()


if __name__ == '__main__':
    HSApp().run()
