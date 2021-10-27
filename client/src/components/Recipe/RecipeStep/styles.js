import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    container: {
        paddingVertical: 10,
    },

    no: {
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: 5,
    },

    image: {
        width: '100%',
        height: 300,
        resizeMode: 'cover',
        borderWidth: 1,
        borderColor: '#EEEEEE',
    },

    sub_images_wrapper: {
        position: 'absolute',
        right: 0,
        bottom: 0,
        flexDirection: 'row',
        padding: 10,
    },

    sub_image: {
        width: 50,
        height: 50,
        borderWidth: 1,
        borderColor: '#FFF',
        marginLeft: 10,
    },

    content: {
        flex: 1,
        color: '#333333',
        paddingVertical: 10,
        paddingHorizontal: 5,
        lineHeight: 20,
    },
});