import React from 'react';
import { Text, View, Image } from 'react-native';
import { ScrollView } from 'react-native-gesture-handler';
import { SharedElement } from 'react-navigation-shared-element';
import { IngredientList, RecipeSection } from '../../components';

import { styles } from './styles';

const RecipeScreen = ({ route }) => {
    const { recipe } = route.params;

    return (
        <ScrollView>
            <SharedElement id={`recipe.${recipe.id}.photo`}>
                <Image style={styles.image} source={{ uri: recipe.thumbnail }} />
            </SharedElement>
            <View style={styles.container}>
                <Text style={styles.title}>참치김치찌개 황금레시피 맛있게 끓여먹어요</Text>
                <View style={styles.info}>
                    <Text style={styles.infoText}>1,123 views</Text>
                    <Text style={styles.infoText}>한식</Text>
                </View>
                <RecipeSection style={styles.ingredients} title='재료' subTitle='Ingredients'>
                    <IngredientList text='순정 느타리버섯' value='110g' />
                    <IngredientList text='더덕' value='110g' />
                    <IngredientList text='파프리카' value='24g' />
                    <IngredientList text='청양고추' value='12g' />
                    <IngredientList text='실파' value='4줄기' />
                </RecipeSection>
                <RecipeSection title='레시피' subTitle='Ingredients'>

                </RecipeSection>
            </View>
        </ScrollView>
    );
}

export default RecipeScreen;
