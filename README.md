# 🛸 ROS2 Autonomous UAV Landing: Vision-Based Precision Control

[![ROS 2](https://img.shields.io/badge/ROS2-Humble-blue)](https://docs.ros.org/en/humble/index.html)
[![Gazebo](https://img.shields.io/badge/Simulation-Gazebo-orange)](https://gazebosim.org/)
[![OpenCV](https://img.shields.io/badge/Vision-OpenCV-green)](https://opencv.org/)
[![Python](https://img.shields.io/badge/Language-Python-yellow)](https://www.python.org/)

A full simulation of an Unmanned Aerial Vehicle (UAV) designed to autonomously detect, track, and land on a helipad using **ROS 2 Humble**, **Gazebo**, and **OpenCV**.

---

## 📸 System Preview

| 🌍 Gazebo Environment | 🛠️ RViz2 Visualization | 👁️ Computer Vision (OpenCV) |
|---|---|---|
| ![Gazebo](assets/drone_gazebo.jpg) | ![RViz](assets/drone_rviz.jpg) | ![OpenCV](assets/drone_vision.jpg) |

> **🎥 Watch the Autonomous Landing Demo:** [YouTube Link](https://youtu.be/_jGU0q87a7U)

---

## 🧠 Technical Challenges & Solutions

This project goes beyond writing code — it tackles real physics and control problems inside a simulation environment:

- **Gravity Compensation:** Implemented a control layer that applies a constant $9.81\,N$ upward force to achieve a stable *hover* state, translating velocity commands (`Twist`) into physical forces (`Wrench`).
- **Pendulum Effect & Stability:** To prevent *overshoot*, a **15-pixel dead zone** and a maximum velocity cap of $0.15\,m/s$ were configured. Inertia moments ($I_{xx},\,I_{yy}$) in the URDF were also tuned for smoother, more stable flight.
- **Proportional Control (P):** The tracking node uses a proportional controller to convert pixel error $(x, y)$ from the camera feed into lateral movement and gradual descent commands.

---

## ⚙️ Core Components

### 🎮 Flight Controller (`controlador_dron.py`)
A ROS 2 node that bridges high-level logic and Gazebo physics. It receives velocity commands and applies them as forces to the drone's `base_link`, enabling controlled descent at $7.5\,N$ or ascent at $14.0\,N$.

### 👁️ Computer Vision (`seguidor_helipuerto.py`)
- **Detection:** HSV color-space filtering to isolate the helipad from the camera feed.
- **Tracking:** Contour moment calculation to find the centroid of the target.
- **Landing Logic:** Once the drone is centered (error $< 30\,px$), automatic descent is triggered.

### 🏗️ URDF Modeling
A modular robot description featuring a downward-facing camera ($90°$ pitch) and Gazebo force-application plugins (`libgazebo_ros_force.so`).

---

## 🚀 Installation & Usage

### Requirements
- ROS 2 Humble (Ubuntu 22.04)
- Gazebo Classic
- OpenCV & CV-Bridge

```bash
sudo apt install ros-humble-cv-bridge python3-opencv
```

### Setup

1. **Clone the workspace:**
   ```bash
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws/src
   git clone https://github.com/paco-vive/mi_dron_sim.git
   ```

2. **Install the helipad model:**
   Copy the model folder to the Gazebo models path so textures load correctly:
   ```bash
   mkdir -p ~/.gazebo/models/
   cp -r ~/ros2_ws/src/mi_dron_sim/models/mi_helipuerto ~/.gazebo/models/
   ```

3. **Build:**
   ```bash
   cd ~/ros2_ws
   colcon build --packages-select mi_dron_sim
   source install/setup.bash
   ```

### Running

Open **4 terminals** and run in order (remember to `source install/setup.bash` in each):

| Terminal | Command |
|---|---|
| T1 — Simulation | `ros2 launch mi_dron_sim sim_launch.py` |
| T2 — Physics | `ros2 run mi_dron_sim controlador_dron.py` |
| T3 — Vision / AI | `ros2 run mi_dron_sim seguidor_helipuerto.py` |
| T4 — Keyboard *(optional)* | `ros2 run teleop_twist_keyboard teleop_twist_keyboard` |

---

## 🛠️ Repository Structure

```
mi_dron_sim/
├── launch/             # Launch files (Gazebo + Robot State Publisher)
├── urdf/               # Drone and sensor definitions
├── mi_dron_sim/        # Python nodes (Control & Vision)
├── models/             # Helipad model (SDF + Textures)
├── CMakeLists.txt      # Ament/C++ build configuration
└── package.xml         # Project dependencies
```

---

## 👨‍💻 Author

**Paco-Vive** — [GitHub Profile](https://github.com/paco-vive)
