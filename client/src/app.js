import React, { useEffect, useState } from 'react';
import { registerRootComponent } from 'expo';
import { NavigationContainer } from '@react-navigation/native';
import { createSharedElementStackNavigator } from 'react-navigation-shared-element';
import { ActionSheetProvider } from '@expo/react-native-action-sheet'
import { Platform, StatusBar } from 'react-native';
import { useFonts } from 'expo-font';
import { observer } from 'mobx-react';

import {
    HomeScreen,
    SearchScreen,
    RecipeScreen,
    DetectionResultScreen,
    FavorScreen,
    SplashScreen,
} from './pages';
import { header_style, transition_style } from './styles/common';
import { MainTheme } from './styles/themes';
import { typography } from './utils';
import { fetchInitalData, myFavorStore } from './store';

const Stack = createSharedElementStackNavigator();


const app = () => {
    const [appIsReady, setAppIsReady] = useState(false);
    const [fontLoaded] = useFonts({
        AppleSDGothicNeoM: require('../assets/fonts/AppleSDGothicNeoM.ttf'),
        AppleSDGothicNeoB: require('../assets/fonts/AppleSDGothicNeoB.ttf'),
    });

    // 초기 데이터 가져오기
    useEffect(() => {
        // myFavorStore.clear();   // 임시 (테스트용)
        fetchInitalData().then(() => setAppIsReady(true));
    }, []);

    // TODO: expo splash screen 적용
    if (!fontLoaded || !appIsReady) return null;
    typography();

    return (
        <NavigationContainer theme={MainTheme}>
            <StatusBar barStyle="light-content" backgroundColor={MainTheme.colors.primary} />
            <ActionSheetProvider>
                <Stack.Navigator>
                    {myFavorStore.favors.length === 0 ?
                        <>
                            <Stack.Screen
                                name="Favor"
                                component={FavorScreen}
                                options={{ title: '선호 메뉴 선택', ...header_style, ...transition_style }} />
                        </>
                        :
                        <>
                            <Stack.Screen
                                name="Home"
                                component={HomeScreen}
                                options={{ title: '라따뚜이', ...header_style, ...transition_style }} />
                            <Stack.Screen
                                name="Search"
                                component={SearchScreen}
                                options={{ title: '검색 설정', ...header_style, ...transition_style }} />
                            <Stack.Screen
                                name="Recipe"
                                component={RecipeScreen}
                                options={{ title: '레시피 정보', ...header_style, ...transition_style }}
                                sharedElements={(route, _, showing) => {
                                    if (Platform.OS === 'ios' && !showing) return;
                                    const { recipe } = route.params;
                                    return [`recipe.${recipe.id}.photo`];
                                }} />
                            <Stack.Screen
                                name="Detection"
                                component={DetectionResultScreen}
                                options={{ presentation: 'modal', headerShown: false }} />
                        </>
                    }
                </Stack.Navigator>
            </ActionSheetProvider>
        </NavigationContainer>
    );
}
export default registerRootComponent(observer(app))