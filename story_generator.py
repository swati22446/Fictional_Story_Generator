from ai_engine import AIStoryEngine
from story_templates import GENRES, THEMES

class StoryGenerator:
    def __init__(self, ai_provider: str = "openai"):
        self.ai_engine = AIStoryEngine(ai_provider)
        self.stories_generated = 0
        
    def generate_story_with_custom_beginning(
        self, 
        custom_beginning: str,
        genre: str,
        theme: str,
        character: str,
        setting: str,
        length: str,
        continuation_mode: str = "continue"
    ) -> str:
        """
        Generate story with custom beginning
        continuation_mode: 'continue', 'analyze', or 'auto'
        """
        
        word_count = {"Short": 500, "Medium": 1000, "Long": 1500}[length]
        
        if continuation_mode == "auto":
            # Auto-generate beginning, then continue
            prompt = self._build_auto_prompt(genre, theme, character, setting, word_count)
        elif continuation_mode == "continue":
            # Continue directly from user's beginning
            prompt = self._build_continuation_prompt(
                custom_beginning, genre, theme, character, setting, word_count
            )
        elif continuation_mode == "analyze":
            # Analyze style and continue matching it
            prompt = self._build_analysis_prompt(
                custom_beginning, genre, theme, character, setting, word_count
            )
        else:
            prompt = self._build_auto_prompt(genre, theme, character, setting, word_count)
        
        story = self.ai_engine.generate_story(prompt)
        self.stories_generated += 1
        
        return story
    
    def _build_auto_prompt(self, genre: str, theme: str, character: str, setting: str, word_count: int) -> str:
        """Build prompt for auto-generated story"""
        genre_info = GENRES.get(genre, {})
        theme_info = THEMES.get(theme, {})
        
        prompt = f"""Write a {word_count}-word {genre} story with a {theme} theme.

Story Requirements:
- Main character: {character}
- Setting: {setting}
- Genre elements: {', '.join(genre_info.get('elements', []))}
- Theme focus: {', '.join(theme_info.get('elements', []))}
- Include: compelling opening, rising action, climax, and satisfying resolution

Create an engaging, well-structured story with vivid descriptions and emotional depth."""
        
        return prompt
    
    def _build_continuation_prompt(
        self, beginning: str, genre: str, theme: str, character: str, setting: str, word_count: int
    ) -> str:
        """Build prompt to continue from user's beginning"""
        prompt = f"""Continue this story in the {genre} genre with a {theme} theme:

STORY BEGINNING:
{beginning}

Continue the story featuring {character} in {setting}. Write approximately {word_count} words.

Include:
- Natural continuation from the provided beginning
- Rising action with engaging plot developments
- A compelling climax
- A satisfying resolution

Maintain consistency with the established tone and style."""
        
        return prompt
    
    def _build_analysis_prompt(
        self, beginning: str, genre: str, theme: str, character: str, setting: str, word_count: int
    ) -> str:
        """Build prompt to analyze style and continue"""
        prompt = f"""Analyze the writing style, tone, and narrative voice of this story beginning, then continue it seamlessly:

STORY BEGINNING:
{beginning}

Task:
1. Match the writing style, tone, and pacing of the beginning
2. Continue the story in {genre} genre with {theme} theme
3. Feature {character} in {setting}
4. Write approximately {word_count} words total (including the beginning)
5. Include rising action, climax, and resolution

Create a cohesive story that feels like it was written by the same author throughout."""
        
        return prompt

