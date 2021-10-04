import React from 'react';
import { View, TouchableOpacity, Text } from 'react-native';
import ImageView from "react-native-image-viewing";

import { styles } from './styles';

const DetectionResultScreen = ({ route, navigation }) => {
    const { images, from } = route.params;

    function onCancel() {
        navigation.goBack()
    }

    function onConfirm() {
        if (from == 'Search') {
            navigation.navigate({
                name: 'Search',
                merge: true,
                params: { ingredients: [] }
            });
        } else {
            navigation.replace('Search', { ingredients: [] });
        }
    }

    return (
        <View style={styles.container}>
            <ImageView
                images={images.map(v => ({ uri: v }))}
                imageIndex={0}
                visible={true}
                animationType='slide'
                onRequestClose={onCancel}
                FooterComponent={() => (
                    <View style={styles.buttonWrapper}>
                        <TouchableOpacity
                            style={[styles.button, styles.buttonLeft]}
                            activeOpacity={0.7}
                            onPress={onCancel}>
                            <Text style={styles.buttonText}>취소</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                            style={[styles.button, styles.buttonRight]}
                            activeOpacity={0.7}
                            onPress={onConfirm}>
                            <Text style={styles.buttonText}>확인</Text>
                        </TouchableOpacity>
                    </View>
                )}
            />
        </View>
    );
}

export default DetectionResultScreen;
