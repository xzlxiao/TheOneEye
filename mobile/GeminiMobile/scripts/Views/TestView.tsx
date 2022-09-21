import React, { useState, useEffect } from 'react';
import { RNCamera } from 'react-native-camera';
import { Component, PureComponent } from 'react';
import {
    View,
    Text,
    Button,
    TextInput,
    Alert,
    ScrollView,
    StyleSheet,
    Image,
    TouchableHighlight,
    TouchableOpacity
} from 'react-native';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import { NavigationContainer } from '@react-navigation/native';
// import { createStackNavigator } from '@react-navigation/stack';
import { MainController } from '../Controller/MainController';
import ViewHeader from './Components/ViewHeader';
import Ionicons from 'react-native-vector-icons/Ionicons';
// import { Camera, frameRateIncluded, useCameraDevices} from 'react-native-vision-camera';
// import { Camera, CameraType } from 'expo-camera';

// const devices = useCameraDevices('wide-angle-camera');

// const TestView = (props) => {
//     const [hasPermission, setHasPermission] = useState(false);
//     const [type, setType] = useState(CameraType.back);

//     useEffect(() => {
//         (async () => {
//         const { status } = await Camera.requestCameraPermissionsAsync();
//         setHasPermission(status === 'granted');
//         })();
//     }, []);

//     if (hasPermission === null) {
//         return <View />;
//     }
//     if (hasPermission === false) {
//         return <Text>No access to camera</Text>;
//     }

//     return (
//         <View style={styles.container}>
//             <Camera style={styles.camera} type={type}>
//                 <View style={styles.buttonContainer}>
//                     <TouchableOpacity
//                         style={styles.button}
//                         onPress={() => {
//                             setType(type === CameraType.back ? CameraType.front : CameraType.back);
//                         }}>
//                         <Text style={styles.text}> Flip </Text>
//                     </TouchableOpacity>
//                 </View>
//             </Camera>
//         </View>
//     );

// }

class TestView extends PureComponent {
    state = {
        postText: '',
        takingPic: false,
    };
    // device = devices.back;
    // useEffect(() => {
    // (async () => {
    //     const { status } = await Camera.requestCameraPermissionsAsync();
    //     setHasPermission(status === 'granted');
    // })();
    // }, []);

    // constructor(props) {
    //     super(props);
    //     this.state = {
    //         takingPic: false,
    //     };
    // }
    takePicture = async () => {
        if (this.camera && !this.state.takingPic) {

            let options = {
                quality: 0.85,
                fixOrientation: true,
                forceUpOrientation: true,
            };

            this.setState({ takingPic: true });

            try {
                this.camera.resumePreview();
                const data = await this.camera.takePictureAsync(options);
                Alert.alert('Success', JSON.stringify(data));
            } catch (err) {
                Alert.alert('Error', 'Failed to take picture: ' + (err.message || err));
                return;
            } finally {
                this.setState({ takingPic: false });
            }
        }
    };
    render() {
        return (
            <View style={styles.container}>
                <RNCamera
                ref={ref => {
                    this.camera = ref;
                }}
                captureAudio={false}
                style={{ flex: 1 }}
                type={RNCamera.Constants.Type.back}
                androidCameraPermissionOptions={{
                    title: 'Permission to use camera',
                    message: 'We need your permission to use your camera',
                    buttonPositive: 'Ok',
                    buttonNegative: 'Cancel',
                }} />
                <Button title="拍照" style={styles.button} onPress={this.takePicture}/>
            </View>
            
        );
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    camera: {
        flex: 1,
    },
    buttonContainer: {
        flex: 1,
        backgroundColor: 'transparent',
        flexDirection: 'row',
        margin: 20,
    },
    button: {
        flex: 0.1,
        alignSelf: 'flex-end',
        alignItems: 'center',
    },
    text: {
        fontSize: 18,
        color: 'white',
    },
});

export default TestView;