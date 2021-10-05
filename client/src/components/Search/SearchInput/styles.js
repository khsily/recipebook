import { Dimensions, Platform, StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    container: {
        position: 'relative',
        flexDirection: 'row',
        width: '100%',
        height: 30,
    },

    leftContainer: {
        flex: 1,
    },

    inputPosWrapper: {
        position: 'absolute',
        top: 0,
        left: 0,
        zIndex: 1,
        width: '100%',
    },

    inputContainer: {
        height: '100%',
    },

    input: {
        height: 30,
        paddingHorizontal: 8,
        borderWidth: 0,
    },

    listContainer: {
        top: 5,
        right: 0,

        ...Platform.select({
            ios: {
                width: Dimensions.get('window').width - 28,
            },
            android: {
                left: -10,
                width: Dimensions.get('window').width - 8,
            },
        })
    },

    list: {
        padding: 5,
        paddingHorizontal: 10,
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