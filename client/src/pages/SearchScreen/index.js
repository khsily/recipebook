import React, { useEffect, useLayoutEffect, useState } from 'react';
import { View, Text, KeyboardAvoidingView, ScrollView, Platform, LayoutAnimation, Keyboard } from 'react-native';
import Constants from 'expo-constants';

import { HeaderButton, LoadingModal, RBButton, SearchForm, SearchTag } from '../../components';
import { useCameraAction } from '../../customHook/useCameraAction';

import ic_camera from '../../../assets/icon/ic_camera.png';
import { blob2base54, cookie2obj, decodeUnicode } from '../../utils';
import { layoutAnimConfig } from '../../animation';
import { styles } from './styles';
import { observer } from 'mobx-react';
import { ingredientStore, myFavorStore, recipeStore } from '../../store';
import { Ingredient } from '../../api';

Keyboard.addListener('keyboardDidHide', () => {
    Keyboard.dismiss(); // lose focus
});


const SearchScreen = ({ route, navigation }) => {
    const params = route.params || {};
    const [categories, setCategories] = useState([]);
    const [ingredients, setIngredients] = useState([]);

    const [isDetecting, setIsDetecting] = useState(false);
    const showAction = useCameraAction();

    function handleDetection() {
        showAction(async (res) => {
            if (res.cancelled) return;

            setIsDetecting(true);
            const result = await Ingredient.detectIngredientFromImage(res.uri);
            const cookie = result.headers['set-cookie'][0];
            const base54 = await blob2base54(result.data);
            setIsDetecting(false);

            let { ingredients } = cookie2obj(cookie);
            ingredients = decodeUnicode(ingredients);
            ingredients = ingredients.split(',');
            ingredients = ingredientStore.ingredients.filter(v => ingredients.indexOf(v.name) > -1);

            navigation.navigate('Detection', {
                images: [base54],
                from: 'Search',
                ingredients,
            });
        })
    }

    function handleDeleteCategory(item) {
        LayoutAnimation.configureNext(layoutAnimConfig);
        setCategories(categories.filter(v => v.id !== item.id));
    }

    function handleDeleteIngredient(item) {
        LayoutAnimation.configureNext(layoutAnimConfig);
        setIngredients(ingredients.filter(v => v.id !== item.id));
    }

    function handleAdd(type) {
        navigation.navigate('Add', {
            type,
            ingredients,
            categories,
        })
    }

    async function handleSearch() {
        recipeStore.reset();
        recipeStore.fetchList({
            page: 1,
            combinationId: myFavorStore.combinationId,
            ingredients,
            categories,
        });

        navigation.navigate({
            name: 'Home',
            merge: true,
            params: { search: true },
        });
    }


    useLayoutEffect(() => {
        navigation.setOptions({
            headerRight: () => (
                <HeaderButton icon={ic_camera} onPress={handleDetection} />
            )
        });

        setIngredients(recipeStore.ingredients);
        setCategories(recipeStore.categories);
    }, [navigation]);

    useEffect(() => {
        if (params.ingredients && params.ingredients.length > 0) {
            setIngredients(params.ingredients);
        }
    }, [params.ingredients]);

    useEffect(() => {
        if (params.categories && params.categories.length > 0) {
            setCategories(params.categories);
        }
    }, [params.categories]);

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
                    <RBButton style={styles.addButton} title='추가' onPress={() => handleAdd('ingredients')} />
                    {ingredients.length > 0 &&
                        <View style={styles.tags}>
                            {ingredients.map((v) => (
                                <SearchTag
                                    style={styles.tag}
                                    key={`ingredient_${v.id}`}
                                    onDelete={() => handleDeleteIngredient(v)}
                                    text={v.name} />
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
                    <RBButton style={styles.addButton} title='추가' onPress={() => handleAdd('categories')} />
                    {categories.length > 0 &&
                        <View style={styles.tags}>
                            {categories.map((v) => (
                                <SearchTag
                                    style={styles.tag}
                                    key={`category_${v.id}`}
                                    onDelete={() => handleDeleteCategory(v)}
                                    text={v.name} />
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
                onPress={handleSearch}
                title='검색' />
            <LoadingModal visible={isDetecting} text='식재료를 확인하고 있어요' />
        </KeyboardAvoidingView>
    );
}

export default observer(SearchScreen);
