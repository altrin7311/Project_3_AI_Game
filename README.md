# EscapeIQ: AI vs Human Pathfinding Game

EscapeIQ is a Python-based interactive educational game built using the Pygame library. It allows a human player to compete against an AI agent across a 12×12 grid to reach a common goal. The AI uses one of 15 pathfinding algorithms, and the game visually compares all algorithms' performances after each round. It blends gameplay with algorithm visualization for a hands-on learning experience.

---

## I. Features

- 15 classic and modern pathfinding algorithms
- AI vs Human turn-based gameplay
- Algorithm selection via keyboard
- Random obstacle generation
- Performance metrics for each algorithm
- Post-game multi-algorithm visual comparison

---

## II. Algorithms Implemented

The following algorithms are available:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Dijkstra’s Algorithm
- Greedy Best-First Search
- A* Search
- Uniform Cost Search (UCS)
- Iterative Deepening DFS (IDDFS)
- Bidirectional BFS
- Hill Climbing
- Beam Search
- Jump Point Search (stubbed as A*)
- Random Walk
- Right-Hand Rule
- Left-Hand Rule
- Best Random Path

Each can be selected through a pre-game UI.

---

## III. Gameplay Instructions

- Use the **arrow keys** to move the human player.
- Use **Enter** to select an AI algorithm at the start.
- After either agent reaches the goal, a comparison screen shows how all other algorithms would have performed.

---

## IV. Graph & Grid Logic

The grid acts as a 2D representation of a graph:
- Each tile is a node
- Each movement is an edge
- Obstacles are blocked nodes

Pathfinding algorithms explore this graph to reach the goal efficiently.

---

## V. Performance Metrics

Each algorithm is evaluated on:
- **Path Length**: Total steps to reach the goal
- **Visited Nodes**: Number of distinct tiles explored
- **Time Taken**: Runtime in milliseconds

These are shown beneath each mini-grid in the post-game view.

---

## VI. Real-World Application: Disaster Evacuation

EscapeIQ can simulate evacuation planning:
- Grids represent floor plans or urban layouts
- Obstacles simulate blocked exits or hazards
- Algorithms test safe and fast evacuation strategies
- Metrics assist in evaluating optimal paths

Future enhancements could include dynamic routing, real-time hazard updates, or multi-agent coordination.

---

## VII. Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/escapeiq-game.git
   cd escapeiq-game
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the game:
   ```bash
   python main.py
   ```

---

## VIII. File Structure

```
Project_4_AI_Game/
├── ai_algorithms.py
├── config.py
├── game.py
├── player.py
├── ui_utils.py
├── main.py
├── README.md
└── requirements.txt
```

---

## IX. License

This project is licensed under the MIT License.
