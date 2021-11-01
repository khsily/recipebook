import { Dimensions, StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    listContainer: {
        width: Dimensions.get('window').width,
    },

    listContent: {
        padding: 14,
        paddingTop: 0,
        paddingBottom: 70,
        minHeight: '100%',
    },
});