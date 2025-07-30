# 🐍 Snake Game

A modern Snake game built with Python and Streamlit that runs in your browser!

## Features

- 🎮 **Interactive Gameplay**: Smooth snake movement with button controls
- 🍎 **Food Collection**: Eat food to grow and score points
- 📊 **Score Tracking**: Real-time score and snake length display
- ⚙️ **Customizable Settings**: Adjust grid size and game speed
- 🎨 **Modern UI**: Beautiful, responsive interface with emojis
- 🔄 **Auto-refresh**: Continuous gameplay with configurable speed
- 🚫 **Collision Detection**: Game over when snake hits itself
- 🌐 **Wall Wrapping**: Snake can pass through walls

## Installation

1. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the game:**

   ```bash
   streamlit run snake_game.py
   ```

3. **Open your browser** and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

## How to Play

1. **Start the Game**: Click the "🎮 Start/Restart Game" button
2. **Control the Snake**: Use the arrow buttons (⬆️⬅️⬇️➡️) to change direction
3. **Eat Food**: Guide the snake to eat the red apples (🍎) to grow and score
4. **Avoid Collisions**: Don't let the snake hit itself
5. **Customize**: Use the sidebar to adjust grid size and game speed

## Game Controls

- **⬆️ Up**: Move snake upward
- **⬅️ Left**: Move snake left
- **⬇️ Down**: Move snake downward
- **➡️ Right**: Move snake right
- **🎮 Start/Restart**: Begin a new game

## Game Settings

- **Grid Size**: Adjust from 10x10 to 30x30 (default: 20x20)
- **Game Speed**: Control movement speed from 100ms to 500ms (default: 200ms)

## Technical Details

- **Framework**: Streamlit for web interface
- **Language**: Python 3.7+
- **Dependencies**: streamlit, numpy
- **Architecture**: Object-oriented design with clean separation of game logic and UI

## Game Mechanics

- **Snake Movement**: Continuous movement in current direction
- **Food Generation**: Random placement avoiding snake body
- **Scoring**: +10 points per food eaten
- **Growth**: Snake grows when eating food
- **Collision**: Game over when snake hits itself
- **Wrapping**: Snake can pass through grid boundaries

Enjoy playing! 🎉
