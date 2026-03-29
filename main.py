"""
Hacker-Neo: Advanced AI Personal Assistant
Main entry point for the application
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer
import logging

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from gui.main_window import HackerNeoMainWindow
from core.ai_engine import AIEngine
from core.memory_system import MemorySystem
from utils.logger import setup_logger
from config import CONFIG

logger = setup_logger(__name__)

class HackerNeoApp:
    """Main application controller"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        
        # Initialize core components
        logger.info("Initializing Hacker-Neo...")
        self.memory_system = MemorySystem()
        self.ai_engine = AIEngine(self.memory_system)
        
        # Initialize GUI
        self.main_window = HackerNeoMainWindow(self.ai_engine, self.memory_system)
        
        # Connect signals
        self._connect_signals()
        
    def _connect_signals(self):
        """Connect application signals"""
        self.main_window.user_input_signal.connect(self.process_user_input)
        self.main_window.voice_input_signal.connect(self.process_voice_input)
        
    def process_user_input(self, text: str):
        """Process text input from user"""
        logger.info(f"User input: {text}")
        response = self.ai_engine.process_query(text)
        self.main_window.display_response(response)
        
    def process_voice_input(self, audio_data):
        """Process voice input from user"""
        logger.info("Processing voice input...")
        text = self.ai_engine.voice_to_text(audio_data)
        response = self.ai_engine.process_query(text)
        self.ai_engine.text_to_speech(response)
        self.main_window.display_response(response)
        
    def run(self):
        """Run the application"""
        self.main_window.show()
        logger.info("Hacker-Neo Started Successfully!")
        return self.app.exec_()

if __name__ == "__main__":
    try:
        app_instance = HackerNeoApp()
        sys.exit(app_instance.run())
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
