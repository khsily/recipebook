import React from 'react';
import { FlatList } from 'react-native';
import { styles } from './styles';

function FavorSectionLayout({ section, index, numColumns = 3, ...props }) {
    if (index !== 0) return null;

    return (
        <FlatList
            numColumns={numColumns}
            columnWrapperStyle={styles.contrainer}
            data={section.data}
            keyExtractor={(v, i) => v + i}
            {...props} />
    );
}

export default FavorSectionLayout;