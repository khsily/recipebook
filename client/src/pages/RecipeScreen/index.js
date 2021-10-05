import React from 'react';
import { Text, View, Image } from 'react-native';
import { SharedElement } from 'react-navigation-shared-element';

import { styles } from './styles';

const RecipeScreen = ({ route }) => {
    const { recipe } = route.params;

    return (
        <View>
            <SharedElement id={`recipe.${recipe.id}.photo`}>
                <Image style={styles.image} source={{ uri: recipe.thumbnail }} />
            </SharedElement>
        </View>
    );
}

export default RecipeScreen;
