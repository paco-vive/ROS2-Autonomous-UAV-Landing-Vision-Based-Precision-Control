# 🛸 ROS2 Autonomous UAV Landing: Vision-Based Precision Control

[![ROS 2](https://img.shields.io/badge/ROS2-Humble-blue)](https://docs.ros.org/en/humble/index.html)
[![Gazebo](https://img.shields.io/badge/Simulation-Gazebo-orange)](https://gazebosim.org/)
[![OpenCV](https://img.shields.io/badge/Vision-OpenCV-green)](https://opencv.org/)
[![Python](https://img.shields.io/badge/Language-Python-yellow)](https://www.python.org/)

Este repositorio contiene una simulación completa de un Vehículo Aéreo No Tripulado (UAV) diseñado para detectar, rastrear y aterrizar de forma autónoma en un helipuerto utilizando **ROS 2 Humble**, **Gazebo** y **OpenCV**.

---

## 📸 Vista Previa del Sistema

| 🌍 Entorno Gazebo | 🛠️ Visualización RViz2 | 👁️ Visión Computacional (OpenCV) |
|---|---|---|
| ![Gazebo](assets/drone_gazebo.jpg) | ![RViz](assets/drone_rviz.jpg) | ![OpenCV](assets/drone_vision.jpg) |

> **🎥 Mira el Video del Aterrizaje Autónomo:** [Link a tu video de YouTube](https://youtu.be/_jGU0q87a7U)

---

## 🧠 Desafíos Técnicos y Soluciones

Este proyecto no solo es código, sino la resolución de problemas físicos en un entorno de simulación:

* **Compensación de Gravedad:** Implementé una capa de control que mantiene una fuerza constante de $9.81N$ para lograr un estado de *Hover* (flotación) estable, traduciendo comandos de velocidad (`Twist`) a fuerzas físicas (`Wrench`).
* **Efecto Péndulo y Estabilidad:** Para evitar el *overshoot* (pasarse de largo), configuré una **Zona Muerta** de 15 píxeles y un limitador de velocidad máxima ($0.15 m/s$), además de ajustar los momentos de inercia ($I_{xx}, I_{yy}$) en el URDF para un vuelo más suave.
* **Control Proporcional (P):** El seguidor utiliza un controlador proporcional para convertir el error de píxeles $(x, y)$ de la cámara en comandos de movimiento lateral y descenso gradual.

---

## ⚙️ Componentes Principales

### 🎮 Control de Vuelo (`controlador_dron.py`)
Un nodo que actúa como puente entre la lógica de alto nivel y la física de Gazebo. Recibe comandos de velocidad y los aplica como fuerzas al `base_link` del dron, permitiendo un descenso controlado de $7.5N$ o un ascenso de $14.0N$.

### 👁️ Visión Artificial (`seguidor_helipuerto.py`)
* **Detección:** Filtro de color en espacio **HSV** para aislar el helipuerto.
* **Tracking:** Cálculo de momentos de contorno para hallar el centro del objetivo.
* **Lógica de Aterrizaje:** Si el dron está centrado ($< 30px$ de error), inicia el descenso automático.

### 🏗️ Modelado URDF
Modelo modular con una cámara fija orientada al suelo ($90^\circ$ pitch) y plugins de Gazebo para la aplicación de fuerzas (`libgazebo_ros_force.so`).

---

## 🚀 Instalación y Uso

### Requisitos
* ROS 2 Humble (Ubuntu 22.04)
* Gazebo Classic
* OpenCV y CV-Bridge (`sudo apt install ros-humble-cv-bridge python3-opencv`)

### Configuración
1. **Clonar el workspace:**
   ```bash
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws/src
   git clone [https://github.com/paco-vive/mi_dron_sim.git](https://github.com/paco-vive/mi_dron_sim.git)
