# 🤖 CrowdMind AI

### Intelligent Event Crowd & Queue Optimizer

CrowdMind AI is a smart event-management system built using **Python and Streamlit**.  
It helps event organizers monitor crowd density, predict future crowd levels, optimize queues, find efficient routes, manage volunteers, and receive AI-based event recommendations.

---

## 🚀 Features

### 👥 Live Crowd Monitor
- Monitor crowd levels in different event zones.
- Calculate occupancy percentage.
- Identify crowd risk levels.
- Simulate live crowd data.
- Display crowd information using charts.

### 🗺️ Smart Route AI
- Provides routes between different event locations.
- Uses **BFS** for path searching.
- Uses **Dijkstra's Algorithm** for shortest weighted routes.
- Displays the route on a digital event map.
- Compares BFS and Dijkstra results.

### 🚦 Queue Intelligence
- Monitor queues at different locations.
- Calculate estimated waiting time.
- Calculate queue priority scores.
- Identify the highest-priority queue.
- Suggest opening additional service counters.

### 🔮 Crowd Predictor
- Predict future crowd occupancy.
- Takes event type and event time into consideration.
- Supports:
  - Seminar
  - Workshop
  - Concert
  - Exhibition
- Provides AI-based crowd-management recommendations.

### 🧑‍💼 AI Volunteer Manager
- Displays available volunteers.
- Matches volunteers according to their skills.
- Supports skills such as:
  - Registration
  - Medical
  - Crowd Control
  - Technical
- Provides automatic volunteer assignment.

### 🧠 Event AI Advisor
- Analyzes current crowd occupancy.
- Checks queue size.
- Considers event type.
- Generates crowd-management recommendations.
- Calculates an event risk score.

### 🎮 Event Simulator
- Allows organizers to experiment with different event conditions.
- Helps understand possible crowd scenarios before an event.

### 🔊 AI Voice Center
- Uses browser-based Text-to-Speech.
- Announces crowd conditions.
- Reads predictions and recommendations aloud.

---

## 🧠 Algorithms Used

CrowdMind AI demonstrates several important algorithms and AI concepts:

| Algorithm / Concept | Purpose |
|---|---|
| BFS | Find a route between locations |
| Dijkstra | Find shortest weighted route |
| Graph Theory | Represent event locations |
| Priority Scoring | Identify important queues |
| Rule-Based Expert System | Generate event recommendations |
| Crowd Prediction | Estimate future occupancy |
| Data Simulation | Simulate live crowd conditions |

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Pandas**
- **NumPy**
- **Matplotlib**
- **NetworkX**
- **Heap Queue (`heapq`)**
- **Deque**
- **Random**
- **HTML / CSS**
- **JavaScript Speech Synthesis API**

---

## 📂 Project Structure

```text
CrowdMind-AI/
│
├── app.py
├── README.md
└── requirements.txt
