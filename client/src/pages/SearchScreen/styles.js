import { Dimensions, StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    container: {
        flex: 1,
    },

    wrapper: {
        flex: 1,
    },

    scrollview: {
        padding: 14,
    },

    searchInput: {
        width: Dimensions.get('window').width - 120,
    },

    searchButton: {
        width: '100%',
        height: 45,
        alignItems: 'center',
        justifyContent: 'center',
        padding: 0,
    },

    searchButtonText: {
        fontFamily: 'AppleSDGothicNeoB',
        fontSize: 18,
    },

    tags: {
        paddingTop: 5,
        flexDirection: 'row',
        flexWrap: 'wrap',
        marginLeft: -10,
    },

    tag: {
        marginLeft: 10,
        marginTop: 10,
    },

    emptyList: {
        alignItems: 'center',
        justifyContent: 'center',
        flex: 1,
    },

    emptyText: {
        fontSize: 14,
        color: '#BBBBBB',
    },
});