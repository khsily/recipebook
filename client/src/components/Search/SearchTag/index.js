import React from 'react';
import { View, Text, TouchableOpacity, Image } from 'react-native';

import { styles } from './styles';
import ic_cancel from '../../../../assets/icon/ic_cancel_black.png';

function SearchTag({ text, onDelete, style }) {
    return (
        <View style={[styles.container, style]}>
            <Text style={styles.text}>{text}</Text>
            <TouchableOpacity
                hitSlop={{ top: 15, bottom: 15, left: 15, right: 15 }}
                onPress={onDelete}>
                <Image style={styles.delete} source={ic_cancel} />
            </TouchableOpacity>
        </View>
    );
}

export default SearchTag;