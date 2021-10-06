import React, { useState } from 'react';
import { ScrollView } from 'react-native';

import { HeaderButton, LoadingModal, SearchForm, SearchInput } from '../../components';
import { useCameraAction } from '../../customHook/useCameraAction';

import ic_camera from '../../../assets/icon/ic_camera.png';
import { fakeLoading } from '../../utils';
import { styles } from './styles';


const ingredients = ['파프리카', '닭고기', '양파', '양배추', '대파', '고구마', '당근', '돼지고기', '소고기', '고추', '오이'].sort();
const categories = ['메인요리', '밑반찬', '간식', '간단요리', '초대요리', '채식', '한식', '양식', '일식', '중식', '퓨전', '분식', '안주', '베이킹', '다이어트', '도시락'].sort();


const SearchScreen = ({ navigation }) => {
    const [isDetectioning, setIsDetectioning] = useState(false);
    const [ingredientQuery, setIngredientQuery] = useState('');
    const [categoryQuery, setCategoryQuery] = useState('');
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
        <ScrollView
            contentContainerStyle={{ padding: 14, minHeight: '100%' }}
            nestedScrollEnabled={true}
            keyboardShouldPersistTaps='always'>
            <SearchForm title='식재료'>
                <SearchInput
                    style={styles.searchInput}
                    data={ingredients}
                    value={ingredientQuery}
                    placeholder='식재료 입력...'
                    onChangeText={(text) => setIngredientQuery(text)}
                    onSelect={(text) => setIngredientQuery(text)} />
            </SearchForm>

            <SearchForm title='카테고리'>
                <SearchInput
                    style={styles.searchInput}
                    data={categories}
                    value={categoryQuery}
                    placeholder='카테고리 입력...'
                    onChangeText={(text) => setCategoryQuery(text)}
                    onSelect={(text) => setCategoryQuery(text)} />
            </SearchForm>

            <LoadingModal visible={isDetectioning} text='식재료를 확인하고 있어요...' />
        </ScrollView>
    );
}

export default SearchScreen;
