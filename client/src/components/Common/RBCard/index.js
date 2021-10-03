import React from 'react';
import { View } from 'react-native';
import { styles } from './styles';

function RBCard({ ...props }) {
    return (
        <View {...props} style={{ ...styles.card, ...props.style }} />
    );
}

export default RBCard;