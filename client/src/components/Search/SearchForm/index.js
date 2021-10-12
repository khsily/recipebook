import React from 'react';
import { View, Text } from 'react-native';

import RBCard from '../../Common/RBCard';

import { styles } from './styles';

function SearchForm({ title, children }) {
    return (
        <View style={styles.container}>
            <Text style={styles.title}>{title}</Text>
            <RBCard style={styles.content}>
                {children}
            </RBCard>
        </View>
    );
}

export default SearchForm;