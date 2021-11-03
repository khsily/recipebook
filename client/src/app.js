import React from 'react';
import { registerRootComponent } from 'expo';
import { NavigationContainer } from '@react-navigation/native';
import { createSharedElementStackNavigator } from 'react-navigation-shared-element';
import { ActionSheetProvider } from '@expo/react-native-action-sheet'
import { Platform, StatusBar } from 'react-native';
import * as Font from 'expo-font';
import { observer } from 'mobx-react';

import {
    HomeScreen,
    SearchScreen,
    RecipeScreen,
    DetectionResultScreen,
    FavorScreen,
    AddScreen,
} from './pages';
import { header_style, transition_style } from './styles/common';
import { MainTheme } from './styles/themes';
import { typography } from './utils';
import { fetchInitalData, myFavorStore } from './store';
import { useSplash } from './customHook/useSplash';

const Stack = createSharedElementStackNavigator();


const app = () => {
    // 초기 데이터 가져오기
    const appIsReady = useSplash(async () => {
        await Font.loadAsync({
            AppleSDGothicNeoM: require('../assets/fonts/AppleSDGothicNeoM.ttf'),
            AppleSDGothicNeoB: require('../assets/fonts/AppleSDGothicNeoB.ttf'),
        });

        // await myFavorStore.clear();   // 임시 (테스트용)
        await fetchInitalData();
        typography();
    });

    if (!appIsReady) return null;

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
                                name="Add"
                                component={AddScreen}
                                options={{ title: '추가', ...header_style, ...transition_style }} />
                            <Stack.Screen
                                name="Recipe"
                                component={RecipeScreen}
                                options={{ title: '레시피 정보', ...header_style, ...transition_style }}
                                sharedElements={(route, _, showing) => {
                                    if (Platform.OS === 'ios' && !showing) return;
                                    const { recipe, search } = route.params;
                                    return [`recipe.${search}.${recipe.id}.photo`];
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