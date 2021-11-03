import React, { useEffect, useMemo, useRef, useState } from 'react';
import { observer } from 'mobx-react';
import { View, ScrollView } from 'react-native';

import {
    FloatingCameraButton,
    HeaderButton,
    LoadingModal,
    RBChoiceGroup,
    RecipeItem,
    RecipeList,
} from '../../components';

import { useCameraAction } from '../../customHook/useCameraAction';
import { useScrollTop } from '../../customHook/useScrollTop';
import { blob2base54, cookie2obj, decodeUnicode } from '../../utils';
import { Ingredient } from '../../api';
import { ingredientStore, myFavorStore, recipeStore, recommendRecipeStore } from '../../store';

import ic_search from '../../../assets/icon/ic_search.png';
import ic_info from '../../../assets/icon/ic_info.png';

let lastScroll = 0;


const HomeScreen = ({ route, navigation }) => {
    const params = route.params || {};

    const [active, setActive] = useState(0);
    const [isDetectioning, setIsDetectioning] = useState(false);

    const showAction = useCameraAction();
    const pageRef = useRef();
    const [recommendScrollRef, recScrollToTop] = useScrollTop();
    const [searchScrollRef, searchScrollToTop] = useScrollTop();

    const memorizedRecoomeds = useMemo(() => renderRecommendItem, [recommendRecipeStore.recipes]);
    const memorizedSearchs = useMemo(() => renderSearchItem, [recipeStore.recipes]);

    React.useLayoutEffect(() => {
        navigation.setOptions({
            headerLeft: () => <HeaderButton icon={ic_info} style={{ width: 18, height: 18 }} onPress={() => {}} />,
            headerRight: () => <HeaderButton icon={ic_search} onPress={() => navigation.navigate('Search')} />,
        });
    }, [navigation]);

    useEffect(() => {
        fetchData();
    }, []);

    useEffect(() => {
        if (params.search) {
            setActive(1);
            pageRef.current.scrollToEnd({ animated: false });
        }
    }, [params]);

    async function fetchData() {
        await recommendRecipeStore.fetchList(1, myFavorStore.combinationId);
    }

    async function searchLoadMore() {
        await recipeStore.fetchList({
            page: recipeStore.page + 1,
            combinationId: myFavorStore.combinationId,
            ingredients: recipeStore.ingredients,
            categories: recipeStore.categories,
        });
    }

    function handlePagination(e) {
        const offset = e.nativeEvent.contentOffset.x;
        if (offset === lastScroll) return;

        const isScrollRight = offset > lastScroll;
        lastScroll = offset;
        setActive(Number(!!isScrollRight))
    }

    function scrollToTop(currentActive) {
        if (active !== currentActive) return;
        if (active === 0) recScrollToTop();
        else searchScrollToTop();
    }

    function renderRecommendItem({ item }) {
        return (
            <RecipeItem
                {...item}
                searchIngredients={[]}
                onPress={() => navigation.navigate('Recipe', { recipe: item, search: false })} />
        );
    }

    function renderSearchItem({ item }) {
        return (
            <RecipeItem
                {...item}
                search
                searchIngredients={recipeStore.ingredients.map(v => v.name)}
                onPress={() => navigation.navigate('Recipe', { recipe: item, search: true })} />
        );
    }

    return (
        <>
            <View style={{ padding: 14 }}>
                <RBChoiceGroup
                    choices={['추천', '검색 결과']}
                    active={active}
                    onChange={(i) => {
                        scrollToTop(i);
                        if (i) pageRef.current.scrollToEnd();
                        else pageRef.current.scrollTo({ x: 0, y: 0, animated: true });
                    }} />
            </View>

            <ScrollView
                ref={pageRef}
                horizontal
                pagingEnabled
                bounces={false}
                scrollEventThrottle={10}
                onScroll={(e) => handlePagination(e)}>
                <RecipeList
                    scrollRef={recommendScrollRef}
                    data={recommendRecipeStore.recipes}
                    renderItem={memorizedRecoomeds}
                    isFetching={recommendRecipeStore.isFetching} />
                <RecipeList
                    scrollRef={searchScrollRef}
                    data={recipeStore.recipes}
                    renderItem={memorizedSearchs}
                    isFetching={recipeStore.isFetching}
                    loadMore={searchLoadMore}
                    search />
            </ScrollView>

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
