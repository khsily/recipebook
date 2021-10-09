import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    contrainer: {
        alignItems: 'center',
        marginBottom: 20,
        flex: 1,
        paddingHorizontal: 15,
    },

    imageWrapper: {
        width: '100%',
        aspectRatio: 1,
        borderRadius: 100,
        marginBottom: 10,
        overflow: 'hidden',
    },

    image: {
        width: '100%',
        height: '100%',
    },

    heartWrapper: {
        width: '100%',
        height: '100%',
        left: 0,
        top: 0,
        backgroundColor: 'rgba(231, 76, 60, 0.85)',
        alignItems: 'center',
        justifyContent: 'center',
        display: 'none',
    },

    heart: {
        width: '30%',
        height: '30%',
    },

    selected: {
        position: 'absolute',
        display: 'flex',
    },

    name: {
        fontSize: 14,
    },
});