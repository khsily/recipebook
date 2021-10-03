import React from 'react';
import { observer } from 'mobx-react';

import {
    LoadingModal,
    RBChoiceGroup,
    RBLayout,
    RecipeList,
} from '../../components';

const HomeScreen = ({ navigation }) => {
    return (
        <RBLayout>
            <RBChoiceGroup
                style={{ marginBottom: 14 }}
                choices={['추천', '식재료 충분', '식재료 부족']}
                active={0} />

            <RecipeList
                thumbnail='https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg'
                title='참치김치찌개 황금레시피 맛있게  끓여먹어요' />
            <RecipeList
                thumbnail='https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg'
                title='참치김치찌개 황금레시피 맛있게  끓여먹어요' />

            <LoadingModal visible text={'사진을 처리하고 있습니다...'} />
        </RBLayout>
    );
}

export default observer(HomeScreen);
