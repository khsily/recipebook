import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    contrainer: {
        borderTopWidth: 1,
        borderTopColor: '#EEEEEE',
        paddingHorizontal: 14,
        paddingVertical: 10,
        flexDirection: 'row',
        alignItems: 'center',
    },

    text: {
        color: '#999999',
    },

    selectedImages: {
        marginLeft: 5,
        flexDirection: 'row',
        flex: 1,
        alignItems: 'center',
    },

    image: {
        position: 'absolute',
        width: 35,
        height: 35,
        borderRadius: 30,
    },

    button: {
        paddingHorizontal: 15,
        borderRadius: 5,
    }
});