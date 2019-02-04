import asyncio
import os.path
import tkinter as tk


class AsyncConsole(tk.Tk):
    def __init__(self):
        super().__init__()

        #basic values:
        self.__history = []
        self.__history_pos = 0
        self.__input_future = None
        self.__input_queue = asyncio.Queue()
        self.__output_queue = asyncio.Queue()

        #gui color options:
        self.__foreground_c = 'green'
        self.__background_c = 'black'
        self.__disabled_c = 'dimgray'

        #gui components:
        self.__output_frame = tk.Frame(self)
        self.__output_scroll = tk.Scrollbar(self.__output_frame)
        self.__output = tk.Text(self.__output_frame)

        self.__input_frame = tk.Frame(self)
        self.__input_prompt = tk.Label(self.__input_frame)
        self.__input = tk.Entry(self.__input_frame)

        #build the style for components
        self.title(os.getcwd())
        self._config_ui()

    def _config_ui(self):
        self.config(bd=1, highlightthickness=0)

        self.__output_frame.config(bd=1, highlightthickness=0)

        self.__output_scroll.config(orient=tk.VERTICAL, command=self.__output.yview)
        self.__output_scroll.config(bd=0)
        
        self.__output.config(bd=0, highlightthickness=0)
        self.__output.config(font=("Courier New", 14))
        self.__output.config(state=tk.DISABLED)

        self.__output_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.__output_scroll.pack(fill=tk.Y, side=tk.RIGHT)
        self.__output.pack(fill=tk.BOTH, expand=tk.YES)

        self.__input_frame.config(bd=2, highlightthickness=0)

        self.__input.config(font=("Courier New", 15))
        self.__input.config(bd=0, highlightthickness=0)
        self.__input_prompt.config(bd=0, highlightthickness=0)
        self.__input_prompt.config(font=("Courier New", 15))
        self.__input_prompt.config(text=">")

        self.__input_frame.pack(fill=tk.X)
        self.__input_prompt.pack(side=tk.LEFT)
        self.__input.pack(fill=tk.X)

        self.__input.bind('<Return>', (lambda _: self._finish_input()))
        self.__input.bind('<Up>', (lambda _: self._nav_up_input()))
        self.__input.bind('<Down>', (lambda _: self._nav_down_input()))

        self._disable_input()
        self._update_colors()

    def _update_colors(self):
        self.__output_frame.config(background=self.__foreground_c)

        self.__output_scroll.config(background=self.__background_c)

        self.__output.config(background=self.__background_c, foreground=self.__foreground_c)

        self.__output.config(insertbackground=self.__foreground_c)
        self.__output.config(selectforeground=self.__background_c)
        self.__output.config(selectbackground=self.__foreground_c)

        self.__input_frame.config(bg=self.__foreground_c)

        self.__input_prompt.config(background=self.__background_c, foreground=self.__foreground_c)

        self.__input.config(background=self.__background_c, foreground=self.__foreground_c)
        self.__input.config(insertbackground=self.__foreground_c)
        self.__input.config(selectforeground=self.__background_c)
        self.__input.config(selectbackground=self.__foreground_c)
        self.__input.config(disabledbackground=self.__background_c)

    def _nav_down_input(self):
        if len(self.__history) == 0: return

        self.__history_pos += 1
        if self.__history_pos >= len(self.__history):
            self.__history_pos = len(self.__history)
            self.__input.delete(0, tk.END)
            return

        self.__input.delete(0, tk.END)
        self.__input.insert(tk.END, self.__history[self.__history_pos])

    def _nav_up_input(self):
        if len(self.__history) == 0: return
        
        self.__history_pos -= 1
        if self.__history_pos < 0:
            self.__history_pos = 0
        if self.__history_pos >= len(self.__history):
            self.__history_pos = len(self.__history) -1

        self.__input.delete(0, tk.END)
        self.__input.insert(tk.END, self.__history[self.__history_pos])

    def _disable_input(self):
        self.__input.config(state=tk.DISABLED)
        self.__input_prompt.config(state=tk.DISABLED)
        self.__input_prompt.config(text=">")

    def _enable_input(self, input_str, result):
        self.__input.config(state=tk.NORMAL)
        self.__input_prompt.config(state=tk.NORMAL)
        self.__input_prompt.config(text=input_str)

        self.__input_future = result

    def _save_input(self):
        i = self.__input.get()
        l = len(self.__history)

        if len(i) != 0:
            if l == 0:
                self.__history.append(i)
            elif self.__history[l-1] != i:
                self.__history.append(i)

        self.__history_pos = l+1

    def _finish_input(self):
        if self.__input_future != None:
            if not self.__input_future.done():
                self._save_input()

                self.__input_future.set_result(self.__input.get())
                self.__input.delete(0, tk.END)
                self.__input_future = None
            
    async def _input_loop(self):
        while True:
            input_str, completed = await self.__input_queue.get()
            
            input_future = asyncio.Future()
            self._enable_input(input_str, input_future)

            result = await input_future
            completed.set_result(result)
            self._disable_input()

    async def _output_loop(self):
        while True:
            print_str, completed = await self.__output_queue.get()

            self.__output.config(state=tk.NORMAL)
            self.__output.insert(tk.END, print_str)
            self.__output.see(tk.END)
            self.__output.config(state=tk.DISABLED)

            completed.set_result(None)

    def set_foreground(self, color):
        self.__foreground_c = color
        self._update_colors()

    def set_background(self, color):
        self.__background_c = color
        self._update_colors()

    def set_disabled(self, color):
        self.__disabled_c = color
        self._update_colors()

    def clear_output(self):
        self.__output.config(state=tk.NORMAL)
        self.__output.delete(1.0, tk.END)
        self.__output.config(state=tk.DISABLED)

    def cancel_input(self):
        if self.__input_future != None:
            if not self.__input_future.done():
                self.__input_future.set_result(None)
                self.__input.delete(0, tk.END)
            
    async def print(self, *args, sep=' ', end='\n'):
        print_str = sep.join(str(x) for x in args) + end
        completed = asyncio.Future()

        await self.__output_queue.put((print_str, completed))
        await completed

    def print_no_wait(self, *args, sep=' ', end='\n'):
        print_str = sep.join(str(x) for x in args) + end

        self.__output.config(state=tk.NORMAL)
        self.__output.insert(tk.END, print_str)
        self.__output.see(tk.END)
        self.__output.config(state=tk.DISABLED)

    async def input(self, prompt):
        completed = asyncio.Future()

        await self.__input_queue.put((prompt, completed))

        result = await completed
        return result

    async def mainloop(self):
        loop = asyncio.get_event_loop()

        loop.create_task(self._output_loop())
        loop.create_task(self._input_loop())

        while True:
            self.update()
            await asyncio.sleep(1/60) #60 fps

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    cmd = AsyncCmd()

    loop.run_until_complete(cmd.mainloop())