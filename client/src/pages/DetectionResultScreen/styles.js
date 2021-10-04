import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#000',
    },

    buttonWrapper: {
        width: '100%',
        height: 50,
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'row',
    },

    button: {
        backgroundColor: 'rgba(255, 255, 255, 0.7)',
        width: 100,
        height: '70%',
        marginHorizontal: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },

    buttonLeft: {
        borderTopLeftRadius: 20,
        borderBottomLeftRadius: 20,
    },

    buttonRight: {
        borderTopRightRadius: 20,
        borderBottomRightRadius: 20,
    },

    buttonText: {
        fontWeight: 'bold',
    }
});