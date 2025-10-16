import tkinter as tk
from tkinter import scrolledtext

# --- 기본 창 설정 ---
# 1. 메인 윈도우 생성
window = tk.Tk()

# 2. 창 제목 설정
window.title("메모장")

# 3. 창 초기 크기 설정
window.geometry("800x600")


# --- 메뉴 바 생성 ---
def exit_app():
    """프로그램을 종료하는 함수"""
    window.destroy()

# 메뉴 바 위젯 생성
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# '파일' 메뉴 생성
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="파일(F)", menu=file_menu)

# '파일' 메뉴에 '종료' 항목 추가
file_menu.add_command(label="종료(X)", command=exit_app)


# --- 텍스트 편집 영역 생성 ---
# 4. 스크롤 가능한 텍스트 위젯 생성
# wrap=tk.WORD: 단어 단위로 자동 줄바꿈
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, undo=True)

# 5. 텍스트 위젯을 창에 꽉 채우도록 배치
# expand=True: 창 크기가 변경될 때 함께 크기 조절
# fill='both': 가로, 세로 방향으로 모두 채움
text_area.pack(expand=True, fill='both')


# --- 메인 루프 시작 ---
# 6. 창이 화면에 나타나고 사용자 입력을 기다리도록 함
window.mainloop()
#