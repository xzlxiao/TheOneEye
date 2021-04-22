from Entity.RobotBase import RobotBase
from Entity.CameraEPuck import CameraEPuck
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

TCP_PORT = 1000 # This is fixed.
MAX_NUM_CONN_TRIALS = 5
COMMAND_PACKET_SIZE = 21
HEADER_PACKET_SIZE = 1
IMAGE_PACKET_SIZE = 38400 # Max buffer size = 160x120x2
SENSORS_PACKET_SIZE = 104
class RobotEpuck(RobotBase):
    def __init__(self, parent, population, pos=np.array((0, 0, 0, 0, 0, 0, 0), dtype=np.float)) -> None:
        myDebug(self.__class__.__name__, get_current_function_name())
        super().__init__(parent)
        self.mState = 0
        self.mCamera = CameraEPuck(self)
        self.mPopulation = population
        self.mPos = np.array(pos, dtype=float)
        # self.mTObsacle = target_obstacle    # 目标障碍物
        self.client_sock = 1000
        self.client_addr = "192.168.1.100"
        self.isConnected = False
        self.socket_error = 0
        self.isFirstConnect = True
        self.proximity = [100.0]*8
        self.num_packets = 0
        self.mCommand = bytearray([0] * COMMAND_PACKET_SIZE)
        self.initCommand()

    def initCommand(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mCommand[0] = 0x80	# Packet id for settings actuators
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
        if not self.isConnected:
            self.socket_error = 0
            self.connect(self.client_addr)
        
        # Send a command to the robot.
        self.sendCommand(self.getCommand(), COMMAND_PACKET_SIZE)	
        self.getState()
        
        self.move()

    def move(self):
        # myDebug(self.__class__.__name__, get_current_function_name())
        pass

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
                self.mId = self.client_addr
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
