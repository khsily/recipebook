import React from 'react';
import { View, Image, Text, TouchableOpacity } from 'react-native';
import { styles } from './styles';

import ic_heart from '../../../../assets/icon/ic_heart.png';

function FavorSectionItem({ title, thumbnail, selected = false, onPress }) {
    return (
        <View style={styles.contrainer}>
            <TouchableOpacity style={styles.imageWrapper} onPress={onPress} activeOpacity={1}>
                <Image
                    style={styles.image}
                    source={{ uri: thumbnail }} />
                <View style={[styles.heartWrapper, selected && styles.selected]}>
                    <Image style={styles.heart} source={ic_heart} />
                </View>
            </TouchableOpacity>
            <Text style={styles.name}>{title}</Text>
        </View>
    );
}

export default FavorSectionItem;