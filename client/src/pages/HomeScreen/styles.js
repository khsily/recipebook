import { Dimensions, StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    listContainer: {
        width: Dimensions.get('window').width,
    },

    listInVisible: {
        width: 0,
        height: 0,
        overflow: 'hidden',
    },

    listContent: {
        padding: 14,
        paddingTop: 0,
        paddingBottom: 70,
        minHeight: '100%',
    },
});