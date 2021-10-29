import React from 'react';
import { Image, Text, View } from 'react-native';
import { SharedElement } from 'react-navigation-shared-element';

import RBCard from '../../Common/RBCard';
import { styles } from './styles';

function RecipeList({ id, title, thumbnail, ingredients = [], searchIngredients = [], rating, view = 0, category, ...props }) {
    view = view.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    const sIngredients = new Set(searchIngredients);

    return (
        <RBCard style={styles.container} touchable {...props}>
            <SharedElement style={styles.thumbnailWrapper} id={`recipe.${id}.photo`}>
                <Image style={styles.thumbnail} source={{ uri: thumbnail }} />
            </SharedElement>
            <View style={styles.content}>
                <Text style={styles.title} numberOfLines={1}>{title}</Text>
                <View style={styles.ingredientsWrapper}>
                    <View style={styles.ingredients}>
                        {[...new Set(ingredients)].map((v, i) => (
                            <View style={[styles.ingredient, sIngredients.has(v) && styles.ingredientActive]} key={`ingredient_${i}`}>
                                <Text style={[styles.ingredientText, sIngredients.has(v) && styles.ingredientTextActive]}>{v}</Text>
                            </View>
                        ))}
                    </View>
                </View>
                <View style={styles.info}>
                    <Text style={styles.info_text}>{category}</Text>
                    <Text style={styles.info_text}>{view} views</Text>
                </View>
            </View>
        </RBCard>
    );
}

export default React.memo(RecipeList);