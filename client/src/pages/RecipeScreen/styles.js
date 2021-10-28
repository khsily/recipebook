import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    container: {
        padding: 14,
    },
    
    image: {
        width: '100%',
        height: 300,
        resizeMode: 'cover',
    },

    title_desc: {
        fontSize: 14,
        color: '#333333',
    },

    title: {
        fontSize: 20,
        fontWeight: 'bold',
        paddingVertical: 3,
    },

    info: {
        flexDirection: 'row',
        marginBottom: 10,
    },

    infoText: {
        fontSize: 13,
        color: '#999999',
        marginRight: 8,
    },

    ingredients: {
        flexDirection: 'row',
        flexWrap: 'wrap',
    },
});