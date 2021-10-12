import { Platform, StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        height: 30,
        zIndex: Platform.select({
            android: undefined,
            ios: 1,
        })
    },

    button: {
        height: '100%',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 0,
    },

    divider: {
        position: 'absolute',
        left: 0,
        bottom: -5,
        borderBottomWidth: 1,
        borderColor: '#CCCCCC',
        width: '100%',
    },
});