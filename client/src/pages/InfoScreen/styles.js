import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        paddingBottom: '5%',
    },

    wrapper: {
        flex: 1,
    },

    header: {
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: '5%',
    },

    title: {
        fontSize: 30,
        marginTop: '15%',
        marginBottom: 10,
    },

    info: {
        marginBottom: 10,
        color: '#999',
    },

    contributorContrainer: {
        padding: '5%',
    },

    contributorTitle: {
        fontSize: 20,
        marginBottom: 10,
        textAlign: 'center',
    },

    contributorInfo: {
        marginBottom: 10,
        textAlign: 'center',
        color: '#666',
    },

    button: {
        width: '70%',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 10,
        marginBottom: 10,
        borderRadius: 30,
        backgroundColor: '#DDD',
        borderWidth: 1,
        borderColor: '#DCDCDC',
    },

    buttonText: {
        color: '#555',
        fontWeight: 'bold',
    },
});