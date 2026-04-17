# SEO发布工具 - Android完整版

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.clock import Clock
from kivy.properties import BooleanProperty
from kivy.graphics import Color, Rectangle
import json
import os
import threading
from datetime import datetime

SITES_FILE = "sites.json"

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # Logo区域
        logo = Label(text='🐾 SEO发布工具', font_size='32sp', size_hint_y=None, height=80)
        layout.add_widget(logo)
        
        # 开始按钮
        btn = Button(text='开始使用 →', size_hint_y=None, height=60, background_color=[0.2, 0.6, 0.8, 1])
        btn.bind(on_press=self.go_main)
        layout.add_widget(btn)
        
        self.add_widget(layout)
    
    def go_main(self, *args):
        self.manager.current = 'main'

class SiteEditPopup(Popup):
    def __init__(self, site, callback, **kwargs):
        super().__init__(**kwargs)
        self.site = site or {}
        self.callback = callback
        self.title = '添加站点' if not site else '编辑站点'
        self.size_hint = (0.9, 0.9)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 站点名称
        layout.add_widget(Label(text='站点名称', size_hint_y=None, height=30))
        self.name_input = TextInput(text=self.site.get('name', ''), multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.name_input)
        
        # GitHub Token
        layout.add_widget(Label(text='GitHub Token', size_hint_y=None, height=30))
        self.token_input = TextInput(text=self.site.get('token', ''), multiline=False, size_hint_y=None, height=40, password=True)
        layout.add_widget(self.token_input)
        
        # GitHub仓库
        layout.add_widget(Label(text='GitHub仓库 (user/repo)', size_hint_y=None, height=30))
        self.repo_input = TextInput(text=self.site.get('repo', ''), multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.repo_input)
        
        # 类目
        layout.add_widget(Label(text='类目 (如: 柯基犬)', size_hint_y=None, height=30))
        self.category_input = TextInput(text=self.site.get('category', ''), multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.category_input)
        
        # 折淘客配置
        layout.add_widget(Label(text='折淘客SID', size_hint_y=None, height=30))
        self.sid_input = TextInput(text=self.site.get('sid', ''), multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.sid_input)
        
        # 按钮
        btn_box = BoxLayout(size_hint_y=None, height=50)
        save_btn = Button(text='保存', background_color=[0.2, 0.7, 0.3, 1])
        save_btn.bind(on_press=self.save)
        cancel_btn = Button(text='取消', background_color=[0.7, 0.3, 0.3, 1])
        cancel_btn.bind(on_press=self.dismiss)
        btn_box.add_widget(save_btn)
        btn_box.add_widget(cancel_btn)
        layout.add_widget(btn_box)
        
        self.content = layout
    
    def save(self, *args):
        data = {
            'name': self.name_input.text.strip(),
            'token': self.token_input.text.strip(),
            'repo': self.repo_input.text.strip(),
            'category': self.category_input.text.strip(),
            'sid': self.sid_input.text.strip(),
            'auto_publish': self.site.get('auto_publish', False),
            'publish_times': self.site.get('publish_times', ['09:00', '14:00', '20:00']),
        }
        self.callback(data)
        self.dismiss()

class MainScreen(Screen):
    auto_enabled = BooleanProperty(False)
    
    def on_enter(self):
        self.load_sites()
        self.setup_auto_check()
    
    def load_sites(self):
        if os.path.exists(SITES_FILE):
            try:
                with open(SITES_FILE, 'r', encoding='utf-8') as f:
                    self.sites = json.load(f)
            except:
                self.sites = []
        else:
            self.sites = []
        
        self.site_names = [s['name'] for s in self.sites] if self.sites else ['请添加站点']
        self.ids.site_spinner.values = self.site_names
        if self.site_names and self.site_names[0] != '请添加站点':
            self.ids.site_spinner.text = self.site_names[0]
            self.on_site_selected()
    
    def setup_auto_check(self):
        if hasattr(self, 'current_site'):
            self.ids.auto_switch.active = self.current_site.get('auto_publish', False)
    
    def on_site_selected(self, *args):
        for site in self.sites:
            if site['name'] == self.ids.site_spinner.text:
                self.current_site = site
                self.ids.category_label.text = f"类目: {site.get('category', '未设置')}"
                self.ids.auto_switch.active = site.get('auto_publish', False)
                break
    
    def add_site(self):
        popup = SiteEditPopup(None, self.on_site_saved)
        popup.open()
    
    def edit_site(self):
        if hasattr(self, 'current_site'):
            popup = SiteEditPopup(self.current_site, self.on_site_saved)
            popup.open()
    
    def on_site_saved(self, data):
        # 检查是否已存在
        for i, s in enumerate(self.sites):
            if s['name'] == data['name']:
                self.sites[i] = data
                break
        else:
            self.sites.append(data)
        
        self.save_sites()
        self.load_sites()
        self.log(f"站点 '{data['name']}' 已保存")
    
    def save_sites(self):
        with open(SITES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.sites, f, ensure_ascii=False, indent=2)
    
    def toggle_auto(self, active):
        if hasattr(self, 'current_site'):
            self.current_site['auto_publish'] = active
            self.save_sites()
            self.log(f"自动发布: {'开启' if active else '关闭'}")
    
    def publish(self):
        if not hasattr(self, 'current_site'):
            self.log("请先添加站点")
            return
        
        self.ids.publish_btn.disabled = True
        self.ids.status_label.text = "发布中..."
        self.log("开始发布...")
        
        threading.Thread(target=self.do_publish, daemon=True).start()
    
    def do_publish(self):
        try:
            from config import config
            config.set_config({
                'category': self.current_site.get('category', ''),
                'keyword': self.current_site.get('category', '') + '用品推荐',
                'repo': self.current_site.get('repo', ''),
                'token': self.current_site.get('token', ''),
                'sid': self.current_site.get('sid', ''),
            })
            
            import index as index_module
            
            def log_callback(msg):
                Clock.schedule_once(lambda dt: self.log(msg))
            
            index_module.log_callback = log_callback
            result = index_module.main_handler({}, {})
            
            Clock.schedule_once(lambda dt: self.on_publish_done(result))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.log(f"错误: {str(e)[:50]}"))
            Clock.schedule_once(lambda dt: self.on_publish_done(None))
    
    def on_publish_done(self, result):
        self.ids.publish_btn.disabled = False
        if result and result.get('success'):
            self.ids.status_label.text = "发布成功"
            self.log(f"✅ 发布成功!")
        else:
            self.ids.status_label.text = "发布失败"
            self.log(f"❌ 发布失败")
    
    def log(self, msg):
        current = self.ids.log_label.text
        timestamp = datetime.now().strftime('%H:%M:%S')
        new_log = f"[{timestamp}] {msg}\n{current}"[:2000]
        self.ids.log_label.text = new_log

class SEOApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    SEOApp().run()
