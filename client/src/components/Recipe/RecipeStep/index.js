import React from 'react';
import { View, Text, Image, TouchableOpacity } from 'react-native';
import { styles } from './styles';

function RecipeStep({ no, images = [], text, onImagePress }) {
    return (
        <View style={styles.container}>
            <Text style={styles.no}>STEP {no}.</Text>
            <TouchableOpacity activeOpacity={0.8} onPress={onImagePress}>
                <Image style={styles.image} source={images[0]} />
                <View style={styles.sub_images_wrapper}>
                    {images.slice(1).map((v, i) => (
                        <Image style={styles.sub_image} key={`step_image_${i}`} source={v} />
                    ))}
                </View>
            </TouchableOpacity>
            <Text style={styles.content}>{text}</Text>
        </View>
    );
}

export default RecipeStep;