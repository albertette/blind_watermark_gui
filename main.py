import os
from tkinter import *
from tkinter import filedialog, messagebox
from blind_watermark import WaterMark

# =========================
# 核心功能（不变）
# =========================

def embed_image(input_path, output_path, wm_text):
    bwm = WaterMark(password_img=1, password_wm=1)
    bwm.read_img(input_path)
    bwm.read_wm(wm_text, mode='str')
    bwm.embed(output_path)
    return len(bwm.wm_bit)


def extract_image(input_path, wm_len):
    bwm = WaterMark(password_img=1, password_wm=1)
    return bwm.extract(input_path, wm_shape=wm_len, mode='str')


def save_wm_info(wm_name, wm_len, filename):
    os.makedirs('wm_info', exist_ok=True)
    file_path = f"wm_info/wm_len_{wm_name}.txt"

    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"水印长度：{wm_len}\n")
            f.write(f"水印内容：{wm_name}\n")
            f.write("使用此水印的文件名\n")
            f.write(f"{filename}\n")
    else:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"{filename}\n")


def load_wm_len(wm_name):
    file_path = f"wm_info/wm_len_{wm_name}.txt"
    if not os.path.exists(file_path):
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("水印长度："):
                return int(line.replace("水印长度：", "").strip())
    return None

# =========================
# GUI（科技风优化）
# =========================

class WatermarkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Watermark System")
        self.root.geometry("720x500")
        self.root.configure(bg="#0f172a")  # 深蓝背景

        self.path = StringVar()
        self.mode = StringVar(value="embed")

        self.build_ui()

    def build_ui(self):
        # 标题
        Label(self.root, text="WATERMARK SYSTEM", fg="#38bdf8", bg="#0f172a",
              font=("Consolas", 20, "bold")).pack(pady=10)

        # 路径
        frame = Frame(self.root, bg="#0f172a")
        frame.pack(pady=10)

        Entry(frame, textvariable=self.path, width=60, bg="#1e293b", fg="white",
              insertbackground="white", relief=FLAT).pack(side=LEFT, padx=5, ipady=5)

        Button(frame, text="浏览", command=self.select_path,
               bg="#38bdf8", fg="black", relief=FLAT).pack(side=LEFT)

        # 模式
        mode_frame = Frame(self.root, bg="#0f172a")
        mode_frame.pack(pady=10)

        Radiobutton(mode_frame, text="嵌入", variable=self.mode, value="embed",
                    bg="#0f172a", fg="white", selectcolor="#1e293b").pack(side=LEFT, padx=20)

        Radiobutton(mode_frame, text="提取", variable=self.mode, value="extract",
                    bg="#0f172a", fg="white", selectcolor="#1e293b").pack(side=LEFT, padx=20)

        # 水印名称（嵌入用）
        Label(self.root, text="水印名称（嵌入）", fg="#94a3b8", bg="#0f172a").pack()

        self.wm_name_entry = Entry(self.root, width=30, bg="#1e293b", fg="white",
                                   insertbackground="white", relief=FLAT)
        self.wm_name_entry.pack(ipady=5, pady=5)

        # 水印长度（提取用）
        Label(self.root, text="水印长度（提取）", fg="#94a3b8", bg="#0f172a").pack()

        self.wm_len_entry = Entry(self.root, width=30, bg="#1e293b", fg="white",
                                  insertbackground="white", relief=FLAT)
        self.wm_len_entry.pack(ipady=5, pady=5)

        # 按钮
        Button(self.root, text="开始执行", command=self.run,
               bg="#22c55e", fg="black", relief=FLAT, width=20, height=2).pack(pady=15)

        # 输出框（终端风格）
        self.output = Text(self.root, height=12, bg="#020617", fg="#22c55e",
                           insertbackground="white", relief=FLAT)
        self.output.pack(fill=BOTH, padx=15, pady=10)

    def log(self, msg):
        self.output.insert(END, msg + "\n")
        self.output.see(END)

    def select_path(self):
        path = filedialog.askopenfilename() or filedialog.askdirectory()
        self.path.set(path)

    def run(self):
        path = self.path.get()
        wm_name = self.wm_name_entry.get().strip()
        wm_len_input = self.wm_len_entry.get().strip()

        if not path:
            messagebox.showerror("错误", "路径不能为空")
            return

        if self.mode.get() == "embed":
            if not wm_name:
                messagebox.showerror("错误", "嵌入模式需要水印名称")
                return
            self.run_embed(path, wm_name)
        else:
            if not wm_len_input.isdigit():
                messagebox.showerror("错误", "提取模式需要输入数字水印长度")
                return
            wm_len = int(wm_len_input)
            self.run_extract(path, wm_len)

    def run_embed(self, path, wm_name):
        if os.path.isfile(path):
            self.process_file(path, wm_name)

        elif os.path.isdir(path):
            for file in os.listdir(path):
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    self.process_file(os.path.join(path, file), wm_name)
        else:
            self.log("❌ 路径无效")

    def process_file(self, input_path, wm_name):
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)

        folder = os.path.join('output', name)
        os.makedirs(folder, exist_ok=True)

        output_path = os.path.join(folder, f"wm_{filename}")
        original_path = os.path.join(folder, filename)
        txt_path = os.path.join(folder, "水印.txt")

        wm_len = embed_image(input_path, output_path, wm_name)

        os.replace(input_path, original_path)

        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"水印长度：{wm_len}\n")
            f.write(f"水印内容：{wm_name}\n")

        save_wm_info(wm_name, wm_len, filename)

        self.log(f"✅ 完成: {folder}")

    def run_extract(self, path, wm_len):
        if os.path.isfile(path):
            wm = extract_image(path, wm_len)
            self.log(f"🔍 {wm}")

        elif os.path.isdir(path):
            for file in os.listdir(path):
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    inp = os.path.join(path, file)
                    wm = extract_image(inp, wm_len)
                    self.log(f"{file} → {wm}")
        else:
            self.log("❌ 路径无效")


if __name__ == '__main__':
    root = Tk()
    app = WatermarkGUI(root)
    root.mainloop()
