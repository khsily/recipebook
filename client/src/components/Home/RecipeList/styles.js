import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        marginBottom: 12,
    },

    thumbnail: {
        width: 130,
        height: 130,
    },

    content: {
        flex: 1,
        padding: 8,
    },

    title: {
        fontSize: 15,
        fontWeight: 'bold',
    },
});