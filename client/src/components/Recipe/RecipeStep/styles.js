import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#F4F4F4',
        padding: 10,
        paddingLeft: 5,
        borderBottomWidth: 1,
        borderBottomColor: '#DDDDDD',
    },

    no: {
        fontSize: 20,
        fontWeight: 'bold',
        width: 20,
        textAlign: 'center',
    },

    image: {
        width: 100,
        height: 100,
        marginLeft: 5,
        marginRight: 10,
    },

    content: {
        flex: 1,
        color: '#333333',
    },
});