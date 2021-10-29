import React, { useEffect, useState } from 'react';
import { observer } from 'mobx-react';
import { ActivityIndicator, FlatList, Image, Text, View } from 'react-native';

import {
    FloatingCameraButton,
    HeaderButton,
    LoadingModal,
    RBChoiceGroup,
    RecipeList,
} from '../../components';

import { useCameraAction } from '../../customHook/useCameraAction';
import { blob2base54, cookie2obj, decodeUnicode } from '../../utils';
import { Ingredient } from '../../api';
import { ingredientStore, recipeStore, recommendRecipeStore } from '../../store';

import ic_search from '../../../assets/icon/ic_search.png';
import no_result from '../../../assets/no_result.png';
import { MainTheme } from '../../styles/themes';


const HomeScreen = ({ route, navigation }) => {
    const params = route.params || {};

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

    useEffect(() => {
        if (params.search) setActive(1);
    }, [params]);

    async function fetchData() {
        await recommendRecipeStore.fetchList(1);
    }

    async function handleRefresh() {
        setIsRefreshing(true);

        if (active === 0) {
            await recommendRecipeStore.refresh();
        } else if (active === 1) {
            await recipeStore.refresh();
        }

        setIsRefreshing(false);
    }

    async function handleLoadMore() {
        if (active === 0) {
            await recommendRecipeStore.fetchList(recommendRecipeStore.page + 1);
        } else {
            await recipeStore.fetchList({
                page: recipeStore.page + 1,
                favors: recipeStore.favors,
                ingredients: recipeStore.ingredients,
                categories: recipeStore.categories,
            });
        }
    }

    return (
        <>
            <FlatList
                contentContainerStyle={{ padding: 14, paddingBottom: 70, minHeight: '100%' }}
                data={active === 0 ? recommendRecipeStore.recipes : recipeStore.recipes}
                keyExtractor={(item, idx) => `recipe_${item.id}_${idx}`}
                refreshing={isRefreshing}
                onRefresh={handleRefresh}
                onEndReached={handleLoadMore}
                onEndReachedThreshold={2}
                removeClippedSubviews={true}
                legacyImplementation={true}
                ListHeaderComponent={() => (
                    <RBChoiceGroup
                        style={{ marginBottom: 14 }}
                        choices={['추천', '검색 결과']}
                        active={active}
                        onChange={(i) => setActive(i)} />
                )}
                ListEmptyComponent={() => (
                    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
                        {!(recipeStore.isFetching || recommendRecipeStore.isFetching) &&
                            <>
                                <Image style={{ width: 100, height: 100, marginTop: -10 }} source={no_result} />
                                <Text style={{ padding: 15, fontSize: 16, color: '#777777', fontWeight: 'bold' }}>레시피가 없어요</Text>
                            </>
                        }
                        {(recipeStore.isFetching || recommendRecipeStore.isFetching) &&
                            <ActivityIndicator
                                animating={true}
                                size='large'
                                color={MainTheme.colors.primary} />
                        }
                    </View>
                )}
                renderItem={({ item }) => (
                    <RecipeList
                        {...item}
                        searchIngredients={active === 1 ? recipeStore.ingredients.map(v => v.name) : []}
                        onPress={() => navigation.navigate('Recipe', { recipe: item })} />
                )} />

            <LoadingModal visible={isDetectioning} text='식재료를 확인하고 있어요' />

            <FloatingCameraButton onPress={() => {
                showAction(async (res) => {
                    if (res.cancelled) return;

                    setIsDetectioning(true);
                    const result = await Ingredient.detectIngredientFromImage(res.uri);
                    const cookie = result.headers['set-cookie'][0];
                    const base54 = await blob2base54(result.data);
                    setIsDetectioning(false);

                    let { ingredients } = cookie2obj(cookie);
                    ingredients = decodeUnicode(ingredients);
                    ingredients = ingredients.split(',');
                    ingredients = ingredientStore.ingredients.filter(v => ingredients.indexOf(v.name) > -1);

                    navigation.navigate('Detection', { images: [base54], ingredients });
                });
            }} />
        </>
    );
}

export default observer(HomeScreen);
