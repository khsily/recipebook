import React from 'react';
import { registerRootComponent } from 'expo';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'react-native';

import {
    HomeScreen,
    SearchScreen,
    RecipeScreen,
} from './pages';
import { header_style, transition_style } from './styles/common';
import { MainTheme } from './styles/themes';

const Stack = createStackNavigator();

const app = () => (
    <NavigationContainer theme={MainTheme}>
        <StatusBar barStyle="light-content" backgroundColor={MainTheme.colors.primary} />
        <Stack.Navigator
            initialRouteName='Home'
            screenOptions={{ ...header_style, ...transition_style }}>
            <Stack.Screen
                name="Home"
                component={HomeScreen}
                options={{ title: '라따뚜이' }} />
            <Stack.Screen
                name="Search"
                component={SearchScreen}
                options={{ title: '검색 설정' }} />
            <Stack.Screen
                name="Recipe"
                component={RecipeScreen}
                options={{ title: '레시피 정보' }} />
        </Stack.Navigator>
    </NavigationContainer>
)

export default registerRootComponent(app)