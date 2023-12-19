from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
from urllib.request import urlopen
import time


def scrap():
    global urls,size
    urls = []
    email = email_input.get().strip()
    pass_word = pass_word_input.get().strip()
    txt = text.get("0.0","end").strip()
    size = int(combo_box.get()[:3])
    if email and pass_word and txt:
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            servise = Service(executable_path="chromedriver.exe")
            driver = webdriver.Chrome(service=servise)
            driver.get("https://www.bing.com/images/create?")

            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "create_btn_c")))
            join_btn = driver.find_element(By.ID, "create_btn_c")
            join_btn.click()
            time.sleep(3)

            WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.ID, "i0116")))
            userName = driver.find_element(By.ID, "i0116")
            userName.send_keys(email + Keys.ENTER)
            time.sleep(3)
            WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.ID, "i0118")))
            passWord = driver.find_element(By.ID, "i0118")
            passWord.send_keys(pass_word + Keys.ENTER)
            time.sleep(3)
            WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.ID, "idSIButton9")))
            yes = driver.find_element(By.ID, "idSIButton9")
            yes.click()

            WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.ID, "sb_form_q")))
            input = driver.find_element(By.ID, "sb_form_q")
            input.send_keys(txt + Keys.ENTER)

            WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "img_cont")))
            divs = driver.find_elements(By.CLASS_NAME, "img_cont")
            for div in divs:
                img = div.find_element(By.TAG_NAME, "img")
                src = img.get_attribute("src")
                urls.append(src)
            driver.quit()
            # win.quit()
            messagebox.showinfo(title="Artin Image Generator", message="Your image is generated. close this window to see them.")
        except:
            messagebox.showerror(title="Artin Image Generator", message="something went wrong")

    else:
        messagebox.showwarning(title="Artin Image Generator", message="Your image is generated. close this window to see them.")

win = ctk.CTk()
win.title("Artin Image Generator")
win.geometry("700x650")
win.minsize(100,580)
win.config(bg="#de1b89")
sizes = [
    "100px",
    "150px",
    "200px",
    "250px",
    "300px",
]

form = ctk.CTkFrame(master=win,width=500,height=480,bg_color="#de1b89", fg_color="blue", border_color="#232323", border_width=2)
form.pack(expand=True)
form.pack_propagate(False)

email_input = ctk.CTkEntry(master=form,border_color="#000",border_width=1, placeholder_text="email...", width=400, height=40, font=("None",16))
email_input.pack(pady=(40,0))

pass_word_input = ctk.CTkEntry(master=form,border_color="#000",border_width=1, placeholder_text="password...", width=400, height=40, font=("None",16), show="•")
pass_word_input.pack(pady=(40,0))

text = ctk.CTkTextbox(master=form,border_color="#000",border_width=1, width=400, height=80, font=("None",16))
text.pack(pady=(40,0))

combo_box = ctk.CTkComboBox(master=form, values=sizes,bg_color="#000", fg_color="#fff",corner_radius=6, width=400, height=35)
combo_box.pack(pady=(40,0))

btn = ctk.CTkButton(master=form, text="generate", corner_radius=7,border_color="#000", border_width=2,font=("None",20), fg_color="#00ffb3",hover_color="#de1b89", width=400, height=40,text_color="#000", command=scrap)
btn.pack(pady=(40,0))

# win.iconbitmap("github.ico")
win.mainloop()


root = ctk.CTk()
image_width, image_height = size, size
root.geometry(f"{image_width*2+100}x{image_height*2+100}")
root.resizable(0,0)
root.config(bg="#000")
row = 0
column = 0
count = 0

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

frm = ctk.CTkFrame(master=root, width=image_height*2, height=image_height*2, fg_color="#fff")
frm.pack(pady=image_height/6)
for url in urls:
    u = urlopen(url)
    raw_data = u.read()
    u.close()
    img = Image.open(BytesIO(raw_data))
    my_image = ctk.CTkImage(light_image=img, dark_image=img, size=(image_width,image_height))
    label = ctk.CTkLabel(master=frm,text="",image=my_image)

    label.grid(row=row, column=column, sticky="nsew", padx=5,pady=5)
    count += 1
    if count % 2 == 0:  # Check if count is even
        row += 1  # Move to the next row
        column = 0  # Reset column to 0 for the new row
    else:
        column += 1  # Move to the next column
root.mainloop()