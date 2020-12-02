import tkinter as tk
import control as ct


class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = 0
        self.y = 0

    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + cx + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{int(x)}+{int(y)}")
        label = tk.Label(tw, text=self.text, justify='center',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

    @staticmethod
    def CreateToolTip(widget, text):
        toolTip = ToolTip(widget)

        def enter(event):
            toolTip.showtip(text)

        def leave(event):
            toolTip.hidetip()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)


def load_icon(image_name, image_ext='png', path='./images'):
    image = tk.PhotoImage(file=f'{path}/{image_name}.{image_ext}')
    return image


class WeatherApp(tk.Frame):
    def __init__(self,  master=None):
        super().__init__(master, bg='#5caeb5')
        self.create_widgets()
        self.create_bindings()
        self.w = ct.WeahterAppModel()

    def create_widgets(self):
        self.serach_frame = tk.Frame(self)
        self.serach_frame.place(relx=0, rely=0.1, relwidth=0.8)
        self.input_entry = tk.Entry(self.serach_frame, font=('Times', 24))
        self.input_entry.pack(fill='both', expand=True, side='left')
        self.input_entry.focus()
        button_image = load_icon('weather-app')
        self.get_weather_button = tk.Button(
            self.serach_frame,
            image=button_image,
            command=lambda: self.get_weather(self.input_entry.get())
        )
        self.get_weather_button.image = button_image
        self.get_weather_button.pack(fill='both', expand=True)
        self.output_frame = tk.Frame(self, bg='white')
        self.output_frame.place(relx=0, rely=0.31, relwidth=0.8, relheight=0.6)
        self.output_label = tk.Label(
            self.output_frame,
            bg='white',
            justify='left',
            anchor='nw',
            font=('Times', 18)
        )
        self.output_label.font = button_image
        self.output_label.pack(side='left', fill='both', expand=True)
        self.icon_place = tk.Canvas(
            self.output_frame,
            width=50,
            height=50,
            bd=0,
            highlightthickness=0,
            bg='white'
        )
        self.icon_place.pack(anchor='ne')

    def create_bindings(self):
        self.master.bind('<Return>', self.get_weather)
        ToolTip.CreateToolTip(
            self.get_weather_button, 'press enter to get the weather')

    def get_weather(self, event):
        w = self.w
        w.MakeRequest(self.input_entry.get())
        if not w.failedToGetResponse():
            self.output_label['text'] = w.getText()
            w_icon = load_icon(w.getIcon())
            self.icon_place.delete('all')
            self.icon_place.create_image(25, 25, image=w_icon)
            self.icon_place.image = w_icon
        else:
            self.output_label['text'] = w.getErrorMessage()
            self.icon_place.delete('all')


def main():
    root = tk.Tk()
    root.title('Weather')
    w = WeatherApp(root).pack(fill='both', expand=True)
    root.minsize(600, 400)
    root.mainloop()


if __name__ == '__main__':
    main()
