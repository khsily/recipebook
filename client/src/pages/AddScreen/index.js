import React, { useEffect, useLayoutEffect, useState } from 'react';
import { View, Text, FlatList, TextInput, KeyboardAvoidingView, Platform } from 'react-native';
import Constants from 'expo-constants';

import { AddItem, RBButton } from '../../components';
import { categoryStore, ingredientStore } from '../../store';

import { styles } from './styles';

const AddScreen = ({ route, navigation }) => {
    const params = route.params || {};
    const isIngredient = params.type === 'ingredients';
    const searchIngredients = params.ingredients;
    const searchCategories = params.categories;

    const [selectedItems, setSelectedItems] = useState(new Set([]));
    const [data, setData] = useState([]);
    const [query, setQuery] = useState('');

    const typeText = isIngredient ? '식재료' : '카테고리';
    const title = `${typeText} 추가`;
    useLayoutEffect(() => navigation.setOptions({ title }), [navigation]);

    useEffect(() => {
        setData(isIngredient ? ingredientStore.ingredients : categoryStore.categories);
    }, [params.type]);

    useEffect(() => {
        const searchData = isIngredient ? searchIngredients : searchCategories;
        setSelectedItems(new Set(searchData.map(v => v.id)));
    }, [searchIngredients, searchCategories]);

    function handleSelect(item) {
        if (selectedItems.has(item.id)) {
            selectedItems.delete(item.id);
        } else {
            selectedItems.add(item.id);
        }

        setSelectedItems(new Set(selectedItems));
    }

    function handleSubmit() {
        const items = data.filter(v => selectedItems.has(v.id));

        navigation.navigate({
            name: 'Search',
            merge: true,
            params: { [params.type]: items }
        });
    }

    function getFilteredData(query) {
        if (!query) return data;
        return data.filter(v => v.name.includes(query));
    }

    return (
        <KeyboardAvoidingView
            style={styles.container}
            behavior={Platform.OS === 'ios' ? 'padding' : null}
            keyboardVerticalOffset={Constants.statusBarHeight + 44}>
            <TextInput
                style={styles.input}
                placeholder={`${typeText} 입력...`}
                onChangeText={text => setQuery(text)}
                value={query} />
            <FlatList
                style={styles.list}
                data={getFilteredData(query)}
                keyExtractor={item => `${params.type}_${item.id}`}
                renderItem={({ item }) => (
                    <AddItem
                        text={item.name}
                        onPress={() => handleSelect(item)}
                        selected={selectedItems.has(item.id)} />
                )} />
            <View style={styles.footer}>
                <RBButton
                    style={styles.submitButton}
                    textStyle={styles.submitButtonText}
                    title='선택 완료'
                    onPress={handleSubmit} />
            </View>
        </KeyboardAvoidingView>
    );
}

export default AddScreen;