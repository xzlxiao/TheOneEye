import React from 'react';
import { Component } from 'react';
import { View, 
    Text, 
    Button,
    TextInput, 
    Alert,
    StyleSheet,
} from 'react-native';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import { NavigationContainer } from '@react-navigation/native';
// import { createStackNavigator } from '@react-navigation/stack';


class SettingsView extends Component 
{
    state = {postText: ''};
    render()
    {
        return(
            <SafeAreaView
                style={{ flex: 1, justifyContent: 'space-between', alignItems: 'center' }}
            >
                <Text>SettingsView</Text>
                <Text>This is bottom text.</Text>
            </SafeAreaView>
        );
    };
}

const styles = StyleSheet.create({
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
export default SettingsView;