import React, { useEffect, useState } from 'react';
import { ScrollView, Text, View, Image, TouchableOpacity } from 'react-native';
import { SharedElement } from 'react-navigation-shared-element';
import ImageView from "react-native-image-viewing";
import { observer } from 'mobx-react';

import { IngredientList, RecipeSection, RecipeStep } from '../../components';

import { styles } from './styles';
import { recipeDetailStore } from '../../store';

const RecipeScreen = ({ route }) => {
    const { search } = route.params;
    const [recipe, setRecipe] = useState(route.params.recipe);
    const [images, setImages] = useState([]);
    const [imageViewerVisible, setImageViewerVisible] = useState(false);

    async function fetchData() {
        await recipeDetailStore.reset();
        await recipeDetailStore.fetchDetail(recipe.id);
        setRecipe(recipeDetailStore.detail);
    }

    function formatImages(images) {
        return images.map((v) => ({ uri: v.replace('\'', '') }));
    }

    function showImageViewer(images = []) {
        setImages(formatImages(images));
        setImageViewerVisible(true);
    }

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <>
            <ScrollView>
                <TouchableOpacity activeOpacity={0.8} onPress={() => showImageViewer([recipe.image])}>
                    <SharedElement id={`recipe.${search}.${recipe.id}.photo`}>
                        <Image style={styles.image} source={{ uri: recipe.thumbnail }} />
                    </SharedElement>
                </TouchableOpacity>
                <View style={styles.container}>
                    <Text style={styles.title_desc}>{recipe.title_desc}</Text>
                    <Text style={styles.title}>{recipe.title}</Text>
                    <View style={styles.info}>
                        <Text style={styles.infoText}>{recipe.category},</Text>
                        <Text style={styles.infoText}>{recipe.view} views</Text>
                    </View>
                    <RecipeSection style={styles.ingredients} title='재료' subTitle='Ingredients'>
                        {typeof recipe.ingredients !== 'string' && recipe.ingredients.map((v, i) => (
                            <IngredientList
                                key={`ingredient_${i}_${v.ingredient_id}`}
                                text={v.name}
                                value={v.amount}
                                buyLink={`https://www.coupang.com/np/search?component=&q=${v.default_name}`} />
                        ))}
                    </RecipeSection>
                    <RecipeSection title='레시피' subTitle='Recipe'>
                        {recipe.steps && recipe.steps.map((v) => (
                            <RecipeStep
                                key={`step_${v.step}`}
                                no={v.step}
                                images={formatImages(v.thumbnails)}
                                text={v.content}
                                onImagePress={() => showImageViewer(v.thumbnails)} />
                        ))}
                    </RecipeSection>
                </View>
            </ScrollView>

            <ImageView
                images={images}
                imageIndex={0}
                visible={imageViewerVisible}
                animationType='fade'
                onRequestClose={() => setImageViewerVisible(false)}
                swipeToCloseEnabled={false} />
        </>
    );
}

export default observer(RecipeScreen);
