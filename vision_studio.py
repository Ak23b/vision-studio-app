import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np

# Global variables
img = None          # stores full-resolution image
display_img = None  # stores the resized image for display
img_tk = None       # stores Tkinter image reference

# Button colors
FILTER_BTN_COLOR = "#ADD8E6"   # light blue
EDITOR_BTN_COLOR = "#FFB6C1"   # pink
WEBCAM_BTN_COLOR = "#FFA500"   # orange


# ---------- Utility: Resize + Display image ----------
def resize_for_display(image, max_w=600, max_h=400):
    """Resize image to fit into max_w x max_h while keeping aspect ratio."""
    h, w = image.shape[:2]
    scale = min(max_w / w, max_h / h, 1)  # scale down, but don't enlarge
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(image, (new_w, new_h))


def display_image(tab_frame):
    global img, display_img, img_tk
    if img is None:
        return

    display_img = resize_for_display(img)
    img_tk = ImageTk.PhotoImage(Image.fromarray(display_img))

    if not hasattr(tab_frame, "label"):
        tab_frame.label = tk.Label(tab_frame)
        tab_frame.label.pack()

    tab_frame.label.config(image=img_tk)
    tab_frame.label.image = img_tk


# ---------- File operations ----------
def open_image(tab_frame):
    global img
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if not file_path:
        return
    img = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
    display_image(tab_frame)


def save_image():
    global img
    if img is None:
        messagebox.showerror("Error", "No image to save.")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
    )
    if not filepath:
        return

    save_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filepath, save_img)
    messagebox.showinfo("Saved", f"Image saved at:\n{filepath}")


# ---------- Filters ----------
def apply_grayscale(tab_frame):
    global img
    if img is None: return
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    display_image(tab_frame)


def apply_blur(tab_frame):
    global img
    if img is None: return
    img = cv2.GaussianBlur(img, (7, 7), 0)
    display_image(tab_frame)


def apply_sharpen(tab_frame):
    global img
    if img is None: return
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    img = cv2.filter2D(img, -1, kernel)
    display_image(tab_frame)


def apply_edge(tab_frame):
    global img
    if img is None: return
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    img = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    display_image(tab_frame)


# ---------- Editor ----------
def adjust_brightness(tab_frame):
    global img
    if img is None: return
    img = cv2.convertScaleAbs(img, alpha=1, beta=50)
    display_image(tab_frame)


def adjust_contrast(tab_frame):
    global img
    if img is None: return
    img = cv2.convertScaleAbs(img, alpha=1.5, beta=0)
    display_image(tab_frame)


def rotate_image(tab_frame):
    global img
    if img is None: return
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), 90, 1)
    img = cv2.warpAffine(img, M, (w, h))
    display_image(tab_frame)


def resize_image(tab_frame):
    global img
    if img is None: return
    h, w = img.shape[:2]
    img = cv2.resize(img, (w//2, h//2))
    display_image(tab_frame)


# ---------- Webcam ----------
def start_webcam(tab_frame):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open webcam")
        return

    def show_frame():
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resized = resize_for_display(frame_rgb)
            frame_tk = ImageTk.PhotoImage(Image.fromarray(resized))
            tab_frame.label.imgtk = frame_tk
            tab_frame.label.config(image=frame_tk)
            tab_frame.label.after(10, show_frame)
        else:
            cap.release()

    if not hasattr(tab_frame, "label"):
        tab_frame.label = tk.Label(tab_frame)
        tab_frame.label.pack()

    show_frame()


# ---------- Main App ----------
def main():
    root = tk.Tk()
    root.title("Vision Studio")
    root.geometry("900x600")


    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)


    # Tabs
    filters_tab = ttk.Frame(notebook)
    editor_tab = ttk.Frame(notebook)
    webcam_tab = ttk.Frame(notebook)


    notebook.add(filters_tab, text="Filters")
    notebook.add(editor_tab, text="Editor")
    notebook.add(webcam_tab, text="Webcam")


    # Filters Tab
    tk.Button(filters_tab, text="Open Image", bg=FILTER_BTN_COLOR,
              command=lambda: open_image(filters_tab)).pack(pady=5)
    tk.Button(filters_tab, text="Grayscale", bg=FILTER_BTN_COLOR,
              command=lambda: apply_grayscale(filters_tab)).pack(pady=5)
    tk.Button(filters_tab, text="Blur", bg=FILTER_BTN_COLOR,
              command=lambda: apply_blur(filters_tab)).pack(pady=5)
    tk.Button(filters_tab, text="Sharpen", bg=FILTER_BTN_COLOR,
              command=lambda: apply_sharpen(filters_tab)).pack(pady=5)
    tk.Button(filters_tab, text="Edge Detection", bg=FILTER_BTN_COLOR,
              command=lambda: apply_edge(filters_tab)).pack(pady=5)
    tk.Button(filters_tab, text="Save Image", bg=FILTER_BTN_COLOR,
              command=save_image).pack(pady=5)


    # Editor Tab
    tk.Button(editor_tab, text="Open Image", bg=EDITOR_BTN_COLOR,
              command=lambda: open_image(editor_tab)).pack(pady=5)
    tk.Button(editor_tab, text="Brightness", bg=EDITOR_BTN_COLOR,
              command=lambda: adjust_brightness(editor_tab)).pack(pady=5)
    tk.Button(editor_tab, text="Contrast", bg=EDITOR_BTN_COLOR,
              command=lambda: adjust_contrast(editor_tab)).pack(pady=5)
    tk.Button(editor_tab, text="Rotate", bg=EDITOR_BTN_COLOR,
              command=lambda: rotate_image(editor_tab)).pack(pady=5)
    tk.Button(editor_tab, text="Resize", bg=EDITOR_BTN_COLOR,
              command=lambda: resize_image(editor_tab)).pack(pady=5)
    tk.Button(editor_tab, text="Save Image", bg=EDITOR_BTN_COLOR,
              command=save_image).pack(pady=5)


    # Webcam Tab
    tk.Button(webcam_tab, text="Start Webcam", bg=WEBCAM_BTN_COLOR,
              command=lambda: start_webcam(webcam_tab)).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
