import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import filedialog
import os
from tkinter import messagebox

class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.tab_counter = 0
        self.file_paths = {} # 각 탭의 파일 경로를 저장하는 딕셔너리
        self.setup_ui()

    def setup_ui(self):
        """UI의 기본 구조를 설정합니다."""
        self.root.title("메모장")
        self.root.geometry("800x600")

        self.create_menu()

        # 탭 관리를 위한 Notebook 위젯 생성
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # 첫 번째 탭 생성
        self.create_new_tab()

    def create_menu(self):
        """메뉴 바를 생성하고 메뉴 항목을 추가합니다."""
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="파일(F)", menu=file_menu)

        file_menu.add_command(label="새 파일(N)", command=self.create_new_tab, accelerator="Ctrl+N")
        file_menu.add_command(label="열기(O)...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="저장(S)", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="다른 이름으로 저장(A)...", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="탭 닫기(W)", command=self.close_current_tab)
        file_menu.add_separator()
        file_menu.add_command(label="종료(X)", command=self.exit_app)

        # 편집 메뉴 생성
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="편집(E)", menu=edit_menu)

        edit_menu.add_command(label="실행 취소(U)", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="다시 실행(R)", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="잘라내기(T)", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="복사(C)", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="붙여넣기(P)", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="모두 선택(A)", command=self.select_all, accelerator="Ctrl+A")

        # 키보드 단축키 바인딩
        # 윈도우에서는 보통 Control
        self.root.bind_all('<Control-n>', lambda e: self.create_new_tab())
        self.root.bind_all('<Control-o>', lambda e: self.open_file())
        self.root.bind_all('<Control-s>', lambda e: self.save_file())
        self.root.bind_all('<Control-S>', lambda e: self.save_as_file())
        self.root.bind_all('<Control-w>', lambda e: self.close_current_tab())
        self.root.bind_all('<Control-q>', lambda e: self.exit_app())

        # 편집 단축키
        self.root.bind_all('<Control-z>', lambda e: self.undo())
        self.root.bind_all('<Control-y>', lambda e: self.redo())
        self.root.bind_all('<Control-x>', lambda e: self.cut())
        self.root.bind_all('<Control-c>', lambda e: self.copy())
        self.root.bind_all('<Control-v>', lambda e: self.paste())
        self.root.bind_all('<Control-a>', lambda e: self.select_all())

    def create_new_tab(self):
        """새로운 탭과 텍스트 영역을 생성합니다."""
        self.tab_counter += 1
        tab_title = f"새 문서 {self.tab_counter}"

        # 탭으로 사용할 프레임 생성
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=tab_title)

        # 텍스트 영역 생성
        text_area = scrolledtext.ScrolledText(tab_frame, wrap=tk.WORD, undo=True)
        text_area.pack(expand=True, fill='both')

        # 새 탭에 대한 파일 경로를 None으로 초기화
        self.file_paths[tab_frame] = None

        # 새로 만든 탭을 활성화
        self.notebook.select(tab_frame)

    def close_current_tab(self):
        """현재 활성화된 탭을 닫습니다."""
        # 선택된 탭이 있는지 확인
        if self.notebook.index("end") == 0:
            return # 탭이 하나도 없으면 아무것도 안 함
        
        selected_tab = self.notebook.select()
        # 해당 탭의 파일 경로 정보도 삭제
        if selected_tab in self.file_paths:
            del self.file_paths[selected_tab]

        self.notebook.forget(selected_tab)

    def exit_app(self):
        """프로그램을 종료합니다."""
        self.root.destroy()

    def open_file(self):
        """파일을 열어 새 탭에 표시합니다."""
        file_path = filedialog.askopenfilename(
            title="파일 열기",
            filetypes=(("텍스트 문서", "*.txt"), ("모든 파일", "*.*"))
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        except Exception as e:
            tk.messagebox.showerror("오류", f"파일을 읽는 중 오류가 발생했습니다:\n{e}")
            return

        self.create_new_tab()
        
        # 새로 만든 탭에 내용 채우기
        current_tab = self.notebook.nametowidget(self.notebook.select())
        text_area = current_tab.winfo_children()[0]
        text_area.delete("1.0", tk.END)
        text_area.insert("1.0", content)

        # 탭 제목을 파일 이름으로 변경하고 파일 경로 저장
        file_name = os.path.basename(file_path)
        self.notebook.tab(current_tab, text=file_name)
        self.file_paths[current_tab] = file_path

    def save_file(self):
        """현재 탭의 내용을 저장합니다."""
        current_tab = self.notebook.nametowidget(self.notebook.select())
        file_path = self.file_paths.get(current_tab)

        if file_path and os.path.exists(file_path):
            # 파일 경로가 있으면 덮어쓰기
            text_area = current_tab.winfo_children()[0]
            content = text_area.get("1.0", tk.END)
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
            except Exception as e:
                tk.messagebox.showerror("오류", f"파일을 저장하는 중 오류가 발생했습니다:\n{e}")
        else:
            # 파일 경로가 없으면 '다른 이름으로 저장' 호출
            self.save_as_file()

    def save_as_file(self):
        """현재 탭의 내용을 새 파일로 저장합니다."""
        file_path = filedialog.asksaveasfilename(
            title="다른 이름으로 저장",
            defaultextension=".txt",
            filetypes=(("텍스트 문서", "*.txt"), ("모든 파일", "*.*"))
        )
        if not file_path:
            return

        # save_file 로직을 재사용하여 저장
        current_tab = self.notebook.nametowidget(self.notebook.select())
        self.file_paths[current_tab] = file_path
        self.save_file()
        # 탭 제목 업데이트
        file_name = os.path.basename(file_path)
        self.notebook.tab(current_tab, text=file_name)

    def get_current_text_area(self):
        """현재 활성화된 탭의 텍스트 위젯을 반환합니다."""
        try:
            current_tab = self.notebook.nametowidget(self.notebook.select())
            # ScrolledText 위젯은 프레임의 자식 위젯 중 첫 번째입니다.
            return current_tab.winfo_children()[0]
        except (tk.TclError, IndexError):
            # 탭이 하나도 없을 경우
            return None

    def undo(self):
        text_area = self.get_current_text_area()
        if text_area:
            try:
                text_area.edit_undo()
            except tk.TclError:
                pass # 실행 취소 스택이 비어있을 때의 오류 무시

    def redo(self):
        text_area = self.get_current_text_area()
        if text_area:
            try:
                text_area.edit_redo()
            except tk.TclError:
                pass # 다시 실행 스택이 비어있을 때의 오류 무시

    def cut(self):
        text_area = self.get_current_text_area()
        if text_area:
            text_area.event_generate("<<Cut>>")

    def copy(self):
        text_area = self.get_current_text_area()
        if text_area:
            text_area.event_generate("<<Copy>>")

    def paste(self):
        text_area = self.get_current_text_area()
        if text_area:
            text_area.event_generate("<<Paste>>")

    def select_all(self):
        text_area = self.get_current_text_area()
        if text_area:
            # 포커스를 텍스트 영역에 주고 실제 텍스트 끝 바로 전까지 선택
            text_area.focus_set()
            try:
                text_area.tag_add("sel", "1.0", "end-1c")
                text_area.mark_set("insert", "1.0")
                text_area.see("insert")
            except tk.TclError:
                # 비어있는 문서 등 예외는 무시
                pass

if __name__ == "__main__":
    # --- 기본 창 설정 ---
    # 1. 메인 윈도우 생성
    window = tk.Tk()

    # 2. NotepadApp 클래스의 인스턴스 생성
    app = NotepadApp(window)

    # --- 메인 루프 시작 ---
    # 3. 창이 화면에 나타나고 사용자 입력을 기다리도록 함
    window.mainloop()
#ㅁ
