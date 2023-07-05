from Tkinter_template.Assets.project_management import create_menu, new_window, making_widget
from Tkinter_template.Assets.universal import parse_json_to_property
from Tkinter_template.Assets.default_menu import background_color
from Tkinter_template.Assets.extend_widget import EffectButton
from Tkinter_template.Assets.default_dashboard import *
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get
from Tkinter_template.base import Interface
from Tkinter_template.Assets.music import Music
from modules.calculate import cal
from modules.log import log


class Main(Interface):
    def __init__(self, title: str, icon=None, default_menu=True):
        super().__init__(title, icon, default_menu)
        self.__initialize()

    def __initialize(self):
        # build music object
        self.Musics = Music()
        self.Musics.set_volume(0.75)
        # read attribute
        parse_json_to_property(self, 'modules\\initial.json')
        # build canvas
        self.__depict_canvas()
        # build scales and buttons
        self.__build_var()
        # customize menu bar
        self.__build_menu()
        # advenced music
        self.Musicplayers = MusicPlayer(self.dashboard, self.Musics)

    def __depict_canvas(self):
        def click_event(position):
            def switch_state(number):
                if self.canvas.itemcget(f'wall{number}', 'state') == 'hidden':
                    self.canvas.itemconfig(f'wall{number}', state='normal')
                else:
                    self.canvas.itemconfig(f'wall{number}', state='hidden')

            x_segment = int((self.canvas_side[0]-20)/3)
            y_segment = int((self.canvas_side[1]-20)/3)
            sensitivity = 15
            if 10 + x_segment - sensitivity < position.x < 10 + x_segment + sensitivity:
                for i in range(3):
                    if 10+y_segment*i < position.y < 10+y_segment*(i+1):
                        switch_state(modify[i+1])
                        return

            if 10 + x_segment*2 - sensitivity < position.x < 10 + x_segment*2 + sensitivity:
                for i in range(3):
                    if 10+y_segment*i < position.y < 10+y_segment*(i+1):
                        switch_state(modify[i+4])
                        return

            if 10 + y_segment - sensitivity < position.y < 10 + y_segment + sensitivity:
                for i in range(3):
                    if 10+x_segment*i < position.x < 10+x_segment*(i+1):
                        switch_state(modify[i+7])
                        return

            if 10 + y_segment*2 - sensitivity < position.y < 10 + y_segment*2 + sensitivity:
                for i in range(3):
                    if 10+x_segment*i < position.x < 10+x_segment*(i+1):
                        switch_state(modify[i+10])
                        return

        self.canvas.create_rectangle(
            10, 10, self.canvas_side[0]-10, self.canvas_side[1]-10, width=3)
        self.canvas.bind('<Button-1>', click_event)

        # room number
        number = 1
        for y in range(int(10+(self.canvas_side[1]-20)/6), self.canvas_side[1]-10, int((self.canvas_side[1]-20)/3)):
            for x in range(int(10+(self.canvas_side[0]-20)/6), self.canvas_side[0]-10, int((self.canvas_side[0]-20)/3))[::-1]:
                self.canvas.create_text(x, y, text=f'{number} area', font=font_get(24),
                                        tags=('area' + str(number)))
                number += 1
        # room number

        modify = {1: 2, 2: 4, 3: 6, 4: 1, 5: 3, 6: 5,
                  7: 9, 8: 8, 9: 7, 10: 12, 11: 11, 12: 10}
        # wall vertical
        number = 1
        for x in range(1, 3):
            for y in range(3):
                self.canvas.create_line(
                    10+int((self.canvas_side[0]-20)/3)*x, 10+int((self.canvas_side[1]-20)/3) *
                    y, 10+int((self.canvas_side[0]-20)/3)*x,
                    10+int((self.canvas_side[1]-20)/3)*(y+1), width=3, tags=(f'wall{modify[number]}'), fill='white', state='normal'
                )
                number += 1
        # wall vertical

        # wall horizontal
        for y in range(1, 3):
            for x in range(3):
                self.canvas.create_line(
                    10+int((self.canvas_side[0]-20)/3)*x, 10+int((self.canvas_side[1]-20)/3) *
                    y, 10+int((self.canvas_side[0]-20)/3)*(x+1),
                    10+int((self.canvas_side[1]-20)/3)*y, width=3, tags=(f'wall{modify[number]}'), fill='white', state='normal'
                )
                number += 1
        # wall horizontal

    def __build_var(self):
        def incense():

            base = (10+int((self.canvas_side[0]-20)/3)*2, 10)
            column_num = int(int((self.canvas_side[0]-20)/3) // 30)
            if self.incenseNumber.get() == 4 * column_num:
                return
            self.canvas.create_image(
                10+int((self.canvas_side[0]-20)/3)*2 +
                30*(self.incenseNumber.get() % column_num),
                10 + 70*(self.incenseNumber.get()//column_num),
                anchor='nw', image=tk_image('incense.png', 80, 80), tags=('incense'))
            self.incenseNumber.set(self.incenseNumber.get()+1)

        def air_cleaner():
            self.canvas.delete('ac')
            self.acLocation.set(self.acLocation.get() +
                                (-8 if self.acLocation.get() == 9 else 1))

            temp_change = {0: 0, 1: 2, 2: 1}
            x = 10+int((self.canvas_side[0]-20)/3) * \
                (temp_change[self.acLocation.get() % 3])
            y = 10+int((self.canvas_side[1]-20)/3) * \
                ((self.acLocation.get()-1)//3+1)

            self.canvas.create_image(
                x, y, image=tk_image('ex.png', 100), anchor='sw', tags=('ac'))
        self.__ini_ac = air_cleaner

        self.cadr_scale = making_widget('Scale')(self.dashboard, orient='horizontal', font=font_get(14), label='CADR Value',
                                                 length=self.dashboard_side[0]-5, variable=self.cadrValue,
                                                 from_=1, to=2001, tickinterval=500, bg='#ff6b87',
                                                 showvalue=1, relief='solid')
        self.cadr_scale.grid()

        self.room_side_scale = making_widget('Scale')(self.dashboard, orient='horizontal', font=font_get(14), label='Room Side(metre)',
                                                      length=self.dashboard_side[0]-5, variable=self.roomSide, from_=0.1,
                                                      to=15.1, tickinterval=3, resolution=0.1,
                                                      showvalue=1, relief='solid', bg='#ff6b87')
        self.room_side_scale.grid()
        EffectButton(('red', 'black'), self.dashboard, image=tk_image(
            'incense.png', width=300, height=74), bg='#ff6b87', command=incense).grid(sticky='we')
        EffectButton(('red', 'black'), self.dashboard, image=tk_image(
            'ex.png', width=100, height=74), bg='#ff6b87', command=air_cleaner).grid(sticky='we')

        air_cleaner()

    def __build_menu(self):
        menu = create_menu(self.top_menu)
        self.top_menu.add_cascade(label='Funtions', menu=menu)

        menu.add_command(label='Reset', command=self.__reset)
        menu.add_command(label='Execute', command=self.__execute)
        menu.add_command(label='Reference', command=self.__show_reference)

    def __reset(self):
        self.canvas.delete('all')
        parse_json_to_property(self, 'modules\\initial.json')
        self.__ini_ac()
        self.cadr_scale['variable'] = self.cadrValue
        self.room_side_scale['variable'] = self.roomSide
        self.cadr_scale.set(self.cadrValue.get())
        self.room_side_scale.set(self.roomSide.get())
        self.__depict_canvas()

    def __execute(self):
        wall = []
        for id_ in self.canvas.find_all():
            for tags in self.canvas.gettags(id_):
                if 'wall' in tags:
                    if self.canvas.itemcget(id_, 'state') == 'normal':
                        wall.append(int(tags[4:]))
        args = {
            'cadr_value': self.cadrValue.get(),
            'room_side': self.roomSide.get(),
            'incense_number': self.incenseNumber.get(),
            'ac_loc': self.acLocation.get(),
            'wall': wall
        }

        result = cal(args)
        log(args, result)

        for i in range(1, 10):
            x, y = self.canvas.coords(f'area{i}')
            self.canvas.delete(f'area{i}')
            self.canvas.create_text(
                x, y, text=result[i-1][0], font=font_get(24), tags=(f'area{i}'))

    def __show_reference(self):
        win = new_window('CADR reference', 'favicon.ico', self.side)

        info = {'HPA830WTW': 214, 'CAC-B1210FWCL': 323,
                'Blueair-3410': 425, 'KI-J100T': 530, 'Blueair-7770i': 735}
        for number, name in enumerate(info):
            making_widget('Label')(
                win, text=name, font=font_get(16), anchor='center').grid(row=1, column=number + 1, sticky='nsew')
            making_widget('Label')(win, image=tk_image(
                f'{name}.png', 300, 300, dirpath='images\\goods')).grid(row=2, column=number + 1)
            making_widget('Label')(win, text='CADR :  ' + str(info[name]),
                                   font=font_get(20), relief='solid', bg='#ff6b87', anchor='w').grid(row=3, column=number + 1, sticky='nsew')


if __name__ == '__main__':
    app = Main('Air polution simulation', 'favicon.ico')
    app.default_menu.add_command(
        label="Background color", command=lambda: background_color(app.canvas))

    while True:
        app.canvas.update()
        app.Musicplayers.set_ball()
