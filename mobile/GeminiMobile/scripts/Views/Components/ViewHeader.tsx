import React from 'react';
import { Component } from 'react';
import { View, 
    Text, 
    Button,
    TextInput, 
    Alert,
    StyleSheet,
} from 'react-native';
import Ionicons from 'react-native-vector-icons/Ionicons';

class ViewHeader extends Component 
{
    state = { mTitle: "" }
    on_list_button_press(): void 
    {
        Alert.alert('list_button_press');
    }

    on_search_button_press(): void 
    {
        Alert.alert('search_button_press');
    }

    on_sort_button_press(): void 
    {
        Alert.alert('sort_button_press');
    }

    render() 
    {
        return (
            <View style={styles.container}>
                <Ionicons style={styles.list_button} onPress={this.on_list_button_press} name="list-outline" size={30} color="black" />
                <Text style={styles.title}>测试</Text>
                <Ionicons style={styles.search_button} onPress={this.on_search_button_press} name="search" size={30} color="black" />
                <Ionicons style={styles.sort_button} onPress={this.on_sort_button_press} name="filter" size={30} color="black" />
            </View>
        );
    }
}

const styles = StyleSheet.create(
    {
        container:{
            margin: 0,
            width: '100%',
            justifyContent: 'space-between',
            flexDirection: "row",
            // flexWrap: "nowrap"
        },

        title: {
            flex: 4,
            textAlign: 'center'
        },

        list_button:{
            flex: 0.5,
            position: 'relative',
            left: "50%",
        },

        search_button: {
            flex: 0.5,
            position: 'relative',
            marginRight: 0,
            right: "50%",
        },

        sort_button:{
            flex: 0.5,
            position: 'relative',
            marginRight: 0,
            right: "50%",
        }
    }
)

export default ViewHeader;