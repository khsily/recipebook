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

    title: {
        fontSize: 20,
        fontWeight: 'bold',
    },

    info: {
        flexDirection: 'row',
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