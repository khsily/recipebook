import React from 'react';
import { View, Text, Image, TouchableOpacity } from 'react-native';
import { styles } from './styles';

function RecipeStep({ no, image, text, onImagePress }) {
    return (
        <View style={styles.container}>
            <Text style={styles.no}>{no}</Text>
            <TouchableOpacity activeOpacity={0.8} onPress={onImagePress}>
                <Image style={styles.image} source={{ uri: image }} />
            </TouchableOpacity>
            <Text style={styles.content}>{text}</Text>
        </View>
    );
}

export default RecipeStep;