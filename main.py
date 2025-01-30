import requests
from PIL import Image
import tkinter
from tkinter import messagebox
import os

BLACK = "#222831"
GREY = "#393E46"
LIGHT_BLUE = "#00ADB5"
WHITE = "#EEEEEE"

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data

poke_img = None

def poke_search():   
    pokemon_name = search_entry.get()

    if len(pokemon_name) == 0:
        messagebox.showwarning(title="Oops", message="Search field is empty!")
    else:    
        pokemon_info = get_pokemon_info(pokemon_name)
        try:
            img_url = pokemon_info["sprites"]["other"]["home"]["front_default"]
            img = Image.open(requests.get(img_url, stream=True).raw)
            resize_img = img.resize((300, 300))
            resize_img.save(f"{pokemon_info["name"]}_img.png") 
            poke_name = pokemon_info["name"]
            poke_id = pokemon_info["id"]
            poke_height = pokemon_info["height"]
            poke_weight = pokemon_info["weight"]

            canvas.itemconfig(welcome_text, text="")
            canvas.itemconfig(pookie_text, text="")
            canvas.config(width=300, height=300, background=BLACK, highlightthickness=0)
            global poke_img
            poke_img = tkinter.PhotoImage(file=rf"{pokemon_info["name"]}_img.png")
            canvas.create_image(150, 150, image=poke_img)
            canvas.place(x=160, y=0)

            search_entry.place(x=190, y=320)
            search_button.place(x=380, y=318)

            label_canvas.config(background=LIGHT_BLUE)
            label_canvas.itemconfig(name_label, text=f"Name: {poke_name}")
            label_canvas.itemconfig(id_label, text=f"Id: {poke_id}")
            label_canvas.itemconfig(height_label, text=f"Height: {poke_height}")
            label_canvas.itemconfig(weight_label, text=f"Weight: {poke_weight}")

            os.remove(f"{pokemon_info["name"]}_img.png")
        except TypeError:
            messagebox.showwarning(title="Error!", message="Given Data Is Not Valid!")                     
#================================MAIN INTERFACE=================================================
window = tkinter.Tk()
window.title("Pookie Wiki")
window.geometry("500x400")
window.config(bg=BLACK, padx=20, pady=20)

label_canvas = tkinter.Canvas(width=160, height=200, background=BLACK, highlightthickness=0)
name_label = label_canvas.create_text(80, 50, text="",
                               font=("Segoe Print", 15, "bold"))

id_label = label_canvas.create_text(80, 80, text="",
                               font=("Segoe Print", 15, "bold"))

height_label = label_canvas.create_text(80, 110, text="",
                               font=("Segoe Print", 15, "bold"))

weight_label = label_canvas.create_text(80, 140, text="",
                               font=("Segoe Print", 15, "bold"))
label_canvas.place(x=0, y=70)

canvas = tkinter.Canvas(width=460, height=200, background=BLACK, highlightthickness=0)
welcome_text = canvas.create_text(230, 150,
                                 text="WELCOME",
                                 font=("Fixedsys", 50, "bold"),
                                 fill=WHITE)
pookie_text = canvas.create_text(160, 190,
                                 text="TO POOKIE WIKI",
                                 font=("Fixedsys", 15, "bold"),
                                 fill=WHITE)
canvas.place(x=0, y=0)

search_entry = tkinter.Entry(window,
                            width=20,
                            background=GREY,
                            highlightbackground=GREY,
                            highlightthickness=2,
                            highlightcolor=GREY,
                            fg="YELLOW",
                            font=("Fixedsys", 16, "bold"))
search_entry.place(x=90, y=220)

search_button = tkinter.Button(window,
                               background=LIGHT_BLUE,
                               foreground=BLACK,
                               highlightthickness=2,
                               highlightbackground=LIGHT_BLUE,
                               highlightcolor=WHITE,
                               width=8,
                               height=1,
                               border=0,
                               text="Search",
                               font=("Fixedsys", 16, "bold"),
                               command=poke_search)
search_button.place(x=280, y=219)


window.mainloop()
