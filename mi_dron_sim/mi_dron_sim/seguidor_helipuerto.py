#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class SeguidorHelipuerto(Node):
    def __init__(self):
        super().__init__('seguidor_helipuerto')
        # Se suscribe a la cámara
        self.subscription = self.create_subscription(Image, '/sensor_dron/image_raw', self.image_callback, 10)
        # Publicará comandos de velocidad (para mover el dron)
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.bridge = CvBridge()

    def image_callback(self, msg):
        # 1. Convertir imagen de ROS a OpenCV
        print("¡Recibiendo imagen!")
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # 2. Filtrar el color negro (de la H)
        # Ajusta estos valores si la detección no es buena
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])
        mask = cv2.inRange(hsv, lower_black, upper_black)

        # 3. Encontrar contornos
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        vel_msg = Twist()

        if contours:
            # Tomar el contorno más grande (que debería ser la H)
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            
            if M["m00"] > 500: # Filtro para evitar ruido pequeño
                # Centro de la H en píxeles
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Centro de la imagen (800x600)
                height, width, _ = cv_image.shape
                error_x = cx - (width / 2)
                error_y = cy - (height / 2)


                

                # Dibujar en la imagen para ver qué pasa
                cv2.circle(cv_image, (cx, cy), 10, (0, 255, 0), -1)
                cv2.putText(cv_image, f"Error: {error_x}, {error_y}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                k_p = 0.0012

                if abs(error_x) < 15: error_x = 0
                if abs(error_y) < 15: error_y = 0


                vx = -error_y * k_p
                vy = -error_x * k_p

                max_v_lateral = 0.15 # Muy lento para no perder la visión
                vel_msg.linear.x = max(min(vx, max_v_lateral), -max_v_lateral)
                vel_msg.linear.y = max(min(vy, max_v_lateral), -max_v_lateral)

                # --- LÓGICA DE DESCENSO ---
                # Solo baja si el error es menor a 40 píxeles (está centrado)
                if abs(error_x) < 30 and abs(error_y) < 30:
                    vel_msg.linear.z = -0.2 # Valor sutil para que el controlador aplique 7.5N
                    self.get_logger().info("Centrado: Bajando suave...")
                else:
                    # Al enviar 0.0, el controlador aplicará 9.81N (Hover)
                    vel_msg.linear.z = 0.0 
                    self.get_logger().info("Corrigiendo posición antes de bajar")
                
        # 4. Mostrar la ventana de visión
        self.publisher.publish(vel_msg)
        cv2.imshow("Vision del Dron", cv_image)
        cv2.waitKey(1)
        
        # Publicar el movimiento (opcional por ahora, puedes solo visualizar)
        # self.publisher.publish(vel_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SeguidorHelipuerto()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
