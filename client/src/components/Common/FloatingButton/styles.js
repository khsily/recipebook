import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    button: {
        position: 'absolute',
        right: 14,
        bottom: 14,
        zIndex: 1,
        backgroundColor: '#FFFFFF',
        borderWidth: 3,
        borderRadius: 100,
        padding: 10,
    },

    icon: {
        width: 35,
        height: 35,
        resizeMode: 'contain',
    },
});