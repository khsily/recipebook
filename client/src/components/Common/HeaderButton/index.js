import React from 'react';
import { Image, TouchableOpacity } from 'react-native';
import { styles } from './styles';

function HeaderButton({ icon, ...props }) {
    return (
        <TouchableOpacity
            {...props}
            style={styles.button}
            activeOpacity={0.6}>
            <Image style={[styles.icon, props.style]} source={icon} />
        </TouchableOpacity>
    );
}

export default HeaderButton;