import React, { useState } from 'react';
import { Text, View, ScrollView } from 'react-native';

import { HeaderButton, LoadingModal, SearchInput } from '../../components';
import { useCameraAction } from '../../customHook/useCameraAction';

import ic_camera from '../../../assets/icon/ic_camera.png';
import { fakeLoading } from '../../utils';
import { useQuerySearch } from '../../customHook/useQuerySearch';

ingredients = ['닭고기', '양파', '양배추', '대파', '고구마', '당근', '후추'].sort();

const SearchScreen = ({ navigation }) => {
    const [isDetectioning, setIsDetectioning] = useState(false);
    const [ingredientData, ingredientQuery, setIngredientQuery, setIngredientData] = useQuerySearch(ingredients);
    const showAction = useCameraAction();

    function handleDetection() {
        showAction(async (res) => {
            setIsDetectioning(true);
            // TODO: object detection 수행
            await fakeLoading(4000);

            // TODO: object detection 완료 결과 보여주기
            setIsDetectioning(false);
            console.log(res);
            navigation.navigate('Detection', {
                images: [res.uri],
                from: 'Search',
            });
        })
    }

    React.useLayoutEffect(() => {
        navigation.setOptions({
            headerRight: () => (
                <HeaderButton icon={ic_camera} onPress={handleDetection} />
            )
        });
    }, [navigation]);

    return (
        <View style={{ padding: 14 }}>
            <SearchInput
                placeholder='식재료 입력...'
                data={ingredientData}
                value={ingredientQuery}
                onChangeText={(text) => setIngredientQuery(text)}
                onSelect={(text) => setIngredientQuery(text)}
                onBlur={() => setIngredientData([])}
                onFocus={() => ingredientQuery || setIngredientData(ingredients)} />
            <LoadingModal visible={isDetectioning} text='식재료를 확인하고 있어요...' />
        </View>
    );
}

export default SearchScreen;
