import React from 'react';
import { View } from 'react-native';
import { styles } from './styles';

function RBLayout({ ...props }) {
    return (
        <View style={styles.container} {...props} />
    );
}

export default RBLayout;