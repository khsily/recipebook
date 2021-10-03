import React from 'react';
import { Image, TouchableOpacity } from 'react-native';
import { styles } from './styles';

function FloatingButton({ icon, ...props }) {
    return (
        <TouchableOpacity
            {...props}
            style={{ ...styles.button, ...props.style }}
            activeOpacity={0.8}>
            <Image style={styles.icon} source={icon} />
        </TouchableOpacity>
    );
}

export default FloatingButton;