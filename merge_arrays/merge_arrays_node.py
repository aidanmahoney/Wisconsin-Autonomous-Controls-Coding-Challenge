import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

class MergeArraysNode(Node):
    def __init__(self):
        super().__init__('merge_arrays_node')
        
        self.sub1 = self.create_subscription(Int32MultiArray, '/input/array1', self.array1_callback, 10)
        self.sub2 = self.create_subscription(Int32MultiArray, '/input/array2', self.array2_callback, 10)
        
        self.publisher = self.create_publisher(Int32MultiArray, '/output/array', 10)
        
        self.array1 = None
        self.array2 = None

    def array1_callback(self, msg):
        self.array1 = list(msg.data)
        self.get_logger().info(f'Received array 1: {self.array1}')
        self.try_merge_and_publish()

    def array2_callback(self, msg):
        self.array2 = list(msg.data)
        self.get_logger().info(f'Received array 2: {self.array2}')
        self.try_merge_and_publish()

    def try_merge_and_publish(self):
        if self.array1 is not None and self.array2 is not None:
            merged = []
            i, j = 0, 0
            
            while i < len(self.array1) and j < len(self.array2):
                if self.array1[i] < self.array2[j]:
                    merged.append(self.array1[i])
                    i += 1
                else:
                    merged.append(self.array2[j])
                    j += 1
                    
            merged.extend(self.array1[i:])
            merged.extend(self.array2[j:])
            
            output_msg = Int32MultiArray()
            output_msg.data = merged
            self.publisher.publish(output_msg)

            self.get_logger().info(f'Published merged array: {merged}')
            
            self.array1 = None
            self.array2 = None

def main(args=None):
    rclpy.init(args=args)
    node = MergeArraysNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()