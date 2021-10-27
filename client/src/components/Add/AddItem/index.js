import React from 'react';
import { Text, TouchableOpacity } from 'react-native';
import { styles } from './styles';

function AddItem({ text, selected, ...props }) {
    const selectedStyle = selected ? styles.selected : {};

    return (
        <TouchableOpacity
            {...props}
            style={{ ...styles.container, ...props.style, ...selectedStyle }}
            activeOpacity={0.7}>
            <Text style={styles.text}>{text}</Text>
        </TouchableOpacity>
    );
}

export default AddItem;