/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * Generated with the TypeScript template
 * https://github.com/react-native-community/react-native-template-typescript
 *
 * @format
 */
import { Camera, frameRateIncluded } from 'react-native-vision-camera';
import {
    CameraDeviceFormat,
    CameraRuntimeError,
    FrameProcessorPerformanceSuggestion,
    PhotoFile,
    sortFormats,
    useCameraDevices,
    useFrameProcessor,
    VideoFile,
    CameraPermissionStatus,
} from 'react-native-vision-camera';
import React, { type PropsWithChildren, useEffect, useState } from 'react';
import {
    ScrollView,
    Settings,
    StatusBar,
    StyleSheet,
    Text,
    useColorScheme,
    View,
    PermissionsAndroid,
    Platform,
    Alert,
} from 'react-native';

import {
    Colors,
    DebugInstructions,
    Header,
    LearnMoreLinks,
    ReloadInstructions,
} from 'react-native/Libraries/NewAppScreen';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Ionicons from 'react-native-vector-icons/Ionicons';
import HomeView from './scripts/Views/HomeView';
import SettingsView from './scripts/Views/SettingsView';
// import TestView from './scripts/Views/TestView';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';

const Section: React.FC<
    PropsWithChildren<{
        title: string;
    }>
> = ({ children, title }) => {
    const isDarkMode = useColorScheme() === 'dark';
    return (
        <View style={styles.sectionContainer}>
            <Text
                style={[
                    styles.sectionTitle,
                    {
                        color: isDarkMode ? Colors.white : Colors.black,
                    },
                ]}>
                {title}
            </Text>
            <Text
                style={[
                    styles.sectionDescription,
                    {
                        color: isDarkMode ? Colors.light : Colors.dark,
                    },
                ]}>
                {children}
            </Text>
        </View>
    );
};

const Tab = createBottomTabNavigator();

const App = (): React.ReactElement | null => {
    const isDarkMode = useColorScheme() === 'dark';
    const [cameraPermission, setCameraPermission] = useState<CameraPermissionStatus>();
    const [microphonePermission, setMicrophonePermission] = useState<CameraPermissionStatus>();

    const backgroundStyle = {
        backgroundColor: isDarkMode ? Colors.darker : Colors.lighter,
    };

    useEffect(() => {
        Camera.getCameraPermissionStatus().then(setCameraPermission);
        Camera.getMicrophonePermissionStatus().then(setMicrophonePermission);
    }, []);

    console.log(`Re-rendering Navigator. Camera: ${cameraPermission} | Microphone: ${microphonePermission}`);

    const showPermissionsPage = cameraPermission !== 'authorized' || microphonePermission === 'not-determined';
    return (
        <SafeAreaProvider>
            {/* <StatusBar barStyle={isDarkMode ? 'light-content' : 'dark-content'} /> */}
            <NavigationContainer>
                <Tab.Navigator
                    screenOptions={({ route }) => ({
                        tabBarIcon: ({ focused, color, size }) => {
                            let iconName: string = '';

                            if (route.name === 'Home') {
                                iconName = focused
                                    ? 'nuclear'
                                    : 'nuclear-outline';
                            }
                            else if (route.name === 'Settings') {
                                iconName = focused ? 'person' : 'person-outline';
                            }
                            else if (route.name === 'Test') {
                                iconName = focused ? 'terminal' : 'terminal-outline';
                            }

                            // You can return any component that you like here!
                            return <Ionicons name={iconName} size={size} color={color} />;
                        },
                        tableActiveTintColor: 'tomato',
                        tableInactiveTintColor: 'gray',
                        tableStyle: [
                            {
                                "display": "flex"
                            },

                        ]
                    })}
                >
                    <Tab.Screen name="Home" component={HomeView} />
                    {/* <Tab.Screen name="Test" component={TestView} /> */}
                    <Tab.Screen name="Settings" component={SettingsView} />
                </Tab.Navigator>
            </NavigationContainer>

        </SafeAreaProvider>
    );
};

// function App() {
//     // const devices = useCameraDevices('wide-angle-camera')
//     const devices = useCameraDevices()
//     const device = devices.back 
//     // 从相机中选择

//     const frameProcessor = useFrameProcessor((frame) => {
//         console.log('frameProcessor');
//         // 处理图像frame
//     }, [])
//     console.log('test');
    
//     if(Platform.OS === 'android'){
//         PermissionsAndroid.request(PermissionsAndroid.PERMISSIONS.CAMERA)
//             .then(res => {
//                 if(res !== 'granted') {
//                     Alert.alert('相机权限没打开', '请在手机的“设置”选项中,允许访问您的摄像头和麦克风')
//                 }
//                 else
//                 {
//                     console.log('相机权限已打开');
//                     if (device == null) return <Text>loading</Text>
//                     return (
//                     <Camera
//                         style={StyleSheet.absoluteFill}
//                         device={device}
//                         isActive={true}
//                         frameProcessor={frameProcessor}
//                     />
//                     )
//                 }
//             });
//     } else {
//         if(Camera){
//             Camera.getCameraPermissionStatus()
//                 .then(access => {
//                     if(!access) {
//                         Alert.alert('相机权限没打开', '请在iPhone的“设置-隐私”选项中,允许访问您的摄像头和麦克风')
//                     }
//                     else 
//                     {
//                         console.log('成功打开');
//                         if (device == null) return <Text>loading</Text>
//                         return (
//                         <SafeAreaView
//                             style={styles.SafeAreaView}
//                         >
//                             <Text>Camera</Text>
//                             {/* <Camera
//                                 style={StyleSheet.absoluteFill}
//                                 device={device}
//                                 isActive={true}
//                                 frameProcessor={frameProcessor}
//                             /> */}
//                         </SafeAreaView>
                        
//                         )
//                     }
//                 });
//         }
//     }

  
    
//   }

const styles = StyleSheet.create({
    SafeAreaView: {
        flex: 1,
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    sectionContainer: {
        marginTop: 32,
        paddingHorizontal: 24,
    },
    sectionTitle: {
        fontSize: 24,
        fontWeight: '600',
    },
    sectionDescription: {
        marginTop: 8,
        fontSize: 18,
        fontWeight: '400',
    },
    highlight: {
        fontWeight: '700',
    },
});
export default App;

