import { MainTheme } from "./themes"
import { CardStyleInterpolators } from '@react-navigation/stack';

export const header_style = {
    headerStyle: {
        backgroundColor: MainTheme.colors.primary,
    },
    headerTintColor: '#fff',
    headerTitleStyle: {
        fontWeight: 'bold',
    },
    headerTitleAlign: 'center',
    headerBackTitleVisible: false,
}

export const transition_style = {
    cardStyleInterpolator: CardStyleInterpolators.forHorizontalIOS,
}