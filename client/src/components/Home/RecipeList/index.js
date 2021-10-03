import React from 'react';
import { Image, Text, View } from 'react-native';
import RBCard from '../../Common/RBCard';
import { styles } from './styles';

function RecipeList({ id, title, thumbnail, ingredients = [], rating, views = 0, category, ...props }) {
    views = views.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

    return (
        <RBCard style={styles.container}>
            <Image
                style={styles.thumbnail}
                source={{ uri: thumbnail }} />
            <View style={styles.content}>
                <Text style={styles.title} numberOfLines={2}>{title}</Text>
                <View style={styles.ingredients}>
                    {ingredients.map((v, i) => (
                        <View style={styles.ingredient} key={`ingredient_${i}`}>
                            <Text style={styles.ingredientText}>{v}</Text>
                        </View>
                    ))}
                </View>
                <View style={styles.info}>
                    <Text style={styles.info_text}>{category}</Text>
                    <Text style={styles.info_text}>{views} views</Text>
                </View>
            </View>
        </RBCard>
    );
}

export default RecipeList;