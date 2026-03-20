# 🚀 Watermark System GUI

基于 [blind_watermark](https://github.com/guofei9987/blind_watermark) 实现的 **图像盲水印工具（GUI版）**  
支持批量嵌入 / 提取水印，带可视化界面与记录系统。

---

## ✨ 功能特性

- 🖼️ 支持图片水印嵌入（PNG / JPG / JPEG）
- 🔍 支持水印提取
- 📁 支持单文件 / 文件夹批量处理
- 🧾 自动记录水印长度与内容
- 📂 自动分类输出结果
- 🖥️ Tkinter 科技风 GUI 界面
- 📜 内置日志输出窗口

---

## 📦 依赖安装

```bash
pip install blind-watermark
```

---

## 📁 项目结构

```
project/
│
├── main.py                  # 主程序
├── output/                 # 输出目录（自动生成）
│   └── 文件名/
│       ├── wm_xxx.jpg
│       ├── xxx.jpg
│       └── 水印.txt
│
├── wm_info/               # 水印信息记录（自动生成）
│   └── wm_len_水印名.txt
│
└── README.md
```

---

## 🚀 使用方法

### 1️⃣ 启动程序

```bash
python main.py
```

---

### 2️⃣ 界面说明

```
标题
路径选择
模式选择

🟢 嵌入 / 🔵 提取 输入框

📜 输入框（根据模式填写）

▶️ 开始执行按钮

📜 输出日志窗口
```

---

## 🟢 嵌入模式

### 输入：

- 选择图片 / 文件夹路径
- 输入 **水印名称（字符串）**

### 执行：

- 自动生成带水印图片
- 原图移动到 output 目录
- 生成水印信息文件

### 输出示例：

```
output/xxx/
├── wm_xxx.jpg      # 带水印
├── xxx.jpg         # 原图
└── 水印.txt
```

---

## 🔵 提取模式

### 输入：

- 选择图片 / 文件夹
- 输入 **水印长度（数字）**

> ⚠️ 水印长度必须正确，否则提取失败

### 输出：

```
🔍 提取到的水印内容
```

或批量：

```
xxx.jpg → watermark
```

---

## 📊 水印记录机制

每个水印会自动记录在：

```
wm_info/wm_len_水印名.txt
```

内容示例：

```
水印长度：64
水印内容：admin
使用此水印的文件名
test.jpg
test2.jpg
```

---

## ⚠️ 注意事项

- 水印长度必须保存，否则无法提取
- 图片会被移动到 output 目录（不是复制）
- 不支持非图片文件
- 密码固定为：

```python
password_img = 1
password_wm = 1
```

> 如需增强安全性可自行修改

---

## 🛠️ 可扩展方向

- 🔐 自定义密码输入
- 🎨 支持图片水印（非文本）
- 📊 GUI 进度条
- 🧠 自动读取水印长度
- 🌐 Web 版本（Flask / FastAPI）

---

## 📜 License

MIT License

---

## 🙌 致谢

- blind_watermark 作者
- Tkinter GUI
