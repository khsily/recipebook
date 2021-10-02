import { DefaultTheme } from '@react-navigation/native';

export const MainTheme = {
    ...DefaultTheme,
    colors: {  // primary, background, card, text, border, notification
        ...DefaultTheme.colors,
        primary: '#62B4FF',
        primaryRed: '#E74C3C',
        primaryRedLight: '#EE8276',
        background: '#FFFFFF',
    },
};