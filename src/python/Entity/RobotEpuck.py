from torch._C import dtype
from Entity.RobotBase import RobotBase
from Algorithm.RobotPolicy import RobotPolicyBase
from Entity.CameraEPuck import CameraEPuck
from Control import MainController
from PyQt5.QtCore import pyqtSignal, QObject, QEvent
import numpy as np
import math
from Common.XSetting import XSetting
from Common import Common
import socket
from Common.DebugPrint import myDebug, get_current_function_name
from PyQt5 import QtCore
from PyQt5.QtGui import QImage
import cv2
import time
from enum import Enum
import math

TCP_PORT = 1000 # This is fixed.
MAX_NUM_CONN_TRIALS = 5
COMMAND_PACKET_SIZE = 21
HEADER_PACKET_SIZE = 1
IMAGE_PACKET_SIZE = 38400 # Max buffer size = 160x120x2
SENSORS_PACKET_SIZE = 104


class RobotControlMode(Enum):
    RemoteControl = 0
    PolicyControl = 1        


class PathFinderController:
    """
    Constructs an instantiate of the PathFinderController for navigating a
    3-DOF wheeled robot on a 2D plane

    Parameters
    ----------
    Kp_rho : The linear velocity gain to translate the robot along a line
             towards the goal
    Kp_alpha : The angular velocity gain to rotate the robot towards the goal
    Kp_beta : The offset angular velocity gain accounting for smooth merging to
              the goal angle (i.e., it helps the robot heading to be parallel
              to the target angle.)
    """

    def __init__(self, Kp_rho, Kp_alpha, Kp_beta):
        self.Kp_rho = Kp_rho
        self.Kp_alpha = Kp_alpha
        self.Kp_beta = Kp_beta

    def calc_control_command(self, x_diff, y_diff, theta, theta_goal, alpha_pre):
        """
        Returns the control command for the linear and angular velocities as
        well as the distance to goal

        Parameters
        ----------
        x_diff : The position of target with respect to current robot position
                 in x direction
        y_diff : The position of target with respect to current robot position
                 in y direction
        theta : The current heading angle of robot with respect to x axis
        theta_goal: The target angle of robot with respect to x axis

        Returns
        -------
        rho : The distance between the robot and the goal position
        v : Command linear velocity
        w : Command angular velocity
        """

        # Description of local variables:
        # - alpha is the angle to the goal relative to the heading of the robot
        # - beta is the angle between the robot's position and the goal
        #   position plus the goal angle
        # - Kp_rho*rho and Kp_alpha*alpha drive the robot along a line towards
        #   the goal
        # - Kp_beta*beta rotates the line so that it is parallel to the goal
        #   angle
        #
        # Note:
        # we restrict alpha and beta (angle differences) to the range
        # [-pi, pi] to prevent unstable behavior e.g. difference going
        # from 0 rad to 2*pi rad with slight turn

        rho = np.hypot(x_diff, y_diff)
        alpha = (np.arctan2(y_diff, x_diff)
                 - theta + np.pi) % (2 * np.pi) - np.pi
        beta = (theta_goal - theta - alpha + np.pi) % (2 * np.pi) - np.pi

        # if abs(alpha * 180 / math.pi) <= 2.0:  # 如果角度差小于2度，忽略好了。
        #     alpha = 0
        # if rho < 60:  # 如果在距离目标半径6cm范围内，alpha还会产生大于10度的突变，忽略该突变。
        #     if abs(alpha - alpha_pre) * 180 / math.pi > 10:
        #         alpha = alpha_pre
        # if abs(beta * 180 / math.pi) <= 2:  # 如果角度差小于2度，忽略好了。
        #     beta = 0

        v = self.Kp_rho * rho
        w = self.Kp_alpha * alpha - self.Kp_beta * beta

        if alpha > np.pi / 2 or alpha < -np.pi / 2:
            v = -v

        return v, w, rho, alpha, beta


