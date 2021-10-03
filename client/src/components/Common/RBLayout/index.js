import React from 'react';
import { SafeAreaView, ScrollView } from 'react-native';
import { styles } from './styles';

function RBLayout({ ...props }) {
    return (
        <SafeAreaView>
            <ScrollView
                {...props}
                contentContainerStyle={{ ...styles.container, ...props.contentContainerStyle }} />
        </SafeAreaView>
    );
}

export default RBLayout;