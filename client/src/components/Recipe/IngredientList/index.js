import React from 'react';
import { View, Text, Image, TouchableOpacity, Linking } from 'react-native';
import { styles } from './styles';

import ic_cart from '../../../../assets/icon/ic_cart.png';

function IngredientList({ text, value, buyLink }) {
    return (
        <View style={styles.container}>
            <Text style={styles.text}>{text}</Text>
            <Text style={styles.value}>{value}</Text>
            <TouchableOpacity
                style={styles.basket}
                activeOpacity={0.7}
                onPress={() => Linking.openURL(buyLink)}>
                <Image style={styles.basketImage} source={ic_cart} />
            </TouchableOpacity>
        </View>
    );
}

export default IngredientList;