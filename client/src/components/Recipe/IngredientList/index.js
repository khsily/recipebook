import React from 'react';
import { View, Text, Image, TouchableOpacity } from 'react-native';
import { styles } from './styles';

import ic_cart from '../../../../assets/icon/ic_cart.png';

function IngredientList({ text, value, buyLink }) {
    return (
        <View style={styles.container}>
            <Text style={styles.text}>{text}</Text>
            <Text style={styles.value}>{value}</Text>
            <TouchableOpacity style={styles.basket}>
                <Image style={styles.basketImage} source={ic_cart} />
            </TouchableOpacity>
        </View>
    );
}

export default IngredientList;