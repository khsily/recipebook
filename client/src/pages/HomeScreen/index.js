import React, { useEffect, useState } from 'react';
import { observer } from 'mobx-react';
import { FlatList } from 'react-native';

import {
    FloatingCameraButton,
    HeaderButton,
    LoadingModal,
    RBChoiceGroup,
    RecipeList,
} from '../../components';

import { useCameraAction } from '../../customHook/useCameraAction';
import ic_search from '../../../assets/icon/ic_search.png';
import { blob2base54, cookie2obj, fakeLoading } from '../../utils';
import { Ingredient } from '../../api';
import { recommendRecipeStore } from '../../store';

const data = [
    {
        thumbnail: 'https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg',
        title: '참치김치찌개 황금레시피 맛있게  끓여먹어요',
        ingredients: ['닭고기', '양파', '양배추', '대파', '깻잎', '후추', '떡볶이용 떡', '고구마', '당근', '생강술'],
        category: '한식',
        views: 1001230,
        id: 1,
    },
    {
        thumbnail: 'https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg',
        title: '참치김치찌개 황금레시피 맛있게  끓여먹어요',
        ingredients: ['닭고기', '양파', '양배추', '대파', '깻잎', '후추', '떡볶이용 떡', '고구마', '당근', '생강술'],
        category: '한식',
        views: 1001230,
        id: 2,
    },
    {
        thumbnail: 'https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg',
        title: '참치김치찌개 황금레시피 맛있게  끓여먹어요',
        ingredients: ['닭고기', '양파', '양배추', '대파', '깻잎', '후추', '떡볶이용 떡', '고구마', '당근', '생강술'],
        category: '한식',
        views: 1001230,
        id: 3,
    },
    {
        thumbnail: 'https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg',
        title: '참치김치찌개 황금레시피 맛있게  끓여먹어요',
        ingredients: ['닭고기', '양파', '양배추', '대파', '깻잎', '후추', '떡볶이용 떡', '고구마', '당근', '생강술'],
        category: '한식',
        views: 1001230,
        id: 4,
    },
    {
        thumbnail: 'https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg',
        title: '참치김치찌개 황금레시피 맛있게  끓여먹어요',
        ingredients: ['닭고기', '양파', '양배추', '대파', '깻잎', '후추', '떡볶이용 떡', '고구마', '당근', '생강술'],
        category: '한식',
        views: 1001230,
        id: 5,
    },
    {
        thumbnail: 'https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg',
        title: '참치김치찌개 황금레시피 맛있게  끓여먹어요',
        ingredients: ['닭고기', '양파', '양배추', '대파', '깻잎', '후추', '떡볶이용 떡', '고구마', '당근', '생강술'],
        category: '한식',
        views: 1001230,
        id: 6,
    },
    {
        thumbnail: 'https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg',
        title: '참치김치찌개 황금레시피 맛있게  끓여먹어요',
        ingredients: ['닭고기', '양파', '양배추', '대파', '깻잎', '후추', '떡볶이용 떡', '고구마', '당근', '생강술'],
        category: '한식',
        views: 1001230,
        id: 7,
    },
    {
        thumbnail: 'https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg',
        title: '참치김치찌개 황금레시피 맛있게  끓여먹어요',
        ingredients: ['닭고기', '양파', '양배추', '대파', '깻잎', '후추', '떡볶이용 떡', '고구마', '당근', '생강술'],
        category: '한식',
        views: 1001230,
        id: 8,
    },
]

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
                contentContainerStyle={{ padding: 14, paddingBottom: 70 }}
                data={recommendRecipeStore.recipes}
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
                renderItem={({ item }) => (
                    <RecipeList {...item} onPress={() => navigation.navigate('Recipe', { recipe: item })} />
                )} />

            <LoadingModal visible={isDetectioning} text='식재료를 확인하고 있어요...' />

            <FloatingCameraButton onPress={() => {
                showAction(async (res) => {
                    if (res.cancelled) return;

                    setIsDetectioning(true);
                    const result = await Ingredient.detectIngredientFromImage(res.uri);
                    const cookie = result.headers['set-cookie'][0];
                    const { ingredients } = cookie2obj(cookie);
                    const base54 = await blob2base54(result.data);
                    setIsDetectioning(false);

                    navigation.navigate('Detection', { images: [base54], ingredients });
                });
            }} />
        </>
    );
}

export default observer(HomeScreen);
