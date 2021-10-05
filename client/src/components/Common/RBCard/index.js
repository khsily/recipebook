import React from 'react';
import { View, TouchableOpacity } from 'react-native';
import { styles } from './styles';

function RBCard({ touchable = false, ...props }) {
    Container = touchable ? TouchableOpacity : View;
    touchableOptions = { activeOpacity: 0.8 }

    return (
        <Container
            {...props}
            {...touchableOptions}
            style={{ ...styles.card, ...props.style }} />
    );
}

export default RBCard;