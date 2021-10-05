import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import Autocomplete from 'react-native-autocomplete-input';

import RBButton from '../../Common/RBButton';

import { styles } from './styles';

function SearchInput({ data, value, onSelect = (() => { }), ...props }) {
    data = data.length === 1 && (data[0] === value) ? [] : data;

    return (
        <View style={styles.container}>
            <View style={styles.leftContainer}>
                <View style={styles.inputPosWrapper}>
                    <Autocomplete
                        {...props}
                        style={styles.inputContainer}
                        inputContainerStyle={styles.input}
                        listContainerStyle={styles.listContainer}
                        data={data}
                        value={value}
                        autoCorrect={false}
                        flatListProps={{
                            keyboardShouldPersistTaps: 'always',
                            keyExtractor: (_, idx) => `ingredient_${idx}`,
                            renderItem: ({ item }) => (
                                <TouchableOpacity style={styles.list} onPress={() => onSelect(item)}>
                                    <Text>{item}</Text>
                                </TouchableOpacity>
                            ),
                        }} />
                </View>
            </View>
            <RBButton style={styles.button} title='추가' />
            <View style={styles.divider} />
        </View>
    );
}

export default SearchInput;