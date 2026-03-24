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

- **Compensación de Gravedad:** Implementé una capa de control que mantiene una fuerza constante de $9.81N$ para lograr un estado de *Hover* (flotación) estable, traduciendo comandos de velocidad (`Twist`) a fuerzas físicas (`Wrench`).
- **Efecto Péndulo y Estabilidad:** Para evitar el *overshoot* (pasarse de largo), configuré una **Zona Muerta** de 15 píxeles y un limitador de velocidad máxima ($0.15 m/s$), además de ajustar los momentos de inercia ($I_{xx}, I_{yy}$) en el URDF para un vuelo más suave.
- **Control Proporcional (P):** El seguidor utiliza un controlador proporcional para convertir el error de píxeles $(x, y)$ de la cámara en comandos de movimiento lateral y descenso gradual.

---

## ⚙️ Componentes Principales

### 🎮 Control de Vuelo (`controlador_dron.py`)
Un nodo que actúa como puente entre la lógica de alto nivel y la física de Gazebo. Recibe comandos de velocidad y los aplica como fuerzas al `base_link` del dron, permitiendo un descenso controlado de $7.5N$ o un ascenso de $14.0N$.

### 👁️ Visión Artificial (`seguidor_helipuerto.py`)
- **Detección:** Filtro de color en espacio **HSV** para aislar el helipuerto.
- **Tracking:** Cálculo de momentos de contorno para hallar el centro del objetivo.
- **Lógica de Aterrizaje:** Si el dron está centrado ($< 30px$ de error), inicia el descenso automático.

### 🏗️ Modelado URDF
Modelo modular con una cámara fija orientada al suelo ($90^\circ$ pitch) y plugins de Gazebo para la aplicación de fuerzas (`libgazebo_ros_force.so`).

---

## 🚀 Instalación y Uso

### Requisitos
- ROS 2 Humble (Ubuntu 22.04)
- Gazebo Classic
- OpenCV y CV-Bridge:
  ```bash
  sudo apt install ros-humble-cv-bridge python3-opencv
  ```

### Configuración

1. **Clonar el workspace:**
   ```bash
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws/src
   git clone https://github.com/paco-vive/mi_dron_sim.git
   ```

2. **Instalar el modelo del helipuerto:**
   Es crucial copiar la carpeta del modelo a la ruta de Gazebo para que las texturas carguen:
   ```bash
   mkdir -p ~/.gazebo/models/
   cp -r ~/ros2_ws/src/mi_dron_sim/models/mi_helipuerto ~/.gazebo/models/
   ```

3. **Compilar:**
   ```bash
   cd ~/ros2_ws
   colcon build --packages-select mi_dron_sim
   source install/setup.bash
   ```

### Ejecución

Abre 4 terminales y ejecuta en orden (haciendo `source install/setup.bash` en cada una):

| Terminal | Comando |
|---|---|
| T1 — Simulación | `ros2 launch mi_dron_sim sim_launch.py` |
| T2 — Física | `ros2 run mi_dron_sim controlador_dron.py` |
| T3 — IA/Visión | `ros2 run mi_dron_sim seguidor_helipuerto.py` |
| T4 — Teclado (Opcional) | `ros2 run teleop_twist_keyboard teleop_twist_keyboard` |

---

## 🛠️ Estructura del Repositorio

```
mi_dron_sim/
├── launch/             # Scripts de lanzamiento (Gazebo + Robot State)
├── urdf/               # Definición del dron y sensores
├── mi_dron_sim/        # Lógica de Python (Control y Visión)
├── models/             # Carpeta del helipuerto (SDF + Texturas)
├── CMakeLists.txt      # Configuración de compilación C++/Ament
└── package.xml         # Dependencias del proyecto
```

---

## 👨‍💻 Autor

**Paco-Vive** — [Tu Perfil de GitHub](https://github.com/paco-vive)
