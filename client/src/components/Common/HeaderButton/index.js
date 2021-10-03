import React from 'react';
import { Image, TouchableOpacity } from 'react-native';
import { styles } from './styles';

function HeaderButton({ icon, ...props }) {
    return (
        <TouchableOpacity
            style={styles.button}
            activeOpacity={0.6}
            {...props}>
            <Image style={styles.icon} source={icon} />
        </TouchableOpacity>
    );
}

export default HeaderButton;