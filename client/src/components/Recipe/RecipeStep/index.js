import React from 'react';
import { View, Text, Image } from 'react-native';
import { styles } from './styles';

function RecipeStep({ no, image, text }) {
    return (
        <View style={styles.container}>
            <Text style={styles.no}>{no}</Text>
            <Image style={styles.image} source={{ uri: image }} />
            <Text style={styles.content}>{text}</Text>
        </View>
    );
}

export default RecipeStep;