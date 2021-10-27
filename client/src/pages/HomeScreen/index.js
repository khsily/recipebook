import React, { useEffect, useState } from 'react';
import { observer } from 'mobx-react';
import { FlatList, Image, Text, View } from 'react-native';

import {
    FloatingCameraButton,
    HeaderButton,
    LoadingModal,
    RBChoiceGroup,
    RecipeList,
} from '../../components';

import { useCameraAction } from '../../customHook/useCameraAction';
import { blob2base54, cookie2obj, fakeLoading } from '../../utils';
import { Ingredient } from '../../api';
import { recommendRecipeStore } from '../../store';

import ic_search from '../../../assets/icon/ic_search.png';
import no_result from '../../../assets/no_result.png';


const HomeScreen = ({ navigation }) => {
    const [active, setActive] = useState(0);
    const [isRefreshing, setIsRefreshing] = useState(false);
    const [isDetectioning, setIsDetectioning] = useState(false);
    const showAction = useCameraAction();

    React.useLayoutEffect(() => {
        navigation.setOptions({
            headerRight: () => (
                <HeaderButton icon={ic_search} onPress={() => navigation.navigate('Search')} />
            )
        });
    }, [navigation]);

    useEffect(() => {
        fetchData();
    }, []);

    async function fetchData() {
        await recommendRecipeStore.fetchList(1);
    }

    async function handleRefresh() {
        setIsRefreshing(true);
        await fakeLoading(2000);
        console.log('refreshed');
        setIsRefreshing(false);
    }

    return (
        <>
            <FlatList
                contentContainerStyle={{ padding: 14, paddingBottom: 70, minHeight: '100%' }}
                data={active === 0 ? recommendRecipeStore.recipes : []}
                keyExtractor={item => `recipe_${item.id}`}
                refreshing={isRefreshing}
                onRefresh={handleRefresh}
                ListHeaderComponent={() => (
                    <RBChoiceGroup
                        style={{ marginBottom: 14 }}
                        choices={['추천', '검색 결과']}
                        active={active}
                        onChange={(i) => setActive(i)} />
                )}
                ListEmptyComponent={() => (
                    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
                        <Image style={{ width: 100, height: 100, marginTop: -10 }} source={no_result} />
                        <Text style={{ padding: 15, fontSize: 16, color: '#777777', fontWeight: 'bold' }}>레시피가 없어요</Text>
                    </View>
                )}
                renderItem={({ item }) => (
                    <RecipeList {...item} onPress={() => navigation.navigate('Recipe', { recipe: item })} />
                )} />

            <LoadingModal visible={isDetectioning} text='식재료를 확인하고 있어요' />

            <FloatingCameraButton onPress={() => {
                showAction(async (res) => {
                    if (res.cancelled) return;

                    setIsDetectioning(true);
                    const result = await Ingredient.detectIngredientFromImage(res.uri);
                    const cookie = result.headers['set-cookie'][0];
                    const { ingredients } = cookie2obj(cookie);
                    const base54 = await blob2base54(result.data);
                    setIsDetectioning(false);

                    navigation.navigate('Detection', { images: [base54], ingredients: [{ id: 1, name: '사과' }] });
                });
            }} />
        </>
    );
}

export default observer(HomeScreen);
