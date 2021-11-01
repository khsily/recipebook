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

    emptyContainer: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },

    emptyImage: {
        width: 100, height: 100, marginTop: -10,
    },

    emptyText: {
        padding: 15, fontSize: 16, color: '#777777', fontWeight: 'bold',
    },
});