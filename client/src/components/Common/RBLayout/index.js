import React from 'react';
import { SafeAreaView, ScrollView } from 'react-native';
import { styles } from './styles';

function RBLayout({ ...props }) {
    return (
        <SafeAreaView>
            <ScrollView contentContainerStyle={styles.container} {...props} />
        </SafeAreaView>
    );
}

export default RBLayout;