class RobotEpuck(RobotBase):
    def __init__(self, parent, population, pos=np.array((0, 0, 0), dtype=np.float), orientation = np.zeros((3,3), dtype=np.float)) -> None:
        myDebug(self.__class__.__name__, get_current_function_name())
        super().__init__(parent)
        self.mRobotType = "RobotEpuck"
        self.mState = RobotControlMode.PolicyControl
        self.isTestRobot = False                        # 是否是用于测试模式，测试模式下epuck无需开机，程序不会连接到epuck
        self.mCamera = CameraEPuck(self)
        self.mPopulation = population
        self.mPos = np.array(pos, dtype=np.float)
        self.mOrientation = np.array(orientation, dtype=np.float)
        self.mSpeedWheels:np.ndarray = np.zeros((1, 2), dtype=np.float)

        self.mTargetEulerAngle = 0.0      # 世界坐标系下目标角度
        self.mRobotEulerAngle  = 0.0      # 世界坐标系下机器人角度
        self.mX_t  = 0.0                  # 目标坐标系下机器人坐标
        self.mY_t  = 0.0                  # 目标坐标系下机器人坐标
        self.mLineSpeed = 0.0
        self.mRotationSpeed = 0.0
        self.mAlpha = 0.0
        self.mPreAlpha = 0.0
        self.mTheta = 0.0
        self.mBeta = 0.0

        # self.mTObsacle = target_obstacle    # 目标障碍物
        self.client_sock = 1000
        self.client_addr = "192.168.1.100"
        self.isConnected = False
        self.socket_error = 0
        self.isFirstConnect = True
        self.proximity = [0.0]*8  # 8个方向的距离传感器
        self.acceleration = 0.0 # 加速度
        self.orientation = 0.0  # 方向
        self.inclination = 0.0  # 倾斜度
        self.lightAvg = 0       # light sensor data
        self.gyroRaw = [0.0]*3    # Gyro
        self.magneticField = [0.0]*3    # Magnetometer
        self.distanceCm = 0.0   # ToF
        self.micVolume = [0]*4  # Microphone
        self.batteryRaw = 100.0 # Battery

        self.num_packets = 0
        self.mCommand = bytearray([0] * COMMAND_PACKET_SIZE)
        self.initCommand()
        self.mPolicy:RobotPolicyBase = None         # 机器人的决策，通过插件更改

        self.isGetLocationFromGlobal = True
        self.isDataStreamOn = False                 # 是否开启机器人数据传输到主机

        self.nearDestination = False
        self.toNextTarget = False   # if a robot has near the now target, it change the target value to the next target, to avoid speed down,

        # 参数
        self.MAX_SPEED = float(XSetting.getValue('Epuck/MAX_SPEED'))
        self.mMaxAngularSpeed = float(XSetting.getValue('Epuck/MAX_ROTATION_SPEED'))
        self.WHEEL_RADIUS = float(XSetting.getValue('Epuck/WHEEL_RADIUS'))
        self.AXLE_LENGTH = float(XSetting.getValue('Epuck/AXLE_LENGTH'))
        self.K_RHO = float(XSetting.getValue('Epuck/K_RHO'))
        self.K_ALPHA = float(XSetting.getValue('Epuck/K_ALPHA'))
        self.K_BETA = float(XSetting.getValue('Epuck/K_BETA'))

    def initCommand(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mCommand[0] = 0x80	    # Packet id for settings actuators
        self.mCommand[1] = 1		# Request: only sensors enabled
        self.mCommand[2] = 0		# Settings: set motors speed
        self.mCommand[3] = 0		# left motor LSB
        self.mCommand[4] = 0		# left motor MSB
        self.mCommand[5] = 0		# right motor LSB
        self.mCommand[6] = 0		# right motor MSB
        self.mCommand[7] = 0x00	# lEDs
        self.mCommand[8] = 0		# LED2 red
        self.mCommand[9] = 0		# LED2 green
        self.mCommand[10] = 0		# LED2 blue
        self.mCommand[11] = 0		# LED4 red	
        self.mCommand[12] = 0		# LED4 green
        self.mCommand[13] = 0		# LED4 blue
        self.mCommand[14] = 0		# LED6 red
        self.mCommand[15] = 0		# LED6 green
        self.mCommand[16] = 0		# LED6 blue
        self.mCommand[17] = 0		# LED8 red
        self.mCommand[18] = 0		# LED8 green
        self.mCommand[19] = 0		# LED8 blue
        self.mCommand[20] = 0		# speaker

    def setTarget(self, target):
        super().setTarget(target)
        # self.mTargetOrientation[0, 0] 

        # 旧代码
        # if target[5] > 0:
        #     self.mTargetEulerAngle = target[5]
        # else:
        #     self.mTargetEulerAngle = target[5]

        # 黄吉修改代码 start
        # if target[5] > 180:  # if input in range [0, 360]
        #     self.mTargetEulerAngle = -360 + target[5]
        # else:
        #     self.mTargetEulerAngle = target[5]
        # 黄吉修改代码 end

        self.mTargetEulerAngle = target[5]*math.pi/180
        sin_i = math.sin(self.mTargetEulerAngle)
        cos_i = math.cos(self.mTargetEulerAngle)
        self.mTargetOrientation[0, 0] = cos_i
        self.mTargetOrientation[0, 1] = -sin_i
        self.mTargetOrientation[1, 0] = sin_i
        self.mTargetOrientation[1, 1] = cos_i
        self.mTargetOrientation[2, 2] = 1

    def setSpeed(self, motor_L, motor_R):
        # myDebug(self.__class__.__name__, get_current_function_name())
        if motor_L >= 0:
            self.mCommand[4] = motor_L//256
            self.mCommand[3] = abs(motor_L)%256
        else:
            self.mCommand[4] = 255-(abs(motor_L)//256)
            self.mCommand[3] = abs(motor_L+1)%256
        if motor_R >= 0:
            self.mCommand[6] = motor_R//256
            self.mCommand[5] = abs(motor_R)%256
        else:
            self.mCommand[6] = 255-(abs(motor_R)//256)
            self.mCommand[5] = abs(motor_R+1)%256
        
        

    def update(self):
        """

        :return:
        """
        # myDebug(self.__class__.__name__, get_current_function_name())
        # If there was some errors in sending or receiving then try to close the connection and reconnect.
        if not self.isConnected and not self.isTestRobot:
            self.socket_error = 0
            self.connect(self.client_addr)

        # if self.mPolicy is not None and self.mState == RobotControlMode.PolicyControl:
        if self.mPolicy is not None:
            self.mPolicy.update()
        
        # Send a command to the robot.
        # self.mCommand[1] = 3
        # self.sendCommand(self.getCommand(), COMMAND_PACKET_SIZE)
        # self.getState()
        # self.mCommand[1] = 2	
        # self.sendCommand(self.getCommand(), COMMAND_PACKET_SIZE)
        # self.getState()
        if self.isDataStreamOn and not self.isTestRobot:
            self.mCommand[1] = 3
            self.sendCommand(self.getCommand(), COMMAND_PACKET_SIZE)
            self.getState()
            self.mCommand[1] = 2	
            self.sendCommand(self.getCommand(), COMMAND_PACKET_SIZE)
            self.getState()
        elif not self.isTestRobot:
            self.mCommand[1] = 0
            self.sendCommand(self.getCommand(), COMMAND_PACKET_SIZE)
        # self.mCommand[1] = 2	
        # self.sendCommand(self.getCommand(), COMMAND_PACKET_SIZE)
        # self.getState()
        if self.isGetLocationFromGlobal:
            self.queryGlobalLocation()

    

    def getCommand(self):
        # myDebug(self.__class__.__name__, get_current_function_name())
        return self.mCommand

    def sendCommand(self, msg, msg_len):
        # myDebug(self.__class__.__name__, get_current_function_name())
        # Send a command to the robot.
        try:
            totalsent = 0
            while totalsent < msg_len:
                sent = self.client_sock.send(msg[totalsent:])
                if sent == 0:
                    raise RuntimeError("Send error")
                totalsent = totalsent + sent
        except socket.timeout as err:
            self.disconnect()
            print('test1')
            print("Error from " + self.client_addr + ":")
            print(err)
            self.socket_error = 1
        except socket.error as err:
            self.disconnect()
            print('test2')
            print("Error from " + self.client_addr + ":")
            print(err)
            self.socket_error = 1
        except Exception as err:
            self.disconnect()
            print('test3')
            print("Error from " + self.client_addr + ":")
            print(err)
            self.socket_error = 1	

    def connect(self, ip):
        myDebug(self.__class__.__name__, get_current_function_name())
        # Init the connection. In case of errors, try again for a while and eventually give up in case the connection cannot be accomplished.
        self.client_addr = ip
        print("Try to connect to " + self.client_addr + ":" + str(TCP_PORT) + " (TCP)")	
        trials = 0		
        while trials < MAX_NUM_CONN_TRIALS:
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client_sock.settimeout(10) # non-blocking socket
            try:
                self.client_sock.connect((self.client_addr, TCP_PORT))
                self.isConnected = True
                self.mCamera.setID(self.mId)
                self.mCamera.openCamera()
            except socket.timeout as err:
                self.disconnect()
                print("Error from " + self.client_addr + ":")
                print(err)
                trials += 1
                continue
            except socket.error as err:
                self.disconnect()
                print("Error from " + self.client_addr + ":")
                print(err)
                trials += 1
                continue
            except Exception as err:
                self.disconnect()
                print("Error from " + self.client_addr + ":")
                print(err)
                trials += 1
                continue
            break
                
        if trials == MAX_NUM_CONN_TRIALS:
            print("Can't connect to " + self.client_addr)
            return
            
        if self.isFirstConnect:
            print("Connected to " + self.client_addr)
            print("\r\n")
            self.isFirstConnect = False 

    def getState(self):
        # myDebug(self.__class__.__name__, get_current_function_name())
        # Set the number of expected packets to receive based on the request done.
        #expected_recv_packets = 2 # Camera and sensors.
        expected_recv_packets = 1 # Only sensors.
        
        while(expected_recv_packets > 0):
            # Get the first byte to distinguish the content of the packet.
            try:
                header = self.receive(HEADER_PACKET_SIZE)
                #print("header=" + str(header[0]))
            except socket.timeout as err:
                self.disconnect()
                print("Error from " + self.client_addr + ":")
                print(err)				
                self.socket_error = 1
                break
            except socket.error as err:
                self.disconnect()
                print("Error from " + self.client_addr + ":")
                print(err)
                self.socket_error = 1
                break
            except Exception as err:
                self.disconnect()
                print("Error from " + self.client_addr + ":")
                print(err)
                self.socket_error = 1
                break				
            # print(header)
            if header == bytearray([1]): # Get a QQVGA image
                try:
                    image = self.receive(IMAGE_PACKET_SIZE)
                    image = np.frombuffer(image, np.uint8)
                    img_np = Common.Common.rgb565ToRgb888(image, 120, 160)
                    self.mCamera.updateFrame(img_np)
                except socket.timeout as err:
                    self.disconnect()
                    print("Error from " + self.client_addr + ":")
                    print(err)
                    self.socket_error = 1
                    break
                except socket.error as err:
                    self.disconnect()
                    print("Error from " + self.client_addr + ":")
                    print(err)
                    self.socket_error = 1
                    break
                except Exception as err:
                    self.disconnect()
                    print("Error from " + self.client_addr + ":")
                    print(err)
                    self.socket_error = 1
                    break
                    
            elif header == bytearray([2]): # Get sensors data
                try:
                    sensor = self.receive(SENSORS_PACKET_SIZE)
                except socket.timeout as err:
                    self.disconnect()
                    print("Error from " + self.client_addr + ":")
                    print(err)
                    self.socket_error = 1
                    break
                except socket.error as err:
                    self.disconnect()
                    print("Error from " + self.client_addr + ":")
                    print(err)
                    self.socket_error = 1
                    break
                except Exception as err:
                    self.disconnect()
                    print("Error from " + self.client_addr + ":")
                    print(err)
                    self.socket_error = 1
                    break					
                self.proximity[0] = sensor[37] + sensor[38]*256
                self.proximity[1] = sensor[39] + sensor[40]*256
                self.proximity[2] = sensor[41] + sensor[42]*256
                self.proximity[3] = sensor[43] + sensor[44]*256
                self.proximity[4] = sensor[45] + sensor[46]*256
                self.proximity[5] = sensor[47] + sensor[48]*256
                self.proximity[6] = sensor[49] + sensor[50]*256
                self.proximity[7] = sensor[51] + sensor[52]*256

                # Compute acceleration
                mantis = (sensor[6] & 0xFF) + ((sensor[7] & 0xFF) << 8) + (((sensor[8] &0x7f) | 0x80) << 16)
                exp = (sensor[9] & 0x7f) * 2 + (1 if (sensor[8] & 0x80) else 0)
                if sensor[9] & 0x80:
                    mantis = -mantis
                flt = math.ldexp(mantis, (exp - 127 - 23)) if mantis or exp else 0
                self.acceleration = flt 

                # Compute orientation.
                mantis = (sensor[10] & 0xff) + ((sensor[11] & 0xff) << 8) + (((sensor[12] &0x7f) | 0x80) << 16)
                exp = (sensor[13] & 0x7f) * 2 + (1 if (sensor[12] & 0x80) else 0)
                if sensor[13] & 0x80:
                    mantis = -mantis
                flt = math.ldexp(mantis, (exp - 127 - 23)) if (mantis or exp) else 0
                self.orientation = flt
                if self.orientation < 0.0:
                    self.orientation = 0.0
                if self.orientation > 360.0:
                    self.orientation = 360.0
                
                # Compute inclination.
                mantis = (sensor[14] & 0xff) + ((sensor[15] & 0xff) << 8) + (((sensor[16] &0x7f) | 0x80) << 16)
                exp = (sensor[17] & 0x7f) * 2 + (1 if (sensor[16] & 0x80) else 0)
                if sensor[17] & 0x80:
                    mantis = -mantis
                flt = math.ldexp(mantis, (exp - 127 - 23)) if (mantis or exp) else 0
                self.inclination = flt
                if self.inclination < 0.0:
                    self.inclination = 0.0
                if self.inclination > 180.0:
                    self.inclination = 180.0

                # Gyro
                self.gyroRaw[0] = sensor[18]+sensor[19]*256
                self.gyroRaw[1] = sensor[20]+sensor[21]*256
                self.gyroRaw[2] = sensor[22]+sensor[23]*256

                # Magnetometer
                self.magneticField[0] = float(sensor[24])
                self.magneticField[1] = float(sensor[28])
                self.magneticField[2] = float(sensor[32])

                # Compute abmient light.
                self.lightAvg += sensor[53]+sensor[54]*256
                self.lightAvg += sensor[55]+sensor[56]*256
                self.lightAvg += sensor[57]+sensor[58]*256
                self.lightAvg += sensor[59]+sensor[60]*256
                self.lightAvg += sensor[61]+sensor[62]*256
                self.lightAvg += sensor[63]+sensor[64]*256
                self.lightAvg += sensor[65]+sensor[66]*256
                self.lightAvg += sensor[67]+sensor[68]*256
                self.lightAvg = self.lightAvg/8
                self.lightAvg = 4000 if (self.lightAvg>4000) else self.lightAvg
                if self.lightAvg < 0:
                    self.lightAvg = 0

                # ToF
                self.distanceCm = ((sensor[70]<<8)|(sensor[69]))/10

                # Microphone
                self.micVolume[0] = 1500 if (sensor[71]+sensor[72]*256>1500) else (sensor[71]+sensor[72]*256)
                self.micVolume[1] = 1500 if (sensor[73]+sensor[74]*256>1500) else (sensor[73]+sensor[74]*256)
                self.micVolume[2] = 1500 if (sensor[75]+sensor[76]*256>1500) else (sensor[75]+sensor[76]*256)
                self.micVolume[3] = 1500 if (sensor[77]+sensor[78]*256>1500) else (sensor[77]+sensor[78]*256)
                
                # Battery
                self.batteryRaw = sensor[83]+sensor[84]*256

                # print('self.proximity: ', self.proximity, 
                # ' self.acceleration: ', self.acceleration, 
                # ' self.orientation: ', self.orientation,
                # ' self.inclination: ', self.inclination,
                # ' self.gyroRaw: ', self.gyroRaw,
                # ' self.magneticField: ', self.magneticField,
                # ' self.lightAvg: ', self.lightAvg, 
                # ' self.distanceCm: ', self.distanceCm,
                # ' self.micVolume: ', self.micVolume, 
                # ' self.batteryRaw: ', self.batteryRaw
                # )
                #print("prox0 = " + str(proximity[0]))
                #print("prox1 = " + str(proximity[1]))
                #print("prox2 = " + str(proximity[2]))
                #print("prox3 = " + str(proximity[3]))
                #print("prox4 = " + str(proximity[4]))
                #print("prox5 = " + str(proximity[5]))
                #print("prox6 = " + str(proximity[6]))
                #print("prox7 = " + str(proximity[7]))
                
                # Here goes your controller.
                # This is a simple example that turn on the body led when there is something in front of any of the proximity sensors.
                # if (proximity[client_index][0] >= SENS_THRESHOLD) or (proximity[client_index][1] >= SENS_THRESHOLD) or (proximity[client_index][2] >= SENS_THRESHOLD) or (proximity[client_index][3] >= SENS_THRESHOLD) or (proximity[client_index][4] >= SENS_THRESHOLD) or (proximity[client_index][5] >= SENS_THRESHOLD) or (proximity[client_index][6] >= SENS_THRESHOLD) or (proximity[client_index][7] >= SENS_THRESHOLD):
                #     command[client_index][7] = 0x10;	# lEDs
                #     led_state[client_index] = 1
                # else:
                #     command[client_index][7] = 0x00;	# lEDs
                #     led_state[client_index] = 0
                
                self.num_packets += 1
                        
            elif header == bytearray([3]): # Empty ack
                print(self.client_addr + " received an empty packet\r\n")
            else:
                print(self.client_addr + ": unexpected packet\r\n")
                
            expected_recv_packets -= 1

    def disconnect(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.isConnected = False
        try:
            self.client_sock.close()
            self.mCamera.releaseCamera()
        except:
            pass

    def receive(self, msg_len):
        # myDebug(self.__class__.__name__, get_current_function_name())
        chunks = []
        bytes_recd = 0
        while bytes_recd < msg_len:
            chunk = self.client_sock.recv(min(msg_len - bytes_recd, 2048))
            if chunk == b'':
                self.disconnect()
                raise RuntimeError("Receive error")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)		

    def queryGlobalLocation(self):
        controller = MainController.getController()
        data_tmp = controller.mCameraData.getData('GlobalLocation', self.mId)
        
        if data_tmp is not None:
            data = np.array(controller.mCameraData.getData('GlobalLocation', self.mId), dtype=np.float)
            self.setSelfPos(data)
        
    def setSelfPos(self, data):
        # 目前坐标是左上为原点，单位是比例，需要转换为中间是原点，单位是米
        # 检验控制流程
        self.mPos[:] = data[0:3]
        # if data[5] > 0:
        #     self.mRobotEulerAngle = -180 + data[5]
        # else:
        #     self.mRobotEulerAngle = 180 + data[5]
        self.mRobotEulerAngle = data[5]

        sin_i = math.sin(self.mRobotEulerAngle)
        cos_i = math.cos(self.mRobotEulerAngle)
        self.mOrientation[0, 0] = cos_i
        self.mOrientation[0, 1] = -sin_i
        self.mOrientation[1, 0] = sin_i
        self.mOrientation[1, 1] = cos_i
        self.mOrientation[2, 2] = 1
        

    def feedbackControl(self):
        self.mSpeedWheels = self.expectedWheelsSpeed()

        # 旧代码
        speed1 = 0.0
        speed2 = 0.0
        speed1, speed2 = self.mSpeedWheels
        # if self.mSpeedWheels[0] > self.MAX_SPEED:
        #     speed1 = self.MAX_SPEED
        # elif self.mSpeedWheels[0] < -self.MAX_SPEED:
        #     speed1 = -self.MAX_SPEED
        # else:
        #     speed1 = self.mSpeedWheels[0]
        # if self.mSpeedWheels[1] > self.MAX_SPEED:
        #     speed2 = self.MAX_SPEED
        # elif self.mSpeedWheels[1] < -self.MAX_SPEED:
        #     speed2 = -self.MAX_SPEED
        # else:
        #     speed2 = self.mSpeedWheels[1]
        
        # 黄吉修改代码 start
        if self.mSpeedWheels[0] >= self.mSpeedWheels[1]:  # 等幅值放大或者缩小
            if self.mSpeedWheels[0] > self.MAX_SPEED:
                speed1 = self.MAX_SPEED
                if self.mSpeedWheels[1] < -self.MAX_SPEED:
                    speed2 = -self.MAX_SPEED
                else:
                    speed2 = self.MAX_SPEED * self.mSpeedWheels[1] / self.mSpeedWheels[0]
            elif self.mSpeedWheels[1] < -self.MAX_SPEED:
                speed1 = -self.MAX_SPEED * self.mSpeedWheels[0] / self.mSpeedWheels[1]
                speed2 = -self.MAX_SPEED
            else:
                speed1 = self.mSpeedWheels[0]
                speed2 = self.mSpeedWheels[1]
        else:
            if self.mSpeedWheels[1] > self.MAX_SPEED:
                if self.mSpeedWheels[0] < -self.MAX_SPEED:
                    speed1 = -self.MAX_SPEED
                else:
                    speed1 = self.MAX_SPEED * self.mSpeedWheels[0] / self.mSpeedWheels[1]
                speed2 = self.MAX_SPEED
            elif self.mSpeedWheels[0] < -self.MAX_SPEED:
                speed2 = -self.MAX_SPEED * self.mSpeedWheels[1] / self.mSpeedWheels[0]
                speed1 = -self.MAX_SPEED
            else:
                speed1 = self.mSpeedWheels[0]
                speed2 = self.mSpeedWheels[1]

        # 黄吉修改代码 end

        if self.mState == RobotControlMode.PolicyControl and not self.isTestRobot:
            self.setMotorVelocity(speed1, speed2)
        if self.isTestRobot:
            print('mBeta: {}'.format(format(self.mBeta * 180 / math.pi, '.3f')),
              'mAlpha: {}'.format(format(self.mAlpha * 180 / math.pi, '.3f')),
            #   'mTheta: {}'.format(format(self.mTheta * 180 / math.pi, '.3f')),
              'mTgEulerAng: {}'.format(format(self.mTargetEulerAngle * 180 / math.pi, '.3f')),
              'targrt: {}'.format(self.mTarget),
              'self.mPos: {}'.format([format(self.mPos[0], '.4f'),
                                      format(self.mPos[1], '.4f'),
                                      ]),
              'line_speed: %.4f' % self.mLineSpeed,
              'rotation_speed: %.4f' % self.mRotationSpeed,
              'Speed: {}'.format(['%.2f' % speed1, '%.2f' % speed2]),
            #   'nearTarget: {}'.format(self.nearDestination),
              end='\r')
            pass

    def expectedWheelsSpeed(self) -> np.ndarray: 
        # 现将机器人自身坐标和角度从世界坐标系转换到目标坐标系下

        path_following_control = PathFinderController(self.K_RHO, self.K_ALPHA, self.K_BETA)
        robot_pos = self.mPos * 1000  # 转换为mm
        target_pos = self.mTarget * 1000
        var_pos = target_pos - robot_pos   # replaced
        # print(self.mRobotEulerAngle)
        # print(self.mTargetEulerAngle)
        line_speed, rotation_speed, rho, alpha, beta = path_following_control.calc_control_command(var_pos[0], var_pos[1], self.mRobotEulerAngle, self.mTargetEulerAngle, self.mPreAlpha)
        # print(line_speed, rotation_speed)
        ret: np.ndarray = np.zeros((2), dtype=np.float)

        # self.mX_t = pos_t[0]
        # self.mY_t = pos_t[1]
        line_speed /= 1000
        rotation_speed /= 50

        if abs(line_speed) > self.MAX_SPEED:
            line_speed = np.sign(line_speed) * self.MAX_SPEED

        if abs(rotation_speed) > self.mMaxAngularSpeed:
            rotation_speed = np.sign(rotation_speed) * self.mMaxAngularSpeed

        self.mLineSpeed = line_speed
        self.mRotationSpeed = rotation_speed 

        _l = self.AXLE_LENGTH / 2
        _r = self.WHEEL_RADIUS
 
        # self.mTheta = self.mRobotEulerAngle  # replaced

        self.mAlpha = alpha
        self.mBeta = beta

        self.mPreAlpha = self.mAlpha  # 记录上一时刻的alpha值
        

        # if abs(self.mX_t) < 0.055 and abs(self.mY_t) < 0.06:  # 如果距离目标点小于10cm，to the next target
        #     self.toNextTarget = True

        # if abs(self.mX_t) < 0.011 and abs(self.mY_t) < 0.012 and self.mBeta == 0:  # 如果距离目标点小于2cm，相当于到达目的地
        #     self.nearDestination = True
        #     # ret[0] = (_l * self.K_BETA * self.mBeta) / _r
        #     # ret[1] = - ret[0]
        #     ret[0] = 0    # 此处原地转圈不能实现，两个ret值互为相反数，但是两轮实际执行转速不同。
        #     ret[1] = 0
        # else:
        #     # 计算两轮的输出转速
        #     ret[0] = (self.mLineSpeed + _l * self.mRotationSpeed) / _r
        #     ret[1] = (self.mLineSpeed - _l * self.mRotationSpeed) / _r
        ret[0] = (self.mLineSpeed + _l * self.mRotationSpeed) / _r
        ret[1] = (self.mLineSpeed - _l * self.mRotationSpeed) / _r
        
        return ret

    def setMotorVelocity(self, speed1, speed2):
        speed1_trans = speed1 * 1000 / self.MAX_SPEED
        speed2_trans = speed2 * 1000 / self.MAX_SPEED
        self.setSpeed(int(speed1_trans), int(speed2_trans))

    def rotationMatrixToEulerAngles(self, rotation_mat: np.ndarray):
        eulerAngle = 0.0
        pi = math.pi 
        R21 = rotation_mat[1, 0]
        R22 = rotation_mat[1, 1]
        eulerAngle = math.atan2(R21, R22)
        # if R11 > 0:
        #     pass 
        # elif R21 >= 0 and R11 < 0:
        #     eulerAngle = pi - eulerAngle
        # elif R21 < 0 and R11 < 0:
        #     eulerAngle = -pi - eulerAngle
        # elif R21 > 0 and R11 == 0:
        #     eulerAngle = pi / 2
        # elif R21 < 0 and R11 == 0:
        #     eulerAngle = -pi / 2
        return eulerAngle