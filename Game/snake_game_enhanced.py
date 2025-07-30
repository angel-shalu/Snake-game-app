import streamlit as st
import numpy as np
import time
import random
from typing import List, Tuple, Optional
import json

class SnakeGame:
    def __init__(self, grid_size: int = 20):
        self.grid_size = grid_size
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.snake = [(self.grid_size // 2, self.grid_size // 2)]  # Start at center
        self.direction = (1, 0)  # Start moving right
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.game_started = False
        self.paused = False
        self.high_score = self.load_high_score()
    
    def load_high_score(self) -> int:
        """Load high score from session state"""
        return st.session_state.get('high_score', 0)
    
    def save_high_score(self):
        """Save high score to session state"""
        if self.score > self.high_score:
            st.session_state.high_score = self.score
            self.high_score = self.score
    
    def generate_food(self) -> Tuple[int, int]:
        """Generate food at random position, avoiding snake body"""
        attempts = 0
        max_attempts = self.grid_size * self.grid_size
        
        while attempts < max_attempts:
            food = (random.randint(0, self.grid_size - 1), 
                   random.randint(0, self.grid_size - 1))
            if food not in self.snake:
                return food
            attempts += 1
        
        # If no space found, return a position anyway (game is won!)
        return (0, 0)
    
    def move_snake(self):
        """Move the snake in current direction"""
        if self.game_over or not self.game_started or self.paused:
            return
        
        # Calculate new head position
        new_head = (
            (self.snake[0][0] + self.direction[0]) % self.grid_size,
            (self.snake[0][1] + self.direction[1]) % self.grid_size
        )
        
        # Check collision with self
        if new_head in self.snake:
            self.game_over = True
            self.save_high_score()
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            # Check if snake fills entire grid (win condition)
            if len(self.snake) >= self.grid_size * self.grid_size:
                self.game_over = True
                self.save_high_score()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def change_direction(self, new_direction: Tuple[int, int]):
        """Change snake direction (prevent 180-degree turns)"""
        if not self.game_over and self.game_started and not self.paused:
            # Prevent opposite direction movement
            if (new_direction[0] != -self.direction[0] or 
                new_direction[1] != -self.direction[1]):
                self.direction = new_direction
    
    def toggle_pause(self):
        """Toggle game pause state"""
        if self.game_started and not self.game_over:
            self.paused = not self.paused
    
    def get_grid_state(self) -> np.ndarray:
        """Get current grid state for visualization"""
        grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        
        # Mark snake body
        for i, segment in enumerate(self.snake):
            if i == 0:  # Head
                grid[segment[1], segment[0]] = 2
            else:  # Body
                grid[segment[1], segment[0]] = 1
        
        # Mark food
        grid[self.food[1], self.food[0]] = 3
        
        return grid

def create_enhanced_game_ui():
    """Create the enhanced game UI with keyboard support"""
    st.set_page_config(
        page_title="Snake Game Enhanced",
        page_icon="🐍",
        layout="wide"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .score-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .game-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
    }
    .controls {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1rem 0;
    }
    .keyboard-hint {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .game-status {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🐍 Snake Game Enhanced</h1>', unsafe_allow_html=True)
    
    # Sidebar for game settings
    with st.sidebar:
        st.header("🎮 Game Settings")
        grid_size = st.slider("Grid Size", 10, 30, 20, help="Size of the game grid")
        game_speed = st.slider("Game Speed (ms)", 100, 500, 200, help="Speed of snake movement")
        
        st.markdown("---")
        st.header("🎯 How to Play")
        st.markdown("""
        **Controls:**
        - **Arrow Keys**: Control snake direction
        - **Space**: Pause/Resume game
        - **R**: Restart game
        - **Arrow Buttons**: Alternative control
        
        **Objective:**
        - Eat 🍎 to grow and score
        - Avoid hitting yourself
        - Snake can pass through walls
        - Fill the entire grid to win!
        """)
        
        st.markdown("---")
        st.header("🏆 High Scores")
        high_score = st.session_state.get('high_score', 0)
        st.metric("Best Score", high_score)
    
    # Initialize game state
    if 'game' not in st.session_state:
        st.session_state.game = SnakeGame(grid_size)
    
    # Update game with new grid size if changed
    if st.session_state.game.grid_size != grid_size:
        st.session_state.game = SnakeGame(grid_size)
    
    # Score display
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="score-display">
            <h2>Score: {st.session_state.game.score}</h2>
            <p>Snake Length: {len(st.session_state.game.snake)} | High Score: {st.session_state.game.high_score}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Game controls
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎮 Start/Restart Game", type="primary", use_container_width=True):
            st.session_state.game.reset_game()
            st.session_state.game.game_started = True
            st.rerun()
    
    # Direction controls
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col2:
        if st.button("⬆️ Up", use_container_width=True):
            st.session_state.game.change_direction((0, -1))
    
    with col1:
        if st.button("⬅️ Left", use_container_width=True):
            st.session_state.game.change_direction((-1, 0))
    
    with col3:
        if st.button("⬇️ Down", use_container_width=True):
            st.session_state.game.change_direction((0, 1))
    
    with col4:
        if st.button("➡️ Right", use_container_width=True):
            st.session_state.game.change_direction((1, 0))
    
    with col5:
        if st.button("⏸️ Pause", use_container_width=True):
            st.session_state.game.toggle_pause()
    
    # Keyboard controls hint
    st.markdown("""
    <div class="keyboard-hint">
        <strong>💡 Keyboard Controls:</strong> Use arrow keys to control the snake, Space to pause, R to restart
    </div>
    """, unsafe_allow_html=True)
    
    # Game status
    if st.session_state.game.game_over:
        if len(st.session_state.game.snake) >= st.session_state.game.grid_size * st.session_state.game.grid_size:
            st.markdown("""
            <div class="game-status" style="background-color: #d4edda; color: #155724;">
                🎉 Congratulations! You've filled the entire grid! You win!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="game-status" style="background-color: #f8d7da; color: #721c24;">
                💀 Game Over! Press Start/Restart to play again.
            </div>
            """, unsafe_allow_html=True)
    elif st.session_state.game.paused:
        st.markdown("""
        <div class="game-status" style="background-color: #fff3cd; color: #856404;">
            ⏸️ Game Paused! Press Pause again or Space to resume.
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.game.game_started:
        st.markdown("""
        <div class="game-status" style="background-color: #d1ecf1; color: #0c5460;">
            🎯 Game Running! Use controls to play.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="game-status" style="background-color: #e2e3e5; color: #383d41;">
            🎮 Press Start/Restart to begin the game!
        </div>
        """, unsafe_allow_html=True)
    
    # Game grid visualization
    if st.session_state.game.game_started:
        # Move snake
        st.session_state.game.move_snake()
        
        # Get grid state
        grid = st.session_state.game.get_grid_state()
        
        # Create visual representation with better styling
        grid_display = []
        for row in grid:
            row_display = []
            for cell in row:
                if cell == 0:  # Empty
                    row_display.append("⬜")
                elif cell == 1:  # Snake body
                    row_display.append("🟩")
                elif cell == 2:  # Snake head
                    row_display.append("🟢")
                elif cell == 3:  # Food
                    row_display.append("🍎")
            grid_display.append(" ".join(row_display))
        
        # Display grid with better styling
        st.markdown('<div class="game-container">', unsafe_allow_html=True)
        for row in grid_display:
            st.markdown(f"<div style='text-align: center; font-family: monospace; font-size: 1.3rem; line-height: 1.2;'>{row}</div>", 
                       unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auto-refresh for continuous gameplay
        time.sleep(game_speed / 1000)
        st.rerun()

if __name__ == "__main__":
    create_enhanced_game_ui() 