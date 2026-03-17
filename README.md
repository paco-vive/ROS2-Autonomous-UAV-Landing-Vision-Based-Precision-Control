# 🛸 ROS2 Autonomous UAV Landing: Vision-Based Precision Control

[![ROS 2](https://img.shields.io/badge/ROS2-Humble-blue)](https://docs.ros.org/en/humble/index.html)
[![Gazebo](https://img.shields.io/badge/Simulation-Gazebo-orange)](https://gazebosim.org/)
[![OpenCV](https://img.shields.io/badge/Vision-OpenCV-green)](https://opencv.org/)
[![Python](https://img.shields.io/badge/Language-Python-yellow)](https://www.python.org/)

This repository features a fully autonomous Unmanned Aerial Vehicle (UAV) simulation designed to detect, track, and land on a moving or static helipad. Developed using **ROS 2 Humble**, it integrates real-time computer vision with custom flight control algorithms in a high-fidelity **Gazebo** environment.

---

## 📸 Simulation Preview

### System Modeling & Visualization
| Photo 1: Gazebo Environment | Photo 2: RViz2 Sensor Fusion |
|---|---|
| <img src="assets/drone_gazebo.jpg" width="400"> | <img src="assets/drone_rviz.jpg" width="400"> |

### 📹 Autonomous Landing Demo
Watch the vision-based controller guide the UAV to a precision landing:

https://github.com/paco-vive/mi_dron_sim/assets/drone_video.mp4

---

## ⚙️ Core Components

### 👁️ Computer Vision & Tracking
* **Detection:** Implemented a real-time detection pipeline using **OpenCV**.
* **Processing:** Utilized **HSV color space filtering** and contour analysis to isolate the landing target from the downward-facing camera feed.
* **Coordinate Mapping:** Transforms pixel-space errors ($u, v$) into spatial displacement vectors relative to the UAV's body frame.

### 🎮 Flight Control & Physics
* **P-Controller:** Engineered a custom **Proportional Control** system in Python to translate vision errors into 3D velocity commands ($V_x, V_y, V_z$).
* **Physics Engine:** Developed a gravity-compensation layer to maintain a stable $9.81N$ hover and implemented smooth descent logic for the final landing phase.
* **State Management:** Handles transitions between *Search*, *Track*, *Descend*, and *Land* states.

### 🏗️ Modeling & Simulation
* **URDF/Xacro:** Modular UAV model with optimized inertial parameters ($I_{xx}, I_{yy}$) for realistic flight stability.
* **TF2 Transforms:** Managed the coordinate transform tree between the `map`, `base_link`, and `camera_link`.
* **RViz2 Integration:** Real-time visualization of sensor data, camera overlays, and the TF tree for debugging.

---

## 🚀 Getting Started

### Prerequisites
* ROS 2 Humble (Ubuntu 22.04)
* Gazebo (Classic or Ignition)
* OpenCV & CV-Bridge

### Installation
1. **Clone the workspace:**
   ```bash
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws/src
   git clone [https://github.com/paco-vive/mi_dron_sim.git](https://github.com/paco-vive/mi_dron_sim.git)
