import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        marginBottom: 12,
    },

    thumbnail: {
        width: 115,
        height: '100%',
    },

    content: {
        flex: 1,
        padding: 8,
    },

    title: {
        fontSize: 15,
        fontWeight: 'bold',
        marginBottom: 5,
    },

    ingredients: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        height: 50,
        overflow: 'hidden',
        marginBottom: 5,
    },

    ingredient: {
        alignSelf: "baseline",
        paddingHorizontal: 8,
        paddingVertical: 3,
        borderWidth: 1,
        borderColor: '#555555',
        borderRadius: 10,
        marginRight: 5,
        marginBottom: 5,
    },

    ingredientText: {
        fontSize: 10,
        color: '#555555',
    },

    info: {
        flexDirection: 'row',
        justifyContent: 'space-between',
    },

    info_text: {
        fontSize: 10,
        color: '#999999',
    },
});