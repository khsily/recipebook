import React from 'react';
import { View, Text } from 'react-native';
import { styles } from './styles';

function RecipeSection({ title, subTitle, children }) {
    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>{title}</Text>
                <Text style={styles.subTitle}>{subTitle}</Text>
            </View>
            <View>
                {children}
            </View>
        </View>
    );
}

export default RecipeSection;