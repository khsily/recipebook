import React from 'react';
import { TouchableOpacity, Text } from 'react-native';
import { styles } from './styles';

function RBButton({ title, color, backgroundColor, rounded, ...props }) {
    return (
        <TouchableOpacity
            {...props}
            style={{
                ...styles.button,
                backgroundColor: backgroundColor || styles.button.backgroundColor,
                borderRadius: rounded ? styles.button.borderRadius : 0,
                ...props.style,
            }}
            activeOpacity={0.8}>
            <Text style={{
                ...styles.text,
                color: color || styles.text.color,
                ...props.styles,
            }}>{title}</Text>
        </TouchableOpacity>
    );
}

export default RBButton;