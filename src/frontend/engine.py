# Name: engine.py
# Author: Carter Hidalgo
#
# Purpose: methods for loading, sending, and receiving uci commands from chess engines

import subprocess, re, threading, queue
from frontend.board import Board
from colors.colors import yellow, green, cyan, grey

class Engine:
    UCIOK = r"uciok"
    READYOK = r"readyok"
    BESTMOVE = r"^bestmove\s+(\S+)"
    PERFT = r"^([a-z0-9]{4,5}): (\d+)"
    NODES_SEARCHED = r"Nodes searched: (\d+)"

    def _text(self, text, color):
        if color == "yellow":
            return yellow(text)
        elif color == "green":
            return green(text)
        elif color == "cyan":
            return cyan(text)
        elif color == "grey":
            return grey(text)
        else:
            return text 

    def __init__(self, exe_path, name, color, teacher):
        self.stop_event = threading.Event()
        self.process = subprocess.Popen(
            [exe_path], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True
        )
        self.output_queue = queue.Queue()
        self.engine_thread = threading.Thread(target = self._listen_output)
        self.engine_thread.start()
        self.name = name
        self.color = color
        self.time = Board.play_time
        self.teacher = teacher

        if not self.teacher:
            print(f"[{self._text('server', 'yellow')}]: loaded [{self._text(self.name, self.color)}]")
    
    def _listen_output(self):
        while not self.stop_event.is_set():
            if self.process.poll() is not None:
                break

            line = self.process.stdout.readline()
            if line:
                if not self.teacher:
                    print(f"[{self._text(self.name, self.color)}] -> [{self._text('server', 'yellow')}]: {line.strip()}")
                self.output_queue.put(line.strip())
            else:
                break;
    
    def _matcher(self, regex, text):
        match = re.match(regex, text)

        if not match:
            return None
        elif match.lastindex is not None:
            return match.group(1)
        else:
            return match.group(0)

    def _wait_for_value(self, regex):
        while True:
            while not self.output_queue.empty():
                value = self._matcher(regex, self.output_queue.get())
                if value:
                    return value
                
    def _get_output(self):
        return self.output_queue
                
    def get_time(self):
        return int(self.time)
    
    def sub_time(self, time):
        self.time -= time

    def send(self, cmd):
        if not self.teacher:
            print(f"[{self._text('server','yellow')}] -> [{self._text(self.name,self.color)}]: {cmd}")
        self.process.stdin.write(cmd + "\n")
        self.process.stdin.flush()
    
    def send_and_wait(self, cmd, value):
        self.send(cmd)
        return self._wait_for_value(value)

    def isready_wait(self):
        self.send("isready")
        return self._wait_for_value(Engine.READYOK)
    
    def get_perft(self):
        cmd = "position fen " + Board.get_start_fen()
        if(Board.moves):
            cmd += " moves "
            for move in Board.moves:
                cmd += move + " "
        self.send(cmd)
        self.send("go perft 1")

        perft = []

        finished = False

        while not finished:
            value = self.output_queue.get()

            match = re.match(Engine.PERFT, value)
            if match:
                perft.append(match.group(1))

            match = re.match(Engine.NODES_SEARCHED, value)
            if match:
                finished = True

        return perft
    
    def close(self):
        if self.process.poll() is None:
            self.process.terminate()
    
        self.stop_event.set() 
        self.engine_thread.join(timeout=1)

        self.process.stdout.close()

        if not self.teacher:
            print(f"[{self._text('server','yellow')}]: closed [{self._text(self.name,self.color)}]")