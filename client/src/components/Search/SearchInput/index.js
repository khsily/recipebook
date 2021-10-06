import React from 'react';
import { View } from 'react-native';
import AutoComplete from '../../Common/AutoComplete';

import RBButton from '../../Common/RBButton';

import { styles } from './styles';

function SearchInput({ ...props }) {
    return (
        <View style={styles.container}>
            <AutoComplete {...props} />
            <RBButton style={styles.button} title='추가' />
            <View style={styles.divider} />
        </View>
    );
}

export default SearchInput;