import tkinter
import asyncio
import time
from contextlib import suppress


class AsyncConsole(tkinter.Tk):
    def __init__(self, **tkargs):
        # super init
        super().__init__(**tkargs)

        # input
        self.__input_queue = None
        self.__input_future = None
        self.__input_loop_task = None
        self.__input_history = []
        self.__input_history_pos = 0

        # ui
        self.__output_frame = tkinter.Frame(self)
        self.__output_scroll = tkinter.Scrollbar(self.__output_frame)
        self.__output_text = tkinter.Text(self.__output_frame)

        self.__input_frame = tkinter.Frame(self)
        self.__input_prompt = tkinter.Label(self.__input_frame)
        self.__input_text = tkinter.Entry(self.__input_frame)

        # state
        self.__running = False
        self.__destroyed = False
        self.__done = None

        self.__init_ui()

    @property
    def running(self):
        return self.__running and not self.__destroyed

    def __init_ui(self):
        self.protocol('WM_DELETE_WINDOW', self.__win_destroyed)

        self.wait_visibility(self)
        self.set_colors('black', 'green2')

        self.config(bd=1, highlightthickness=0)

        self.__output_frame.config(bd=1, highlightthickness=0)

        self.__output_scroll.config(
            orient=tkinter.VERTICAL, command=self.__output_text.yview)
        self.__output_scroll.config(bd=0)

        self.__output_text.config(bd=0, highlightthickness=0)
        self.__output_text.config(font=('Courier New', 14))
        self.__output_text.bind('<Key>', self.__output_key_press)

        self.__output_frame.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.__output_scroll.pack(fill=tkinter.Y, side=tkinter.RIGHT)
        self.__output_text.pack(fill=tkinter.BOTH, expand=tkinter.YES)

        self.__input_frame.config(bd=2, highlightthickness=0)

        self.__input_text.config(font=('Courier New', 15))
        self.__input_text.config(bd=0, highlightthickness=0)
        self.__input_prompt.config(bd=0, highlightthickness=0)
        self.__input_prompt.config(font=('Courier New', 15))
        self.__input_prompt.config(text='>')

        self.__input_frame.pack(fill=tkinter.X)
        self.__input_prompt.pack(side=tkinter.LEFT)
        self.__input_text.pack(fill=tkinter.X)

        self.__input_text.bind('<Return>', (lambda _: self.__input_finish()))
        self.__input_text.bind('<Up>', (lambda _: self.__input_nav_up()))
        self.__input_text.bind('<Down>', (lambda _: self.__input_nav_down()))

        self.__input_disable()

    def __win_destroyed(self):
        self.__destroyed = True
        self.destroy()

    def __output_key_press(self, key):
        try:
            if (key.state == 4 or key.state == 6) and key.keysym.lower() == 'c':
                text = self.__output_text.get(tkinter.SEL_FIRST, tkinter.SEL_LAST)
                self.clipboard_clear()  
                self.clipboard_append(text)  
            elif (key.state == 4 or key.state == 6) and key.keysym.lower() == 'r':
                self.clear_output()
        except tkinter.TclError:
            pass
        
        return 'break'

    def __input_nav_up(self):
        if len(self.__input_history) == 0: return
        
        self.__input_history_pos -= 1
        if self.__input_history_pos < 0:
            self.__input_history_pos = 0
        if self.__input_history_pos >= len(self.__input_history):
            self.__input_history_pos = len(self.__input_history) -1

        self.__input_text.delete(0, tkinter.END)
        self.__input_text.insert(tkinter.END, self.__input_history[self.__input_history_pos])

    def __input_nav_down(self):
        if len(self.__input_history) == 0: return

        self.__input_history_pos += 1
        if self.__input_history_pos >= len(self.__input_history):
            self.__input_history_pos = len(self.__input_history)
            self.__input_text.delete(0, tkinter.END)
            return

        self.__input_text.delete(0, tkinter.END)
        self.__input_text.insert(tkinter.END, self.__input_history[self.__input_history_pos])

    def __input_finish(self):
        if self.__input_future and not self.__input_future.done():
            result = self.__input_text.get()
            self.__input_future.set_result(result)
            self.__input_save(result)

    def __input_save(self, result):
        if result:
            if self.__input_history:
                last = self.__input_history[len(self.__input_history) - 1]
                if last != result:
                    self.__input_history.append(result)
            else:
                self.__input_history.append(result)

        self.__input_history_pos = len(self.__input_history)

    def __input_enable(self, prompt):
        self.__input_text.config(state=tkinter.NORMAL)
        self.__input_prompt.config(state=tkinter.NORMAL)
        self.__input_prompt.config(text=prompt)

    def __input_disable(self):
        self.__input_text.delete(0, tkinter.END)
        self.__input_text.config(state=tkinter.DISABLED)
        self.__input_prompt.config(state=tkinter.DISABLED)
        self.__input_prompt.config(text='>')

    async def __input_loop(self):
        while True:
            self.__input_future, prompt = await self.__input_queue.get()

            if self.__input_future.done():
                self.__input_queue.task_done()
                continue

            self.__input_enable(prompt)

            with suppress(asyncio.CancelledError):
                await self.__input_future

            if self.__destroyed or not self.__running:
                break

            self.__input_disable()
            self.__input_queue.task_done()

    def input(self, prompt):
        if self.__destroyed or not self.__running:
            raise RuntimeError('console closed')

        future = asyncio.Future()
        self.__input_queue.put_nowait((future, prompt))
        return future

    def print(self, *args, sep=' ', end='\n'):
        if self.__destroyed or not self.__running:
            raise RuntimeError('console closed')

        print_str = sep.join(str(x) for x in args) + end
        self.__output_text.insert(tkinter.END, print_str)
        self.__output_text.see(tkinter.END)

    def clear_output(self):
        self.__output_text.delete('1.0', tkinter.END)

    def cancel_input(self):
        if self.__input_future and not self.__input_future.done():
            self.__input_disable()
            self.__input_future.set_exception(asyncio.CancelledError('input cancelled'))

    def set_colors(self, background, foreground):
        self.__output_frame.config(background=foreground)
        self.__output_scroll.config(background=background)
        self.__output_text.config(background=background, foreground=foreground)
        self.__output_text.config(insertbackground=foreground)
        self.__output_text.config(selectforeground=background)
        self.__output_text.config(selectbackground=foreground)
        self.__input_frame.config(bg=foreground)
        self.__input_prompt.config(background=background, foreground=foreground)
        self.__input_text.config(background=background, foreground=foreground)
        self.__input_text.config(insertbackground=foreground)
        self.__input_text.config(selectforeground=background)
        self.__input_text.config(selectbackground=foreground)
        self.__input_text.config(disabledbackground=background)
    
    def set_alpha(self, opacity):
        self.attributes('-alpha', opacity)
        self.wm_attributes('-alpha', opacity)

    async def mainloop(self):
        if self.__running:
            raise RuntimeError('aready running')

        if self.__destroyed:
            raise RuntimeError('destroyed')

        try:
            loop = asyncio.get_event_loop()

            self.__input_queue = asyncio.Queue()
            self.__input_loop_task = loop.create_task(self.__input_loop())
            self.__running = True

            while True:
                self.update()
                self.update_idletasks()
                await asyncio.sleep(0.01)
        except tkinter.TclError:
            pass
        finally:
            self.__running = False

            if not self.__input_loop_task.done():
                self.__input_loop_task.cancel()

            if self.__input_future and not self.__input_future.done():
                self.__input_future.set_exception(asyncio.CancelledError('console closed'))

            while not self.__input_queue.empty():
                future, _ = self.__input_queue.get_nowait()
                future.set_exception(asyncio.CancelledError('console closed'))
                
            with suppress(asyncio.CancelledError):
                await self.__input_loop_task

    def run(self, loop=None):
        if not loop:
            loop = asyncio.get_event_loop()

        return loop.create_task(self.mainloop())
