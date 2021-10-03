import { StyleSheet } from "react-native";
import { MainTheme } from "../../../styles/themes";

export const styles = StyleSheet.create({
    button: {
        alignSelf: 'baseline',
        padding: 8,
        paddingHorizontal: 20,
        backgroundColor: MainTheme.colors.primary,
        borderRadius: 15,
    },

    text: {
        color: '#FFFFFF',
        fontSize: 14,
        fontWeight: 'bold',
    }
});