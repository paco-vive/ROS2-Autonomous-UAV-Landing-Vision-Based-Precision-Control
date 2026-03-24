#!/usr/bin/env python3


import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Wrench

class ControladorDron(Node):
    def __init__(self):
        super().__init__('controlador_dron')
        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.listener_callback, 10)
        self.publisher = self.create_publisher(Wrench, 'cmd_force', 10)
        
        # Guardamos el último comando recibido
        self.ultimo_twist = Twist()
        
        # TIMER: Envía fuerza a Gazebo cada 0.02 segundos (50Hz)
        self.timer = self.create_timer(0.02, self.publicar_fuerza)

    def listener_callback(self, msg):
        self.ultimo_twist = msg
    
    def publicar_fuerza(self):
        fuerza = Wrench()
        msg = self.ultimo_twist

        # Multiplicadores de movimiento XY
        fuerza.force.x = msg.linear.x * 12.0
        fuerza.force.y = msg.linear.y * 12.0
        
        # LÓGICA DE ALTURA CONSTANTE
        if msg.linear.z > 0.05:
            fuerza.force.z = 14.0  # Sube
        elif msg.linear.z < -0.05:
            fuerza.force.z = 7.5   # Baja controlado (menor que 9.8)
        else:
            # Si no hay comando Z, mantiene la gravedad EXACTA para flotar
            fuerza.force.z = 9.78 

        self.publisher.publish(fuerza)

def main(args=None):
    rclpy.init(args=args)
    node = ControladorDron()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
