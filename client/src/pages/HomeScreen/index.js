import React, { useState } from 'react';
import { observer } from 'mobx-react';
import { View, FlatList } from 'react-native';

import {
    FloatingCameraButton,
    HeaderButton,
    LoadingModal,
    RBChoiceGroup,
    RecipeList,
} from '../../components';

import { useCameraAction } from '../../customHook/useCameraAction';
import ic_search from '../../../assets/icon/ic_search.png';
import { fakeLoading } from '../../utils';

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
    const [isDetectioning, setIsDetectioning] = useState(false);
    const showAction = useCameraAction();

    React.useLayoutEffect(() => {
        navigation.setOptions({
            headerRight: () => (
                <HeaderButton icon={ic_search} onPress={() => navigation.navigate('Search')} />
            )
        });
    }, [navigation]);

    return (
        <>
            <FlatList
                contentContainerStyle={{ padding: 14, paddingBottom: 70 }}
                data={data}
                keyExtractor={item => `recipe_${item.id}`}
                ListHeaderComponent={() => (
                    <RBChoiceGroup
                        style={{ marginBottom: 14 }}
                        choices={['추천', '식재료 충분', '식재료 부족']}
                        active={active}
                        onChange={(i) => setActive(i)} />
                )}
                renderItem={({ item }) => (
                    <RecipeList {...item} onPress={() => navigation.navigate('Recipe', { recipe: item })} />
                )} />

            <LoadingModal visible={isDetectioning} text='식재료를 확인하고 있어요...' />

            <FloatingCameraButton onPress={() => {
                showAction(async (res) => {
                    setIsDetectioning(true);
                    // TODO: object detection 수행
                    await fakeLoading(4000);

                    // TODO: object detection 완료 결과 보여주기
                    setIsDetectioning(false);
                    console.log(res);
                    navigation.navigate('Detection', { images: [res.uri] });
                });
            }} />
        </>
    );
}

export default observer(HomeScreen);
