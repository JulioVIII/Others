from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.graphics import Color, Rectangle
import os
from kivy.utils import platform

# --- Mobile-like screen size for desktop testing ---
if platform in ("win","linux", "macosx"):
    Window.size = (360, 640)
    Window.clearcolor = (0, 0, 0, 1)

class StoryPage(Screen):
    image_source = StringProperty('')
    story_text = StringProperty('')

    def __init__(self, image_source='', story_text='', **kwargs):
        super().__init__(**kwargs)
        self.image_source = image_source
        self.story_text = story_text

        root = BoxLayout(orientation='vertical', padding=8, spacing=6)

        # --- Image at the top ---
        if image_source:
            img_box = BoxLayout(size_hint_y=0.6)
            if os.path.isfile(image_source):
                img = Image(source=image_source, allow_stretch=True, keep_ratio=True)
                img_box.add_widget(img)
            else:
                img_box.add_widget(Label(text=f"[Image not found]\n{image_source}", halign='center', valign='middle', markup=True))
            root.add_widget(img_box)
        else:
            root.add_widget(BoxLayout(size_hint_y=0.02))

        # --- Centered text with black background ---
        txt_box = BoxLayout(size_hint_y=0.35)
        with txt_box.canvas.before:
            Color(0, 0, 0, 1)  # black background
            self._rect = Rectangle(pos=txt_box.pos, size=txt_box.size)
        txt_box.bind(pos=lambda inst, val: setattr(self._rect, 'pos', txt_box.pos),
                     size=lambda inst, val: setattr(self._rect, 'size', txt_box.size))

        if self.story_text:
            float_layout = FloatLayout(size_hint=(1,1))
            lbl = Label(
                text=self.story_text,
                markup=True,
                font_size='20sp',
                halign='center',
                valign='middle',
                size_hint=(0.95,0.95),
                pos_hint={'center_x':0.5,'center_y':0.5},
                text_size=(Window.width*0.95, None)
            )
            lbl.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
            float_layout.add_widget(lbl)
            txt_box.add_widget(float_layout)

        root.add_widget(txt_box)

        # --- Bottom bar with navigation buttons ---
        bar = BoxLayout(size_hint_y=0.05, spacing=6)
        self.prev_btn = Button(text='◀ Previous', size_hint_x=0.3)
        self.page_label = Label(text='', halign='center', valign='middle')
        self.next_btn = Button(text='Next ▶', size_hint_x=0.3)
        bar.add_widget(self.prev_btn)
        bar.add_widget(self.page_label)
        bar.add_widget(self.next_btn)
        root.add_widget(bar)

        # Bind button events
        self.prev_btn.bind(on_release=self._on_prev_pressed)
        self.next_btn.bind(on_release=self._on_next_pressed)

        self.add_widget(root)

    def on_pre_enter(self):
        sm = self.manager
        if not sm:
            return
        names = [s.name for s in sm.screens]
        i = names.index(self.name)
        self.page_label.text = f"Page {i+1} of {len(names)}"
        self.prev_btn.disabled = (i == 0)
        self.next_btn.disabled = (i == len(names) - 1)

    def _on_next_pressed(self, *args):
        sm = self.manager
        if sm:
            names = [s.name for s in sm.screens]
            i = names.index(sm.current)
            if i + 1 < len(names):
                sm.transition.direction = 'left'
                sm.current = names[i + 1]

    def _on_prev_pressed(self, *args):
        sm = self.manager
        if sm:
            names = [s.name for s in sm.screens]
            i = names.index(sm.current)
            if i - 1 >= 0:
                sm.transition.direction = 'right'
                sm.current = names[i - 1]

    def on_touch_down(self, touch):
        w = Window.width
        x = touch.pos[0]
        sm = self.manager
        if sm:
            names = [s.name for s in sm.screens]
            i = names.index(sm.current)
            if x > w * 0.6 and i + 1 < len(names):
                sm.transition.direction = 'left'
                sm.current = names[i + 1]
                return True
            elif x < w * 0.4 and i - 1 >= 0:
                sm.transition.direction = 'right'
                sm.current = names[i - 1]
                return True
        return super().on_touch_down(touch)

class MyScreenManager(ScreenManager):
    def next(self):
        names = [s.name for s in self.screens]
        i = names.index(self.current)
        if i + 1 < len(names):
            return names[i + 1]
        return names[i]
    def previous(self):
        names = [s.name for s in self.screens]
        i = names.index(self.current)
        if i - 1 >= 0:
            return names[i - 1]
        return names[i]

class StoryApp(App):
    def build(self):
        sm = MyScreenManager(transition=SlideTransition())
        sequence = [
            {"image": "1.jpeg", "text": ""},
            {"image": "", "text": "Ella was a forest dwarf elf, daughter of Queen Zoiryt. She needed to find her way home after getting lost in the dense, whispering woods. Yet, the castle of the kingdom was still nearby, a beacon through the trees."},
            {"image": "2.jpeg", "text": ""},
            {"image": "", "text": "Guided by three brave elves of the realm, Ella ventured forward. Lyran, the master archer, could see through the darkest shadows. Thalen, the path guardian, knew every root and stone of the forest. Sira, the light sorceress, illuminated even the most twisted trails with her magic."},
            {"image": "3.jpeg", "text": ""},
            {"image": "", "text": "Along their journey, they faced great challenges, like the towering beast of the northern cliffs. Its roar shook the trees, and its eyes glowed like molten gold. Together, the group had to find courage and cleverness to pass safely. Every step brought Ella closer to home, but also deeper into the mysteries of the kingdom. Whispers of old magic and hidden secrets lingered in the wind. The castle’s walls promised safety, yet hinted at adventures still untold.[i]The End.[/i]"}
        ]
        
        for idx, item in enumerate(sequence):
            name = f"page{idx+1}"
            s = StoryPage(name=name, image_source=item.get("image",""), story_text=item.get("text",""))
            sm.add_widget(s)

        if sm.screens:
            sm.current = sm.screens[0].name

        # Keyboard navigation
        def on_key(window, key, scancode, codepoint, modifiers):
            names = [s.name for s in sm.screens]
            i = names.index(sm.current)
            if key in (275, ord('d')) and i + 1 < len(names):
                sm.transition.direction = 'left'
                sm.current = names[i + 1]
            if key in (276, ord('a')) and i - 1 >= 0:
                sm.transition.direction = 'right'
                sm.current = names[i - 1]

        Window.bind(on_key_down=on_key)
        return sm

if __name__ == "__main__":
    StoryApp().run()
