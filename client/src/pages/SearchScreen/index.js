import React, { useEffect, useLayoutEffect, useState } from 'react';
import { View, Text, KeyboardAvoidingView, ScrollView, Platform, LayoutAnimation, Keyboard } from 'react-native';
import Constants from 'expo-constants';

import { HeaderButton, LoadingModal, RBButton, SearchForm, SearchInput, SearchTag } from '../../components';
import { useCameraAction } from '../../customHook/useCameraAction';

import ic_camera from '../../../assets/icon/ic_camera.png';
import { fakeLoading } from '../../utils';
import { layoutAnimConfig } from '../../animation';
import { styles } from './styles';

Keyboard.addListener('keyboardDidHide', () => {
    Keyboard.dismiss(); // lose focus
})

const ingredientData = ['파프리카', '닭고기', '양파', '양배추', '대파', '고구마', '당근', '돼지고기', '소고기', '고추', '오이'].sort();
const categoryData = ['메인요리', '밑반찬', '간식', '간단요리', '초대요리', '채식', '한식', '양식', '일식', '중식', '퓨전', '분식', '안주', '베이킹', '다이어트', '도시락'].sort();

const SearchScreen = ({ route, navigation }) => {
    const params = route.params;
    const detectedIngredients = params ? params.ingredients : [];

    const [isDetectioning, setIsDetectioning] = useState(false);
    const [query, setQuery] = useState({ ingredient: '', category: '' });
    const [data, setData] = useState({ ingredient: new Set(detectedIngredients), category: new Set() });
    const showAction = useCameraAction();

    const categories = Array.from(data.category);
    const ingredients = Array.from(data.ingredient);


    function handleDetection() {
        showAction(async (res) => {
            if (res.cancelled) return;

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


    function handleSubmit(type) {
        setQuery({ ...query, [type]: '' });

        const baseData = type === 'ingredient' ? ingredientData : categoryData;
        const queryText = query[type];
        if (!queryText) return;

        const hasQuery = baseData.includes(queryText);
        if (!hasQuery) {
            alert(`"${queryText}" 은/는 사용할 수 없습니다`);
            return;
        }

        data[type].add(queryText);
        setData({ ...data });
    }

    function handleDelete(type, target) {
        data[type].delete(target);
        setData({ ...data });
        LayoutAnimation.configureNext(layoutAnimConfig);
    }


    useLayoutEffect(() => {
        navigation.setOptions({
            headerRight: () => (
                <HeaderButton icon={ic_camera} onPress={handleDetection} />
            )
        });
    }, [navigation]);

    useEffect(() => {
        if (detectedIngredients && detectedIngredients.length > 0) {
            detectedIngredients.forEach(item => data.ingredient.add(item));
            setData({ ...data });
        }
    }, [detectedIngredients]);

    return (
        <KeyboardAvoidingView
            style={styles.container}
            behavior={Platform.OS === 'ios' ? 'padding' : null}
            enabled
            keyboardVerticalOffset={Constants.statusBarHeight + 44}>
            <ScrollView
                contentContainerStyle={styles.scrollview}
                nestedScrollEnabled={true}
                keyboardShouldPersistTaps='handled'>
                <SearchForm title='식재료'>
                    <SearchInput
                        style={styles.searchInput}
                        data={ingredientData}
                        value={query.ingredient}
                        placeholder='식재료 입력...'
                        blurOnSubmit={false}
                        onChangeText={(text) => setQuery({ ...query, ingredient: text })}
                        onSelect={(text) => setQuery({ ...query, ingredient: text })}
                        onSubmit={() => handleSubmit('ingredient')} />
                    {ingredients.length > 0 &&
                        <View style={styles.tags}>
                            {ingredients.map((v) => (
                                <SearchTag
                                    style={styles.tag}
                                    key={`ingredient_${v}`}
                                    onDelete={() => handleDelete('ingredient', v)}
                                    text={v} />
                            ))}
                        </View>
                    }
                    {ingredients.length === 0 &&
                        <View style={styles.emptyList}>
                            <Text style={styles.emptyText}>선택된 식재료가 없습니다</Text>
                        </View>
                    }
                </SearchForm>

                <SearchForm title='카테고리'>
                    <SearchInput
                        style={styles.searchInput}
                        data={categoryData}
                        value={query.category}
                        placeholder='카테고리 입력...'
                        blurOnSubmit={false}
                        onChangeText={(text) => setQuery({ ...query, category: text })}
                        onSelect={(text) => setQuery({ ...query, category: text })}
                        onSubmit={() => handleSubmit('category')} />
                    {categories.length > 0 &&
                        <View style={styles.tags}>
                            {categories.map((v) => (
                                <SearchTag
                                    style={styles.tag}
                                    key={`category_${v}`}
                                    onDelete={() => handleDelete('category', v)}
                                    text={v} />
                            ))}
                        </View>
                    }
                    {categories.length === 0 &&
                        <View style={styles.emptyList}>
                            <Text style={styles.emptyText}>선택된 카테고리가 없습니다</Text>
                        </View>
                    }
                </SearchForm>
            </ScrollView>

            <RBButton
                style={styles.searchButton}
                textStyle={styles.searchButtonText}
                title='검색' />
            <LoadingModal visible={isDetectioning} text='식재료를 확인하고 있어요...' />
        </KeyboardAvoidingView>
    );
}

export default SearchScreen;
