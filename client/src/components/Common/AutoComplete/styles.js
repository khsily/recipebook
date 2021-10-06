import { Dimensions, StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    container: {
    },

    input: {
        height: '100%',
        fontSize: 14,
        paddingHorizontal: 8,
        height: 30,

        // flex: 1을 컨테이너에 주게 되면 ios에서 crash (버그)
        // 크기를 조절하려면 직접 수정 필요
        width: Dimensions.get('window').width - 92,
    },

    listWrapper: {
        position: 'absolute',
        top: 37,
        zIndex: 1,
        width: '100%',
        borderWidth: 1,
        borderColor: '#CCCCCC',
        backgroundColor: '#FFFFFF',
        maxHeight: 150,
    },

    listContainer: {
        width: '100%',
    },

    list: {
        backgroundColor: '#FFFFFF',
        paddingVertical: 8,
        paddingHorizontal: 12,
        color: '#333333',
    },
});