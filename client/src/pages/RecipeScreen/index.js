import React, { useState } from 'react';
import { ScrollView, Text, View, Image, TouchableOpacity } from 'react-native';
import { SharedElement } from 'react-navigation-shared-element';
import ImageView from "react-native-image-viewing";

import { IngredientList, RecipeSection, RecipeStep } from '../../components';

import { styles } from './styles';

const RecipeScreen = ({ route }) => {
    const { recipe } = route.params;

    const [imageViewerVisible, setImageViewerVisible] = useState(false);

    return (
        <>
            <ScrollView>
                <TouchableOpacity activeOpacity={0.8} onPress={() => setImageViewerVisible(true)}>
                    <SharedElement id={`recipe.${recipe.id}.photo`}>
                        <Image style={styles.image} source={{ uri: recipe.thumbnail }} />
                    </SharedElement>
                </TouchableOpacity>
                <View style={styles.container}>
                    <Text style={styles.title}>참치김치찌개 황금레시피 맛있게 끓여먹어요</Text>
                    <View style={styles.info}>
                        <Text style={styles.infoText}>1,123 views</Text>
                        <Text style={styles.infoText}>한식</Text>
                    </View>
                    <RecipeSection style={styles.ingredients} title='재료' subTitle='Ingredients'>
                        <IngredientList text='느타리버섯' value='110g' buyLink={`https://www.coupang.com/np/search?component=&q=${'느타리버섯'}`} />
                        <IngredientList text='더덕' value='110g' buyLink={`https://www.coupang.com/np/search?component=&q=${'더덕'}`} />
                        <IngredientList text='파프리카' value='24g' buyLink={`https://www.coupang.com/np/search?component=&q=${'파프리카'}`} />
                        <IngredientList text='청양고추' value='12g' buyLink={`https://www.coupang.com/np/search?component=&q=${'청양고추'}`} />
                        <IngredientList text='실파' value='4줄기' buyLink={`https://www.coupang.com/np/search?component=&q=${'실파'}`} />
                    </RecipeSection>
                    <RecipeSection title='레시피' subTitle='Ingredients'>
                        <RecipeStep
                            no={1}
                            image='https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg'
                            text='깔끔하고 예쁜 버섯 3종 모둠 셋트입니다. 백색 버섯 이름이 백선이고, 노란 버섯이 순정이고, 기존 느타리 버섯과 같은색 버섯이 곤지 7호입니다.'
                            onImagePress={() => setImageViewerVisible(true)} />
                        <RecipeStep
                            no={2}
                            image='https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg'
                            text='깔끔하고 예쁜 버섯 3종 모둠 셋트입니다. 백색 버섯 이름이 백선이고, 노란 버섯이 순정이고, 기존 느타리 버섯과 같은색 버섯이 곤지 7호입니다.'
                            onImagePress={() => setImageViewerVisible(true)} />
                        <RecipeStep
                            no={3}
                            image='https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg'
                            text='깔끔하고 예쁜 버섯 3종 모둠 셋트입니다. 백색 버섯 이름이 백선이고, 노란 버섯이 순정이고, 기존 느타리 버섯과 같은색 버섯이 곤지 7호입니다.'
                            onImagePress={() => setImageViewerVisible(true)} />
                        <RecipeStep
                            no={4}
                            image='https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg'
                            text='깔끔하고 예쁜 버섯 3종 모둠 셋트입니다. 백색 버섯 이름이 백선이고, 노란 버섯이 순정이고, 기존 느타리 버섯과 같은색 버섯이 곤지 7호입니다.'
                            onImagePress={() => setImageViewerVisible(true)} />
                    </RecipeSection>
                </View>
            </ScrollView>

            <ImageView
                images={[{ uri: 'https://www.elmundoeats.com/wp-content/uploads/2021/02/FP-Quick-30-minutes-chicken-ramen.jpg' }]}
                imageIndex={0}
                visible={imageViewerVisible}
                animationType='fade'
                onRequestClose={() => setImageViewerVisible(false)} />
        </>
    );
}

export default RecipeScreen;
