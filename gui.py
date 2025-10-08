# ===================================================================
# FILE: gui.py (FIXED VERSION with Scrollable Control Panel)
# ===================================================================
# Enhanced GUI with scrollable left panel to ensure all controls are visible

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from FictionalStory_AI.story_generator import StoryGenerator
from FictionalStory_AI.story_templates import GENRES, THEMES
import threading

class StoryGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Story Generator")
        self.root.geometry("1100x800")
        self.root.configure(bg="#f0f0f0")
        
        self.generator = StoryGenerator()
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill="x")
        
        title_label = tk.Label(
            header_frame,
            text="🤖 AI-Powered Story Generator",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Controls with Canvas for scrolling
        left_container = tk.Frame(main_frame, bg="#f0f0f0", width=350)
        left_container.pack(side="left", fill="y", padx=(0, 10))
        left_container.pack_propagate(False)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(left_container, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_container, orient="vertical", command=canvas.yview)
        
        # Create frame inside canvas
        control_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        canvas_window = canvas.create_window((0, 0), window=control_frame, anchor="nw")
        
        # Update scroll region when frame size changes
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Update canvas window width to match canvas width
            canvas.itemconfig(canvas_window, width=event.width)
        
        control_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Story Settings Frame
        settings_frame = tk.LabelFrame(
            control_frame,
            text="Story Settings",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15
        )
        settings_frame.pack(fill="x", pady=(0, 10))
        
        # AI Provider selection
        tk.Label(
            settings_frame,
            text="AI Provider:",
            font=("Arial", 10, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", pady=(0, 5))
        
        self.provider_var = tk.StringVar(value="openai")
        provider_frame = tk.Frame(settings_frame, bg="#ffffff")
        provider_frame.pack(fill="x", pady=(0, 15))
        
        tk.Radiobutton(
            provider_frame, text="OpenAI", variable=self.provider_var,
            value="openai", bg="#ffffff"
        ).pack(anchor="w")
        tk.Radiobutton(
            provider_frame, text="Anthropic", variable=self.provider_var,
            value="anthropic", bg="#ffffff"
        ).pack(anchor="w")
        tk.Radiobutton(
            provider_frame, text="Google", variable=self.provider_var,
            value="google", bg="#ffffff"
        ).pack(anchor="w")
        tk.Radiobutton(
            provider_frame, text="Demo Mode", variable=self.provider_var,
            value="local", bg="#ffffff"
        ).pack(anchor="w")
        
        # Genre
        tk.Label(
            settings_frame,
            text="Genre:",
            font=("Arial", 10, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", pady=(0, 5))
        
        self.genre_var = tk.StringVar(value="Fantasy")
        genre_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.genre_var,
            values=list(GENRES.keys()),
            state="readonly",
            width=25
        )
        genre_combo.pack(pady=(0, 15))
        
        # Theme
        tk.Label(
            settings_frame,
            text="Theme:",
            font=("Arial", 10, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", pady=(0, 5))
        
        self.theme_var = tk.StringVar(value="Adventure")
        theme_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.theme_var,
            values=list(THEMES.keys()),
            state="readonly",
            width=25
        )
        theme_combo.pack(pady=(0, 15))
        
        # Character name
        tk.Label(
            settings_frame,
            text="Main Character:",
            font=("Arial", 10, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", pady=(0, 5))
        
        self.character_entry = tk.Entry(settings_frame, width=28, font=("Arial", 10))
        self.character_entry.pack(pady=(0, 15))
        
        # Setting
        tk.Label(
            settings_frame,
            text="Setting/Location:",
            font=("Arial", 10, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", pady=(0, 5))
        
        self.setting_entry = tk.Entry(settings_frame, width=28, font=("Arial", 10))
        self.setting_entry.pack(pady=(0, 15))
        
        # Story length
        tk.Label(
            settings_frame,
            text="Story Length:",
            font=("Arial", 10, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", pady=(0, 5))
        
        self.length_var = tk.StringVar(value="Medium")
        length_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.length_var,
            values=["Short", "Medium", "Long"],
            state="readonly",
            width=25
        )
        length_combo.pack(pady=(0, 10))
        
        # Custom Beginning Frame
        beginning_frame = tk.LabelFrame(
            control_frame,
            text="Story Beginning Options",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15
        )
        beginning_frame.pack(fill="x", pady=(0, 10))
        
        # Beginning mode selection
        self.beginning_mode = tk.StringVar(value="auto")
        
        tk.Radiobutton(
            beginning_frame,
            text="Auto-generate opening",
            variable=self.beginning_mode,
            value="auto",
            bg="#ffffff",
            command=self.toggle_custom_beginning
        ).pack(anchor="w", pady=5)
        
        tk.Radiobutton(
            beginning_frame,
            text="Continue from my beginning",
            variable=self.beginning_mode,
            value="continue",
            bg="#ffffff",
            command=self.toggle_custom_beginning
        ).pack(anchor="w", pady=5)
        
        tk.Radiobutton(
            beginning_frame,
            text="Analyze & match my style",
            variable=self.beginning_mode,
            value="analyze",
            bg="#ffffff",
            command=self.toggle_custom_beginning
        ).pack(anchor="w", pady=5)
        
        # Custom beginning text area
        tk.Label(
            beginning_frame,
            text="Your story beginning:",
            font=("Arial", 9, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", pady=(10, 5))
        
        self.custom_beginning_text = scrolledtext.ScrolledText(
            beginning_frame,
            wrap="word",
            height=6,
            font=("Arial", 9),
            state="disabled"
        )
        self.custom_beginning_text.pack(fill="both", expand=True)
        
        # Buttons Frame
        button_frame = tk.Frame(control_frame, bg="#f0f0f0")
        button_frame.pack(fill="x", pady=(10, 0))
        
        self.generate_btn = tk.Button(
            button_frame,
            text="Generate Story",
            command=self.generate_story_threaded,
            bg="#3498db",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )
        self.generate_btn.pack(fill="x", pady=(0, 10))
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_all,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8
        )
        clear_btn.pack(fill="x")
        
        # Right panel - Story display
        story_frame = tk.LabelFrame(
            main_frame,
            text="Generated Story",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15
        )
        story_frame.pack(side="right", fill="both", expand=True)
        
        self.story_text = scrolledtext.ScrolledText(
            story_frame,
            wrap="word",
            font=("Georgia", 11),
            bg="#fffef7",
            relief="flat",
            padx=10,
            pady=10
        )
        self.story_text.pack(fill="both", expand=True)
        
    def toggle_custom_beginning(self):
        """Enable/disable custom beginning text based on mode"""
        mode = self.beginning_mode.get()
        if mode == "auto":
            self.custom_beginning_text.config(state="disabled")
        else:
            self.custom_beginning_text.config(state="normal")
    
    def generate_story_threaded(self):
        """Generate story in separate thread to prevent UI freezing"""
        thread = threading.Thread(target=self.generate_story)
        thread.daemon = True
        thread.start()
    
    def generate_story(self):
        """Generate story with AI"""
        # Disable button during generation
        self.generate_btn.config(state="disabled", text="Generating...")
        
        genre = self.genre_var.get()
        theme = self.theme_var.get()
        character = self.character_entry.get().strip()
        setting = self.setting_entry.get().strip()
        length = self.length_var.get()
        mode = self.beginning_mode.get()
        provider = self.provider_var.get()
        
        if not character:
            messagebox.showwarning("Missing Input", "Please enter a character name!")
            self.generate_btn.config(state="normal", text="Generate Story")
            return
        
        if not setting:
            messagebox.showwarning("Missing Input", "Please enter a setting!")
            self.generate_btn.config(state="normal", text="Generate Story")
            return
        
        custom_beginning = self.custom_beginning_text.get(1.0, tk.END).strip()
        
        if mode != "auto" and not custom_beginning:
            messagebox.showwarning(
                "Missing Beginning",
                "Please enter your story beginning or select 'Auto-generate opening'!"
            )
            self.generate_btn.config(state="normal", text="Generate Story")
            return
        
        self.story_text.delete(1.0, tk.END)
        self.story_text.insert(tk.END, "🤖 AI is crafting your story...\n\nThis may take 10-30 seconds depending on the AI provider and story length.\n\nPlease wait...")
        self.root.update()
        
        # Update generator with selected provider
        self.generator = StoryGenerator(provider)
        
        try:
            story = self.generator.generate_story_with_custom_beginning(
                custom_beginning=custom_beginning,
                genre=genre,
                theme=theme,
                character=character,
                setting=setting,
                length=length,
                continuation_mode=mode
            )
            
            self.story_text.delete(1.0, tk.END)
            
            # If continuing from custom beginning, show it first
            if mode != "auto" and custom_beginning:
                self.story_text.insert(tk.END, "[YOUR BEGINNING]\n", "header")
                self.story_text.insert(tk.END, custom_beginning + "\n\n")
                self.story_text.insert(tk.END, "[AI CONTINUATION]\n", "header")
            
            self.story_text.insert(tk.END, story)
            
            # Configure tags for styling
            self.story_text.tag_config("header", font=("Arial", 10, "bold"), foreground="#2c3e50")
            
        except Exception as e:
            self.story_text.delete(1.0, tk.END)
            self.story_text.insert(tk.END, f"Error: {str(e)}\n\nPlease check your API configuration in config.py")
        
        finally:
            self.generate_btn.config(state="normal", text="Generate Story")
    
    def clear_all(self):
        """Clear all fields"""
        self.story_text.delete(1.0, tk.END)
        self.custom_beginning_text.delete(1.0, tk.END)
        self.character_entry.delete(0, tk.END)
        self.setting_entry.delete(0, tk.END)