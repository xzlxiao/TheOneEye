from torch._C import dtype
from Entity.RobotBase import RobotBase
from Algorithm.RobotPolicy import RobotPolicyBase
from Entity.CameraCellphone import CameraCellphone
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


# class RobotControlMode(Enum):
#     RemoteControl = 0
#     PolicyControl = 1


class RobotCellphone(RobotBase):
    def __init__(self, parent, population, pos=np.array((0, 0, 0), dtype=np.float), orientation = np.zeros((3,3), dtype=np.float)) -> None:
        myDebug(self.__class__.__name__, get_current_function_name())
        super().__init__(parent)
        self.mRobotType = "RobotEpuck"
        # self.mState = RobotControlMode.PolicyControl
        self.mCamera = CameraCellphone(self)
        self.mPopulation = population
        self.mPos = np.array(pos, dtype=np.float)
        self.mOrientation = np.array(orientation, dtype=np.float)
        # self.mSpeedWheels:np.ndarray = np.zeros((1, 2), dtype=np.float)

        # self.mTargetEulerAngle = 0.0      # 世界坐标系下目标角度
        # self.mRobotEulerAngle  = 0.0      # 世界坐标系下机器人角度
        # self.mX_t  = 0.0                  # 目标坐标系下机器人坐标
        # self.mY_t  = 0.0                  # 目标坐标系下机器人坐标
        # self.mLineSpeed = 0.0
        # self.mRotationSpeed = 0.0
        # self.mAlpha = 0.0
        # self.mTheta = 0.0
        # self.mBeta = 0.0

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

        # 参数
        # self.MAX_SPEED = float(XSetting.getValue('Epuck/MAX_SPEED'))
        # self.WHEEL_RADIUS = float(XSetting.getValue('Epuck/WHEEL_RADIUS'))
        # self.AXLE_LENGTH = float(XSetting.getValue('Epuck/AXLE_LENGTH'))
        # self.K_RHO = float(XSetting.getValue('Epuck/K_RHO'))
        # self.K_ALPHA = float(XSetting.getValue('Epuck/K_ALPHA'))
        # self.K_BETA = float(XSetting.getValue('Epuck/K_BETA'))

    def initCommand(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        pass

    def setTarget(self, target):
        super().setTarget(target)
        pass

    # def setSpeed(self, motor_L, motor_R):
    #     # myDebug(self.__class__.__name__, get_current_function_name())
    #     if motor_L >= 0:
    #         self.mCommand[4] = motor_L//256
    #         self.mCommand[3] = abs(motor_L)%256
    #     else:
    #         self.mCommand[4] = 255-(abs(motor_L)//256)
    #         self.mCommand[3] = abs(motor_L+1)%256
    #     if motor_R >= 0:
    #         self.mCommand[6] = motor_R//256
    #         self.mCommand[5] = abs(motor_R)%256
    #     else:
    #         self.mCommand[6] = 255-(abs(motor_R)//256)
    #         self.mCommand[5] = abs(motor_R+1)%256
        
        

    def update(self):
        """

        :return:
        """
        # myDebug(self.__class__.__name__, get_current_function_name())
        # If there was some errors in sending or receiving then try to close the connection and reconnect.
        if not self.isConnected:
            self.socket_error = 0
            self.connect(self.client_addr)

        if self.mPolicy is not None:
            self.mPolicy.update()
        
        # Send a command to the robot.
        self.sendCommand(self.getCommand(), COMMAND_PACKET_SIZE)
        self.getState()
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
        pass
        
    