import React from 'react'
import { Text, StyleSheet } from 'react-native'
import * as ImagePicker from 'expo-image-picker';
import { manipulateAsync } from 'expo-image-manipulator';


export async function openGallery(options) {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
        alert('권한이 없으면 사용이 불가능합니다. 권한 요청을 수락해주세요!');
        return;
    }

    try {
        const image = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.All,
            quality: 1,
            ...options,
        });
        const resizedImage = await resizeImage(image, 800);
        return { ...image, ...resizedImage };
    } catch (e) {
        console.error(e);
    }
}


export async function openCamera(options) {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
        alert('권한이 없으면 사용이 불가능합니다. 권한 요청을 수락해주세요!');
        return;
    }

    try {
        const image = await ImagePicker.launchCameraAsync({
            quality: 0.5,
            mediaTypes: ImagePicker.MediaTypeOptions.All,
            ...options,
        });
        const resizedImage = await resizeImage(image, 800);
        return { ...image, ...resizedImage };
    } catch (e) {
        console.error(e);
    }
}


export async function resizeImage(image, width) {
    const resizedImage = await manipulateAsync(
        image.localUri || image.uri,
        [{ resize: { width } }],
        { compress: 1, format: 'jpeg' },
    );

    return resizedImage;
}


export const typography = () => {
    const styles = StyleSheet.create({
        defaultText: {
            fontFamily: 'AppleSDGothicNeoM',
        },

        defaultBoldText: {
            fontFamily: 'AppleSDGothicNeoB',
        }
    });

    const oldTextRender = Text.render
    Text.render = function (...args) {
        const origin = oldTextRender.call(this, ...args);

        const isBold = origin && origin.props && origin.props.style && (origin.props.style.fontWeight === 'bold');
        const fontStyle = isBold ? styles.defaultBoldText : styles.defaultText;

        return React.cloneElement(origin, {
            style: [fontStyle, origin.props.style],
        })
    }
}


export function fakeLoading(time = 1000) {
    return new Promise((resolve) => {
        window.setTimeout(resolve, time);
    });
}


export function cookie2obj(cookieStr) {
    return cookieStr.split('; ').reduce((prev, current) => {
        const [name, ...value] = current.split('=');
        prev[name] = value.join('=').replace(/"/g, '');
        prev[name] = prev[name].replace(/\\054/g, ',');
        return prev;
    }, {});
}

export function decodeUnicode(unicodeString) {
    const r = /\\u([\d\w]{4})/gi;
    unicodeString = unicodeString.replace(r, (_, grp) => {
        return String.fromCharCode(parseInt(grp, 16));
    });
    return unicodeString.replace(/\\/g, '');
}


export async function blob2base54(blob) {
    const fr = new FileReader();
    fr.readAsDataURL(blob);

    return new Promise((resolve, reject) => {
        fr.onload = () => resolve(fr.result);
        fr.onerror = () => reject;
    })
}