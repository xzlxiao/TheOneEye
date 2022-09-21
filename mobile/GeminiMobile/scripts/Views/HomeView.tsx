import React from 'react';
import { Component } from 'react';
import { View, 
    Text, 
    Button,
    TextInput, 
    Alert,
    ScrollView,
    StyleSheet,
    Image,
} from 'react-native';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import { NavigationContainer } from '@react-navigation/native';
// import { createStackNavigator } from '@react-navigation/stack';
import { MainController } from '../Controller/MainController';
import ViewHeader from './Components/ViewHeader';
import Ionicons from 'react-native-vector-icons/Ionicons';

// function NotificationsScreen({ navigation }) {
//     return (
//       <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
//         <Button onPress={() => navigation.goBack()} title="Go back home" />
//       </View>
//     );
//   }

// 侧边菜单(抽屉) https://www.cnblogs.com/crazycode2/p/9537518.html



// function HomeView({ route, navigation }) {
//     /* 2. Get the param */
//     const [postText, setPostText] = React.useState('');
// 	return (
//         <SafeAreaView
//             style={{ flex: 1, justifyContent: 'space-between', alignItems: 'center' }}
//         >
//             <ViewHeader/>
//             <Text>HomeView</Text>
//             <Text>This is bottom text.</Text>
//             {/* <Backdrop/> */}
//             <Button title="打开抽屉" onPress={() => MainController.getInstance().print()}/>
//         </SafeAreaView>
        
//     );
// }

class HomeView extends Component
{
    state = { postText: '' };

    render() 
    {
        return(
            <SafeAreaView
                style={styles.SafeAreaView}
            >
                <ViewHeader/>
                <Text>HomeView</Text>
                <Text>This is bottom text.</Text>
                {/* <Backdrop/> */}
                <Button title="打开抽屉" onPress={() => MainController.getInstance().print()}/>
            </SafeAreaView>
        );
    }
}

const styles = StyleSheet.create({
    SafeAreaView: {
        flex: 1,
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    container: {
    flex: 1,
    },
    listTitle: {
    color: '#FFF',
    },
    backdropStyle: {
    backgroundColor: '#F4F4F5',
    },
});

export default HomeView;