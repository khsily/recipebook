import React, { useState } from 'react';
import { View, TextInput, Text, TouchableOpacity, ScrollView } from 'react-native';

import { styles } from './styles';

function searchQuery(arr = [], query) {
    return arr.filter((item) => item.includes(query));
}

function AutoComplete({ data, value, onSelect = (() => { }), containerStyle, ...props }) {
    const [visible, setVisible] = useState(false);
    const filteredData = searchQuery(data, value);

    const isLastOne = filteredData.length == 1 && filteredData[0] == value;
    const isEmpty = filteredData.length == 0;

    return (
        <View style={[styles.container, containerStyle]}>
            <TextInput
                {...props}
                style={[styles.input, props.style]}
                value={value}
                onFocus={() => setVisible(true)}
                onBlur={() => setVisible(false)} />
            {(visible && !isLastOne && !isEmpty) &&
                <View style={styles.listWrapper}>
                    <ScrollView
                        contentContainerStyle={styles.listContainer}
                        keyboardShouldPersistTaps='always'
                        nestedScrollEnabled={true}>
                        {filteredData.map((v, i) => (
                            <TouchableOpacity key={`item_${v}_${i}`} activeOpacity={0.7} onPress={() => onSelect(v)}>
                                <Text style={styles.list}>{v}</Text>
                            </TouchableOpacity>
                        ))}
                    </ScrollView>
                </View>
            }
        </View>
    );
}

export default AutoComplete;