import cv2
import numpy as np
from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

class VisionStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Vision Studio")
        self.root.geometry("900x600")
        self.root.configure(bg="#2e2e2e")
        
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#2e2e2e",borderwidth=0)
        style.configure("TNotebook.Tab", background="#444",foreground="white",padding=[10,5])
        style.map("TNOtebook.Tab",background=[("selected","#1f6aa5")])
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=BOTH, expand=True,padx=5,pady=5)
        
        # Tabs
        self.filters_tab = Frame(self.notebook,bg="#2e2e2e")
        self.editor_tab = Frame(self.notebook,bg="#2e2e2e")
        self.webcam_tab = Frame(self.notebook,bg="#2e2e2e")
        
        
        self.notebook.add(self.filters_tab,text="🖼️ Filters")
        self.notebook.add(self.editor_tab,text="🎨 Editor")
        self.notebook.add(self.webcam_tab,text="📸 Webcam")
        
        
        # Init modules
        self.init_filters_tab()
        self.init_editor_tab()
        self.init_webcam_tab()
        
     #-----------FILTERS TAB ---------
    def init_filters_tab(self):
        Label(self.filters_tab, text="Image Filters",font=("Arial",16), bg="#2e2e2e",fg="white").pack(pady=10)
        btn_frame = Frame(self.filters_tab,bg="#2e2e2e")
        btn_frame.pack(pady=5)
            
            
        Button(btn_frame, text="Open Image",command=self.open_image).grid(row=0,column=0,padx=5)
            
        Button(btn_frame,text="Grayscale",command=self.apply_grayscale).grid(row=0,column=1,padx=5)
        Button(btn_frame,text="Blur",command=self.apply_blur).grid(row=0,column=2,padx=5)
        Button(btn_frame,text="Sharpen",command=self.apply_sharpen).grid(row=0,column=3,padx=5)
        Button(btn_frame,text="Edge Detect",command=self.apply_edges).grid(row=0,column=4,padx=5)
        
        
        self.filter_canvas = Label(self.filters_tab,bg="black")
        self.filter_canvas.pack(pady=10)
    
    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files","*.jpg *.png *.jpeg")])
        if path:
            self.img = cv2.imread(path)
            self.display_image(self.img,self.filter_canvas)
            
    def apply_grayscale(self):
        if hasattr(self,'img'):
            gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
            self.display_image(gray,self.filter_canvas)
            
    def apply_blur(self):
        if hasattr(self,"img"):
            blur = cv2.GaussianBlur(self.img)
            self.display_image(blur, self.filter_canvas)
            
    def apply_sharpen(self):
        if hasattr(self,'img'):
            kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
            sharp = cv2.filter2D(self.img, -1, kernel)
            self.display_image(sharp,self.filter_canvas)
            
    def apply_edges(self):
        if hasattr(self,'img'):
            edges = cv2.Canny(self.img,100, 200)
            self.display_image(edges,self.filter_canvas)
            
    
    # -----------EDITOR TAB ------------------
    def init_editor_tab(self):
        Label(self.editor_tab,text="Image Editor",font=("Arial",16),bg="#2e2e2e",fg="white").pack(pady=10)
        btn_frame = Frame(self.editor_tab,bg="#2e2e2e")
        btn_frame.pack(pady=5)
        
        
        Button(btn_frame,text="Open Image",command=self.open_editor_image).grid(row=0,column=0,padx=5)
        Button(btn_frame,text="Brightness +",command=lambda:self.adjust_brightness(30)).grid(row=0,column=1,padx=5)
        Button(btn_frame,text="Brightness -",command=lambda:self.adjust_brightness(-30)).grid(row=0,column=2,padx=5)
        Button(btn_frame,text="Contrast +",command=lambda:self.adjust_contrast(1.3)).grid(row=0,column=3,padx=5)
        Button(btn_frame,text="Contrast -",comman=lambda:self.adjust_contrast(0.7)).grid(row=0,column=4,padx=5)
        Button(btn_frame,text="Rotate 90 degrees",command=lambda:self.rotate_image).grid(row=0,column=5,padx=5)
        Button(btn_frame,text="Resize 50%",command=self.resize_image).grid(row=0,column=6,padx=5)
        
        self.editor_canvas = Label(self.editor_tab,bg="black")
        self.editor_canvas.pack(pady=10)
        
    def open_editor_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files","*.jpg *.png *.jpeg")])
        if path:
            self.edit_img = cv2.imread(path)
            self.display_image(self.edit_img, self.editor_canvas)
            
    def adjust_brightness(self,value):
        if hasattr(self,'edit_img'):
            hsv = cv2.cvtColor(self.edit_img,cv2.COLOR_BGRHSV)
            h,s,v = cv2.split(hsv)
            v = np.clip(v + value,0,255)
            final = cv2.merge((h ,s ,v))
            self.edit_img = cv2.cvtColor(final,cv2.COLOR_HSVBGR)
            self.display_image(self.edit_img, self.editor_canvas)
            
    def adjust_contrast(self,factor):
        if hasattr(self,'edit_img'):
            self.edit_img = cv2.convertScaleAbs(self.edit_img, alpha=factor,beta=0)
            self.display_image(self.edit_img, self.editor_canvas)
            
    def rotate_image(self):
        if hasattr(self,'edit_img'):
            self.edit_img = cv2.rotate(self.edit_img,cv2.ROTATE_90_CLOCKWISE)
            self.display_image(self.edit_img, self.editor_canvas)
        
    def resize_image(self):
        if hasattr(self,'edit_img'):
            h, w = self.edit_img.shape[:2]
            self.edit_img = cv2.resize(self.edit_img,(w//2,h//2))
            self.display_image(self.edit_img,self.editor_canvas)
            
            
    # ----------- WEBCAM -----------------
    def init_webcam_tab(self):
        Label(self.webcam_tab,text="Webcam Fun",font=("Arial",16),bg="#2e2e2e",fg="white").pack(pady=10)
        btn_frame = Frame(self.webcam_tab,bg="#2e2e2e")
        btn_frame.pack(pady=5)
        
        Button(btn_frame,text="Start Webcam",command=self.start_webcam).grid(row=0,column=0,padx=5)
        Button(btn_frame,text="Stop Webcam",comman=self.stop_webcam).grid(row=0,column=1,padx=5)
        
        self.webcam_canvas = Label(self.webcam_tab,bg="black")
        self.webcam_canvas.pack(pady=10)
        
        self.cap = None
        
    def start_webcam(self):
        self.cap = cv2.VideoCapture(0)
        self.update_webcam()
        
    def stop_webcam(self):
        if self.cap:
            self.cap.release()
        self.cap = None
        
    def update_webcam(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.display_image(frame,self.webcam_canvas)
            self.webcam_canvas.after(30, self.update_webcam)
    
    
    # ---------------HELPER -------------------
    def display_image(self,img,canvas_label):
        if len(img.shape) == 2:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img)
            img_pil = img_pil.resize((500,400))
            imgtk = ImageTk.PhotoImage(image=img_pil)
            canvas_label.config(image=imgtk)
            canvas_label.image = imgtk
            
            
if __name__ == "__main__":
    root = Tk()
    app = VisionStudio(root)
    root.mainloop()
            