import tkinter as tk
import json
import hashlib
from gtts import gTTS
import os
import winsound

class Constants():
    class Colors():
        accent = "#cc5252"
        accentFocused = "#a13d3d"

        bgPrimary = "#242424"
        bgSecondary = "#2B2B2B"
        bgTertiary = "#333333"

        text = "#e3e3e3"

    class Geometry():
        width = 400
        height = 470
        geometry = f"{width}x{height}"

    class Meta():
        version = 1.0
        title = "InstantSpeak"
        fullName = f"{title} {version}"

        # Configuration
        ttsLanguage = "en"
        try:
            with open("config.json") as c:
                config = json.load(c)
                ttsLanguage = config["language"]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            config = json.dumps({"language": ttsLanguage}, indent=4)
            with open("config.json", "w") as c:
                c.write(config)

        # Directories
        rootPath = os.path.dirname(os.path.realpath(__file__))
        tempDirectory = "tmp"
        if not os.path.exists(os.path.join(rootPath, tempDirectory)):
            os.makedirs(os.path.join(rootPath, tempDirectory))
    
    class Assets():
        assetDirectory = "assets/"
        icon = assetDirectory + "icon.png"
        favicon = assetDirectory + "favicon.ico"


class Button(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.c = Constants()

        self["bg"] = self.c.Colors.accent
        self["activebackground"] = self.c.Colors.accentFocused
        self["activeforeground"], self["fg"] = self.c.Colors.text, self.c.Colors.text
        self["padx"] = "7px"
        self["pady"] = "5px"
        self["bd"] = 0
        self["relief"] = tk.SUNKEN


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.c = Constants()

        # Variables
        self.ttsHash = None

        # Root properties
        self.title(self.c.Meta.fullName)
        self.geometry(self.c.Geometry.geometry)
        self.iconbitmap(self.c.Assets.favicon)
        self.configure(bg=self.c.Colors.bgPrimary)
        self.resizable(False, False)

        # Main container
        self.mainContainer = tk.Frame(self, padx="10px", bg=self.c.Colors.bgPrimary)

        # Widgets
        self.ttsInput = tk.Text(
            self.mainContainer,
            bg=self.c.Colors.bgTertiary,
            fg=self.c.Colors.text,
            borderwidth=0,
            relief=tk.GROOVE,
            pady="5px",
            padx="5px"
        )
        self.ttsInput.pack_propagate(0)

        # Packs
        self.mainContainer.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)
        self.ttsInput.pack(fill=tk.X, anchor=tk.N, side=tk.TOP, pady="10px")
        self.processBtn = Button(self.mainContainer, text="Process text", command=self.processText).pack(pady=(0, 10))

    def processText(self):
        text = "sheesh".encode("utf-8") #self.ttsInput.get(1.0, "end-1c").encode("UTF-8")
        hash = hashlib.sha256(text).hexdigest()
        audioPath = os.path.join(self.c.Meta.rootPath, self.c.Meta.tempDirectory, f"{hash}.wav")
        print(audioPath)
        if self.ttsHash != hash:
            try:
                tts = gTTS(text=text, lang=self.c.Meta.ttsLanguage)
                tts.save(f"{hash}.wav")
                self.ttsHash = hash

                if self.ttsHash:
                    os.remove(os.path.join(self.c.Meta.rootPath, self.c.Meta.tempDirectory, f"{self.ttsHash}.wav"))
            except AssertionError:
                return
        
        try:
            winsound.PlaySound(audioPath)
        except FileNotFoundError:
            tts = gTTS(text=text, lang=self.c.Meta.ttsLanguage)
            tts.save(audioPath)
            self.ttsHash = hash
            winsound.PlaySound(audioPath)

if __name__ == "__main__":
    app = App()
    app.mainloop()