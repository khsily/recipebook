import React, { useState } from 'react';
import { observer } from 'mobx-react';

import {
    HeaderButton,
    RBChoiceGroup,
    RBLayout,
    RecipeList,
} from '../../components';

import ic_search from '../../../assets/icon/ic_search.png';

const HomeScreen = ({ navigation }) => {
    React.useLayoutEffect(() => {
        navigation.setOptions({
            headerRight: () => (
                <HeaderButton icon={ic_search} onPress={() => navigation.navigate('Search')} />
            )
        });
    }, [navigation]);

    const [active, setActive] = useState(0);

    return (
        <RBLayout contentContainerStyle={{ paddingBottom: 30 }}>
            <RBChoiceGroup
                style={{ marginBottom: 14 }}
                choices={['추천', '식재료 충분', '식재료 부족']}
                active={active}
                onChange={(i) => setActive(i)} />

            <RecipeList
                thumbnail='https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg'
                title='참치김치찌개 황금레시피 맛있게  끓여먹어요'
                ingredients={['닭고기', '양파', '양배추', '대파', '깻잎', '후추', '떡볶이용 떡', '고구마', '당근', '생강술']}
                category='한식'
                views={1001230} />
            <RecipeList
                thumbnail='https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg'
                title='참치김치찌개 황금레시피 맛있게  끓여먹어요'
                ingredients={['닭고기', '양파', '양배추']}
                category='중식'
                views={10010} />
            <RecipeList
                thumbnail='https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg'
                title='참치김치찌개 황금레시피 맛있게  끓여먹어요'
                ingredients={['닭고기', '양파', '양배추']}
                category='중식'
                views={131209380} />
            <RecipeList
                thumbnail='https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg'
                title='참치김치찌개 황금레시피 맛있게  끓여먹어요'
                ingredients={['닭고기', '양파', '양배추']}
                category='중식'
                views={131209380} />
            <RecipeList
                thumbnail='https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg'
                title='참치김치찌개 황금레시피 맛있게  끓여먹어요'
                ingredients={['닭고기', '양파', '양배추']}
                category='중식'
                views={131209380} />
            <RecipeList
                thumbnail='https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg'
                title='참치김치찌개 황금레시피 맛있게  끓여먹어요'
                ingredients={['닭고기', '양파', '양배추']}
                category='중식'
                views={131209380} />
        </RBLayout>
    );
}

export default observer(HomeScreen);
