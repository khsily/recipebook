import React from 'react';
import { registerRootComponent } from 'expo';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { ActionSheetProvider } from '@expo/react-native-action-sheet'
import { StatusBar } from 'react-native';
import { useFonts } from 'expo-font';

import {
    HomeScreen,
    SearchScreen,
    RecipeScreen,
} from './pages';
import { header_style, transition_style } from './styles/common';
import { MainTheme } from './styles/themes';
import { typography } from './utils';

const Stack = createStackNavigator();

const app = () => {
    const [loaded] = useFonts({
        AppleSDGothicNeoM: require('../assets/fonts/AppleSDGothicNeoM.ttf'),
    });

    if (!loaded) return null;
    typography();

    return (
        <NavigationContainer theme={MainTheme}>
            <StatusBar barStyle="light-content" backgroundColor={MainTheme.colors.primary} />
            <ActionSheetProvider>
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
            </ActionSheetProvider>
        </NavigationContainer>
    );
}
export default registerRootComponent(app)