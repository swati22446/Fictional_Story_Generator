# ===================================================================
# FILE: gui.py (PlotPilot - Stylish Modern UI with LARGE Subtitle)
# ===================================================================

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
from story_generator import StoryGenerator
from story_templates import GENRES, THEMES
import threading

class RoundedButton(tk.Canvas):
    """Custom button with rounded corners"""
    def __init__(self, parent, text, command, bg_color, fg_color="white", hover_color=None, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color or bg_color
        
        self.config(bg=parent.cget('bg'), highlightthickness=0, relief='flat')
        
        # Create rounded rectangle
        self.rect = self.create_rounded_rect(0, 0, 300, 50, radius=12, fill=bg_color, outline="")
        self.text = self.create_text(150, 25, text=text, fill=fg_color, 
                                     font=("Segoe UI", 12, "bold"))
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_click(self, event):
        self.command()
    
    def on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)
        self.config(cursor="hand2")
    
    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)
        self.config(cursor="")
    
    def set_text(self, text):
        self.itemconfig(self.text, text=text)
    
    def set_state(self, state):
        if state == "disabled":
            self.itemconfig(self.rect, fill="#94a3b8")
            self.unbind("<Button-1>")
        else:
            self.itemconfig(self.rect, fill=self.bg_color)
            self.bind("<Button-1>", self.on_click)

class StoryGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PlotPilot - AI Story Generator")
        self.root.geometry("1200x850")
        
        # Modern, crisp color palette
        self.bg_color = "#f8fafc"
        self.card_bg = "#ffffff"
        self.primary_color = "#6366f1"  # Bright Indigo
        self.primary_hover = "#4f46e5"
        self.secondary_color = "#a855f7"  # Bright Purple
        self.accent_color = "#ec4899"  # Bright Pink
        self.success_color = "#22c55e"  # Bright Green
        self.danger_color = "#ef4444"  # Bright Red
        self.danger_hover = "#dc2626"
        self.text_primary = "#1e293b"
        self.text_secondary = "#64748b"
        self.border_color = "#e2e8f0"
        
        self.root.configure(bg=self.bg_color)
        
        self.generator = StoryGenerator()
        self.setup_ui()
        
    def setup_ui(self):
        # Modern Header with solid color
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=150)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Title with stylish Jokerman font
        title_label = tk.Label(
            header_frame,
            text="✨ PlotPilot ✨",
            font=("Jokerman", 32, "bold"),
            bg=self.primary_color,
            fg="#ffffff"
        )
        title_label.pack(pady=(18, 3))
        
        # Small but clearly visible subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Your AI Co-Pilot for Epic Storytelling Adventures",
            font=("Comic Sans MS", 11, "bold"),
            bg=self.primary_color,
            fg="#ffed4e"  # Very bright yellow for high contrast
        )
        subtitle_label.pack(pady=(3, 18))
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Left panel - Controls with Canvas for scrolling
        left_container = tk.Frame(main_frame, bg=self.bg_color, width=380)
        left_container.pack(side="left", fill="y", padx=(0, 20))
        left_container.pack_propagate(False)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(left_container, bg=self.bg_color, highlightthickness=0, bd=0)
        
        # Modern scrollbar
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Modern.Vertical.TScrollbar",
                       background=self.primary_color,
                       troughcolor=self.bg_color,
                       bordercolor=self.bg_color,
                       arrowcolor="white",
                       relief="flat")
        
        scrollbar = ttk.Scrollbar(left_container, orient="vertical", command=canvas.yview, 
                                 style="Modern.Vertical.TScrollbar")
        
        # Create frame inside canvas
        control_frame = tk.Frame(canvas, bg=self.bg_color)
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        canvas_window = canvas.create_window((0, 0), window=control_frame, anchor="nw")
        
        # Update scroll region
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=event.width)
        
        control_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Modern Card for Settings
        settings_card = tk.Frame(
            control_frame,
            bg=self.card_bg,
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.border_color
        )
        settings_card.pack(fill="x", pady=(0, 20))
        
        # Card header
        settings_header = tk.Frame(settings_card, bg=self.primary_color, height=50)
        settings_header.pack(fill="x")
        settings_header.pack_propagate(False)
        
        tk.Label(
            settings_header,
            text="📚 Story Settings",
            font=("Segoe UI", 14, "bold"),
            bg=self.primary_color,
            fg="white"
        ).pack(side="left", padx=20, pady=12)
        
        # Card content
        settings_content = tk.Frame(settings_card, bg=self.card_bg)
        settings_content.pack(fill="x", padx=20, pady=20)
        
        # AI Provider
        tk.Label(
            settings_content,
            text="🤖 AI Provider",
            font=("Segoe UI", 11, "bold"),
            bg=self.card_bg,
            fg=self.text_primary
        ).pack(anchor="w", pady=(0, 8))
        
        self.provider_var = tk.StringVar(value="google")
        provider_frame = tk.Frame(settings_content, bg=self.card_bg)
        provider_frame.pack(fill="x", pady=(0, 18))
        
        providers = [
            ("OpenAI", "openai", "#10b981"),
            ("Anthropic", "anthropic", "#f59e0b"),
            ("Google", "google", "#3b82f6"),
            ("Demo Mode", "local", "#8b5cf6")
        ]
        
        for text, value, color in providers:
            rb = tk.Radiobutton(
                provider_frame,
                text=text,
                variable=self.provider_var,
                value=value,
                bg=self.card_bg,
                fg=color,
                font=("Segoe UI", 10, "bold"),
                activebackground=self.card_bg,
                selectcolor="#f1f5f9",
                bd=0,
                highlightthickness=0
            )
            rb.pack(anchor="w", pady=3)
        
        # Style the comboboxes
        style.configure("Modern.TCombobox",
                       fieldbackground=self.card_bg,
                       background=self.primary_color,
                       bordercolor=self.border_color,
                       arrowcolor=self.primary_color)
        
        # Genre
        tk.Label(
            settings_content,
            text="🎭 Genre",
            font=("Segoe UI", 11, "bold"),
            bg=self.card_bg,
            fg=self.text_primary
        ).pack(anchor="w", pady=(0, 8))
        
        self.genre_var = tk.StringVar(value="Fantasy")
        genre_combo = ttk.Combobox(
            settings_content,
            textvariable=self.genre_var,
            values=list(GENRES.keys()),
            state="readonly",
            width=30,
            font=("Segoe UI", 10),
            style="Modern.TCombobox"
        )
        genre_combo.pack(anchor="w", pady=(0, 18))
        
        # Theme
        tk.Label(
            settings_content,
            text="🌟 Theme",
            font=("Segoe UI", 11, "bold"),
            bg=self.card_bg,
            fg=self.text_primary
        ).pack(anchor="w", pady=(0, 8))
        
        self.theme_var = tk.StringVar(value="Adventure")
        theme_combo = ttk.Combobox(
            settings_content,
            textvariable=self.theme_var,
            values=list(THEMES.keys()),
            state="readonly",
            width=30,
            font=("Segoe UI", 10),
            style="Modern.TCombobox"
        )
        theme_combo.pack(anchor="w", pady=(0, 18))
        
        # Character
        tk.Label(
            settings_content,
            text="👤 Main Character",
            font=("Segoe UI", 11, "bold"),
            bg=self.card_bg,
            fg=self.text_primary
        ).pack(anchor="w", pady=(0, 8))
        
        char_frame = tk.Frame(settings_content, bg="white", bd=1, relief="solid")
        char_frame.pack(anchor="w", fill="x", pady=(0, 18))
        
        self.character_entry = tk.Entry(
            char_frame,
            font=("Segoe UI", 11),
            bd=0,
            bg="white",
            fg=self.text_primary,
            insertbackground=self.primary_color
        )
        self.character_entry.pack(fill="x", padx=12, pady=10)
        
        # Setting
        tk.Label(
            settings_content,
            text="🗺️ Setting/Location",
            font=("Segoe UI", 11, "bold"),
            bg=self.card_bg,
            fg=self.text_primary
        ).pack(anchor="w", pady=(0, 8))
        
        setting_frame = tk.Frame(settings_content, bg="white", bd=1, relief="solid")
        setting_frame.pack(anchor="w", fill="x", pady=(0, 18))
        
        self.setting_entry = tk.Entry(
            setting_frame,
            font=("Segoe UI", 11),
            bd=0,
            bg="white",
            fg=self.text_primary,
            insertbackground=self.primary_color
        )
        self.setting_entry.pack(fill="x", padx=12, pady=10)
        
        # Length
        tk.Label(
            settings_content,
            text="📏 Story Length",
            font=("Segoe UI", 11, "bold"),
            bg=self.card_bg,
            fg=self.text_primary
        ).pack(anchor="w", pady=(0, 8))
        
        self.length_var = tk.StringVar(value="Medium")
        length_combo = ttk.Combobox(
            settings_content,
            textvariable=self.length_var,
            values=["Short", "Medium", "Long"],
            state="readonly",
            width=30,
            font=("Segoe UI", 10),
            style="Modern.TCombobox"
        )
        length_combo.pack(anchor="w", pady=(0, 10))
        
        # Beginning Options Card
        beginning_card = tk.Frame(
            control_frame,
            bg=self.card_bg,
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.border_color
        )
        beginning_card.pack(fill="both", expand=True, pady=(0, 20))
        
        # Card header
        beginning_header = tk.Frame(beginning_card, bg=self.secondary_color, height=50)
        beginning_header.pack(fill="x")
        beginning_header.pack_propagate(False)
        
        tk.Label(
            beginning_header,
            text="✍️ Story Beginning Options",
            font=("Segoe UI", 14, "bold"),
            bg=self.secondary_color,
            fg="white"
        ).pack(side="left", padx=20, pady=12)
        
        # Card content
        beginning_content = tk.Frame(beginning_card, bg=self.card_bg)
        beginning_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.beginning_mode = tk.StringVar(value="auto")
        
        modes = [
            ("🎲 Auto-generate opening", "auto", self.success_color),
            ("📝 Continue from my beginning", "continue", "#f59e0b"),
            ("🎨 Analyze & match my style", "analyze", self.accent_color)
        ]
        
        for text, value, color in modes:
            rb = tk.Radiobutton(
                beginning_content,
                text=text,
                variable=self.beginning_mode,
                value=value,
                bg=self.card_bg,
                fg=color,
                font=("Segoe UI", 10, "bold"),
                activebackground=self.card_bg,
                selectcolor="#f1f5f9",
                command=self.toggle_custom_beginning,
                bd=0,
                highlightthickness=0
            )
            rb.pack(anchor="w", pady=4)
        
        tk.Label(
            beginning_content,
            text="Your story beginning:",
            font=("Segoe UI", 10, "bold"),
            bg=self.card_bg,
            fg=self.text_secondary
        ).pack(anchor="w", pady=(12, 8))
        
        text_frame = tk.Frame(beginning_content, bg="white", bd=1, relief="solid")
        text_frame.pack(fill="both", expand=True)
        
        self.custom_beginning_text = scrolledtext.ScrolledText(
            text_frame,
            wrap="word",
            height=6,
            font=("Segoe UI", 10),
            state="disabled",
            bd=0,
            bg="white",
            fg=self.text_primary,
            insertbackground=self.primary_color
        )
        self.custom_beginning_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Buttons
        button_frame = tk.Frame(control_frame, bg=self.bg_color)
        button_frame.pack(fill="x", pady=(10, 0))
        
        self.generate_btn = RoundedButton(
            button_frame,
            "✨ Generate Story",
            self.generate_story_threaded,
            bg_color=self.primary_color,
            hover_color=self.primary_hover,
            width=340,
            height=55
        )
        self.generate_btn.pack(pady=(0, 12))
        
        self.clear_btn = RoundedButton(
            button_frame,
            "🗑️ Clear All",
            self.clear_all,
            bg_color=self.danger_color,
            hover_color=self.danger_hover,
            width=340,
            height=50
        )
        self.clear_btn.pack()
        
        # Right panel - Story display
        story_card = tk.Frame(
            main_frame,
            bg=self.card_bg,
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.border_color
        )
        story_card.pack(side="right", fill="both", expand=True)
        
        # Story header
        story_header = tk.Frame(story_card, bg=self.accent_color, height=50)
        story_header.pack(fill="x")
        story_header.pack_propagate(False)
        
        tk.Label(
            story_header,
            text="📖 Generated Story",
            font=("Segoe UI", 14, "bold"),
            bg=self.accent_color,
            fg="white"
        ).pack(side="left", padx=20, pady=12)
        
        # Story content
        story_content_frame = tk.Frame(story_card, bg=self.card_bg)
        story_content_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.story_text = scrolledtext.ScrolledText(
            story_content_frame,
            wrap="word",
            font=("Georgia", 11),
            bg="#fffef9",
            fg=self.text_primary,
            relief="flat",
            padx=25,
            pady=25,
            bd=0,
            highlightthickness=0,
            insertbackground=self.primary_color
        )
        self.story_text.pack(fill="both", expand=True)
        
        # Welcome message
        welcome = """Welcome to PlotPilot! ✨

Your AI Co-Pilot for crafting extraordinary stories!

Here's how to create your masterpiece:

1. 🤖 Choose your AI provider (OpenAI, Anthropic, Google, or Demo Mode)
2. 🎭 Select a genre and theme that sparks your imagination
3. 👤 Name your main character
4. 🗺️ Set the location for your adventure
5. 📏 Pick your story length
6. ✍️ Choose how to begin your tale
7. ✨ Click "Generate Story" and watch the magic happen!

Ready to pilot your plot? Let's soar! 🚀"""
        
        self.story_text.insert("1.0", welcome)
        self.story_text.config(state="disabled")
        
    def toggle_custom_beginning(self):
        mode = self.beginning_mode.get()
        if mode == "auto":
            self.custom_beginning_text.config(state="disabled")
        else:
            self.custom_beginning_text.config(state="normal")
    
    def generate_story_threaded(self):
        thread = threading.Thread(target=self.generate_story)
        thread.daemon = True
        thread.start()
    
    def generate_story(self):
        self.generate_btn.set_state("disabled")
        self.generate_btn.set_text("⏳ Generating...")
        
        genre = self.genre_var.get()
        theme = self.theme_var.get()
        character = self.character_entry.get().strip()
        setting = self.setting_entry.get().strip()
        length = self.length_var.get()
        mode = self.beginning_mode.get()
        provider = self.provider_var.get()
        
        if not character:
            messagebox.showwarning("Missing Input", "Please enter a character name!")
            self.generate_btn.set_state("normal")
            self.generate_btn.set_text("✨ Generate Story")
            return
        
        if not setting:
            messagebox.showwarning("Missing Input", "Please enter a setting!")
            self.generate_btn.set_state("normal")
            self.generate_btn.set_text("✨ Generate Story")
            return
        
        custom_beginning = self.custom_beginning_text.get(1.0, tk.END).strip()
        
        if mode != "auto" and not custom_beginning:
            messagebox.showwarning(
                "Missing Beginning",
                "Please enter your story beginning or select 'Auto-generate opening'!"
            )
            self.generate_btn.set_state("normal")
            self.generate_btn.set_text("✨ Generate Story")
            return
        
        self.story_text.config(state="normal")
        self.story_text.delete(1.0, tk.END)
        self.story_text.insert(tk.END, "🤖 AI is crafting your story...\n\n✨ This may take 10-30 seconds\n\n⏳ Please wait...")
        self.story_text.config(state="disabled")
        self.root.update()
        
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
            
            self.story_text.config(state="normal")
            self.story_text.delete(1.0, tk.END)
            
            if mode != "auto" and custom_beginning:
                self.story_text.insert(tk.END, "[ YOUR BEGINNING ]\n", "header")
                self.story_text.insert(tk.END, custom_beginning + "\n\n")
                self.story_text.insert(tk.END, "[ AI CONTINUATION ]\n", "header")
            
            self.story_text.insert(tk.END, story)
            self.story_text.tag_config("header", font=("Segoe UI", 11, "bold"), 
                                      foreground=self.accent_color)
            self.story_text.config(state="disabled")
            
        except Exception as e:
            self.story_text.config(state="normal")
            self.story_text.delete(1.0, tk.END)
            self.story_text.insert(tk.END, f"❌ Error: {str(e)}\n\nPlease check your API configuration")
            self.story_text.config(state="disabled")
        
        finally:
            self.generate_btn.set_state("normal")
            self.generate_btn.set_text("✨ Generate Story")
    
    def clear_all(self):
        self.story_text.config(state="normal")
        self.story_text.delete(1.0, tk.END)
        self.story_text.config(state="disabled")
        self.custom_beginning_text.config(state="normal")
        self.custom_beginning_text.delete(1.0, tk.END)
        self.custom_beginning_text.config(state="disabled")
        self.character_entry.delete(0, tk.END)
        self.setting_entry.delete(0, tk.END)
        self.beginning_mode.set("auto")