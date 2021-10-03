import React from 'react';
import { Image, Text, View } from 'react-native';
import RBCard from '../../Common/RBCard';
import { styles } from './styles';

function RecipeList({ id, title, thumbnail, ingredients, rating, views, theme, category, ...props }) {
    return (
        <RBCard style={styles.container}>
            <Image
                style={styles.thumbnail}
                source={{ uri: thumbnail }} />
            <View style={styles.content}>
                <Text style={styles.title} numberOfLines={2}>{title}</Text>
                <View></View>
                <View></View>
            </View>
        </RBCard>
    );
}

export default RecipeList;