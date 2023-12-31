import tkinter as tk

def read_and_get_first_line(filepath):
    with open(filepath, "r+") as file:
        #Reads the first line and removes spaces and line breaks
        first_line = file.readline().strip()  
        #Reads the remaining contents of the file after the first line
        remaining_content = file.read()  
        #Sets the file pointer to the beginning of the file
        file.seek(0)  
        #Writes the remaining content back to the file
        file.write(remaining_content)  
        #Shortens the file to the current position
        file.truncate()  
    return first_line

def read_and_get_second_line(filepath):
        with open(filepath, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                second_line = lines[1]
                return second_line
            else:
                second_line = ""
                return second_line 

#Checks if the text file is empty
def is_file_empty(filepath):
    with open(filepath, "r") as file:
        content = file.read()
        return not content.strip()

#Deletes the first line
def delete_first_line(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()

    with open(filepath, "w") as file:
        file.writelines(lines[0:])

#Deletes the second line
def delete_second_line(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()

    with open(filepath, "w") as file:
        file.writelines(lines[:1] + lines[2:])
#For GUI, searches for keywords to assign to labels
def update_labels():
    first_line = read_and_get_first_line(filepath)

    if is_file_empty(filepath):
        year_label.config(text="Game Over")
        temperature_label.config(text="")
    else:
        if first_line.startswith("/year/"):
            year = first_line.lstrip("/year/")
            year_label.config(text=f"{year}")
        elif first_line.startswith("/temperature/"):
            temperature = first_line.lstrip("/temperature/")
            temperature = float(temperature)
            temperature_label.config(text="" + f"Aktuelle Erderwärmung: {temperature:.2f}°C")  
        elif first_line.startswith("/catastrophe/"):
            catastrophe = first_line.lstrip("/catastrophe/")
            headlines.insert(0, catastrophe)
            #headline_list_text.image_create(tk.END, image=image)
        elif first_line.startswith("/headline/"):
            headline = first_line.lstrip("/headline/")
            headlines.insert(0, headline)
        else:
            first_line = ""
        delete_first_line(filepath)

        headlines_to_display = headlines[:15]
        headlines_text = "\n\n\n\n".join(headlines_to_display)
        #headline_list_label.config(text=headlines_text)
    
        #Insert the headlines text into the headline_list_text
        headline_list_text.delete(1.0, tk.END)  
        #Bild einfügen
        headline_list_text.image_create(tk.END, image=image)
        headline_list_text.insert(tk.END, headlines_text)

    #updatet Labels
    window.after(500, update_labels)

filepath = 'newsfeed/news.txt'

window = tk.Tk()
window.configure(bg='#DFE9F6')

#Newsfeed according to screensize
screen_width = window.winfo_screenwidth() 
screen_height = window.winfo_screenheight()

window_width = screen_width // 2
news_wrap = screen_width // 1.5
titel_size = screen_width // 40
text_size = screen_width // 80
news_size = screen_width // 100

window.geometry(f"{window_width}x{screen_height}")

#MainFrame
frame = tk.Frame(window, bg='#DFE9F6',pady=24, padx=32)
frame.pack(fill=tk.BOTH, expand=True)

#Header
header = tk.Frame(frame, bg=window.cget("bg")) 
header.pack(fill=tk.X)

#Newsframe
newsframe = tk.Frame(window, bg=window.cget("bg"), pady=24, padx=24)
newsframe.pack(fill=tk.BOTH)

#Postframe
postframe =tk.Frame(newsframe,bg='#FFFFFF', padx=24)
postframe.pack(side=tk.LEFT, anchor='n')

#Darstellung im Header
year_label = tk.Label(header, text="2025", font=("Inter", titel_size),  fg="#262626", bg=window.cget("bg"))
year_label.pack(side=tk.LEFT)

#Image for header
image = tk.PhotoImage(file="./assets/Sorting.png")  
resized_image = image.subsample(2, 2)  
image_label = tk.Label(header, image=resized_image, bg=window.cget("bg"))  
image_label.pack(side=tk.RIGHT)

temperature_label = tk.Label(frame, text="Aktuelle Erderwärmung: 1.00°C", font=("Inter", text_size), fg="#262626", bg=window.cget("bg"))
temperature_label.pack(fill=tk.Y, side=tk.TOP, anchor='w')

#TODO: HEadlines ganz oben zuerst anzeigen lassen
#Label for the list of headlines
headline_list_label = tk.Label(newsframe, text="Dein Newsfeed", width=screen_width, font=("Inter", text_size), fg="#262626", wraplength=news_wrap,  bg=window.cget("bg"))
headline_list_label.pack(fill=tk.Y, side=tk.TOP)


headline_list_text = tk.Text(newsframe, width=screen_width, pady=12, padx=24, font=("Inter", news_size), wrap=tk.WORD)
headline_list_text.pack(fill=tk.Y, side=tk.TOP)           
#Initialize the headlines array
headlines = []

image = tk.PhotoImage("./assets/Sorting.gif")

update_labels()
window.mainloop()