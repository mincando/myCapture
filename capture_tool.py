import os
import tkinter as tk
from PIL import ImageGrab, ImageTk
import keyboard

class ScreenCaptureTool:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        
        # tkinter 초기화 (화면 전체를 덮는 투명 창 생성)
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.3)  # 창 투명도 (0.3 = 30%)
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.config(cursor="cross")

        # 마우스 이벤트 바인딩
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        self.rect = None

    def on_button_press(self, event):
        # 시작 좌표 저장
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red', width=2)

    @property
    def x(self):
        return self.start_x

    @property
    def y(self):
        return self.start_y

    def on_move_press(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        # 드래그 중인 사각형 그리기
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.current_x, self.current_y)

    def on_button_release(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        self.root.withdraw() # 캡처 순간 창 숨기기
        self.root.update()
        
        # 시작점과 끝점 정렬 (거꾸로 드래그해도 작동하도록)
        x1 = min(self.start_x, self.current_x)
        y1 = min(self.start_y, self.current_y)
        x2 = max(self.start_x, self.current_x)
        y2 = max(self.start_y, self.current_y)
        
        if x2 - x1 > 0 and y2 - y1 > 0:
            # 지정한 영역 화면 캡처 후 클립보드(메모리) 저장
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            self.send_to_clipboard(img)
            
        self.root.destroy()

    def send_to_clipboard(self, img):
        # 이미지를 클립보드로 복사하는 Windows API 활용 (io 사용대신 간단하게 구현)
        import io
        from PIL import Image
        import win32clipboard

        output = io.BytesIO()
        img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    def start(self):
        self.root.mainloop()

def start_capture():
    app = ScreenCaptureTool()
    app.start()

if __name__ == "__main__":
    print("화면 캡처 프로그램이 백그라운드에서 실행 중입니다...")
    # 단축키 지정: ctrl + alt + s
    keyboard.add_hotkey('ctrl+alt+s', start_capture)
    keyboard.wait()