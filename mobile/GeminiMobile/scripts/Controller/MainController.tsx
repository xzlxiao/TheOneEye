import * as React from 'react';
import {
	Alert,
} from 'react-native';

export class MainController{

    private static controller = new MainController();
    private constructor(){}
    
    public static getInstance()
    {
        return MainController.controller;
    }

    public print(): void
    {
        Alert.alert("this is MainController");
    }

}
