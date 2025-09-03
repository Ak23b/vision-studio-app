import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk, ImageEnhance
import numpy as np

class VisionStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Vision Studio")
        self.root.geometry("900x600")

        # Notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Tabs
        self.filters_tab = ttk.Frame(self.notebook)
        self.editor_tab = ttk.Frame(self.notebook)
        self.webcam_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.filters_tab, text="Filters")
        self.notebook.add(self.editor_tab, text="Editor")
        self.notebook.add(self.webcam_tab, text="Webcam")

        # Variables
        self.image = None
        self.tk_image = None
        self.webcam_running = False

        # Build Tabs
        self.build_filters_tab()
        self.build_editor_tab()
        self.build_webcam_tab()

    def build_filters_tab(self):
        btn_frame = tk.Frame(self.filters_tab)
        btn_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Button(btn_frame, text="Load Image", command=self.load_image, bg="#ADD8E6").pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Grayscale", command=self.apply_grayscale, bg="#ADD8E6").pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Blur", command=self.apply_blur, bg="#ADD8E6").pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Sharpen", command=self.apply_sharpen, bg="#ADD8E6").pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Edge Detection", command=self.apply_edge, bg="#ADD8E6").pack(fill="x", pady=5)

        self.filter_canvas = tk.Label(self.filters_tab)
        self.filter_canvas.pack(side="right", expand=True)

    def build_editor_tab(self):
        btn_frame = tk.Frame(self.editor_tab)
        btn_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Button(btn_frame, text="Load Image", command=self.load_image, bg="pink").pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Brightness +", command=lambda: self.adjust_brightness(1.2), bg="pink").pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Brightness -", command=lambda: self.adjust_brightness(0.8), bg="pink").pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Contrast +", command=lambda: self.adjust_contrast(1.2), bg="pink").pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Contrast -", command=lambda: self.adjust_contrast(0.8), bg="pink").pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Rotate", command=self.rotate_image, bg="pink").pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Resize 50%", command=self.resize_half, bg="pink").pack(fill="x", pady=5)

        self.editor_canvas = tk.Label(self.editor_tab)
        self.editor_canvas.pack(side="right", expand=True)

    def build_webcam_tab(self):
        btn_frame = tk.Frame(self.webcam_tab)
        btn_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Button(btn_frame, text="Start Webcam", command=self.start_webcam, bg="orange").pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Stop Webcam", command=self.stop_webcam, bg="orange").pack(fill="x", pady=5)

        self.webcam_canvas = tk.Label(self.webcam_tab)
        self.webcam_canvas.pack(side="right", expand=True)

    # Image loading
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if not file_path:
            return
        self.image = cv2.imread(file_path)
        self.display_image(self.image)

    def display_image(self, img):
        if img is None:
            return
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        self.tk_image = ImageTk.PhotoImage(img_pil)

        if self.notebook.index(self.notebook.select()) == 0:
            self.filter_canvas.config(image=self.tk_image)
        else:
            self.editor_canvas.config(image=self.tk_image)

    # Filters
    def apply_grayscale(self):
        if self.image is None:
            return
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        self.display_image(gray)

    def apply_blur(self):
        if self.image is None:
            return
        blur = cv2.GaussianBlur(self.image, (15, 15), 0)
        self.display_image(blur)

    def apply_sharpen(self):
        if self.image is None:
            return
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        sharp = cv2.filter2D(self.image, -1, kernel)
        self.display_image(sharp)

    def apply_edge(self):
        if self.image is None:
            return
        edges = cv2.Canny(self.image, 100, 200)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        self.display_image(edges)

    # Editor functions
    def adjust_brightness(self, factor):
        if self.image is None:
            return
        pil_img = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Brightness(pil_img)
        img_enhanced = enhancer.enhance(factor)
        self.image = cv2.cvtColor(np.array(img_enhanced), cv2.COLOR_RGB2BGR)
        self.display_image(self.image)

    def adjust_contrast(self, factor):
        if self.image is None:
            return
        pil_img = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Contrast(pil_img)
        img_enhanced = enhancer.enhance(factor)
        self.image = cv2.cvtColor(np.array(img_enhanced), cv2.COLOR_RGB2BGR)
        self.display_image(self.image)

    def rotate_image(self):
        if self.image is None:
            return
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        self.display_image(self.image)

    def resize_half(self):
        if self.image is None:
            return
        h, w = self.image.shape[:2]
        self.image = cv2.resize(self.image, (w // 2, h // 2))
        self.display_image(self.image)

    # Webcam
    def start_webcam(self):
        if self.webcam_running:
            return
        self.webcam_running = True
        self.capture = cv2.VideoCapture(0)
        self.update_webcam()

    def update_webcam(self):
        if not self.webcam_running:
            return
        ret, frame = self.capture.read()
        if ret:
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            self.tk_image = ImageTk.PhotoImage(img_pil)
            self.webcam_canvas.config(image=self.tk_image)
        self.root.after(30, self.update_webcam)

    def stop_webcam(self):
        self.webcam_running = False
        if hasattr(self, 'capture'):
            self.capture.release()
            self.webcam_canvas.config(image="")

if __name__ == "__main__":
    root = tk.Tk()
    app = VisionStudio(root)
    root.mainloop()
