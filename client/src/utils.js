import React from 'react'
import { Text, StyleSheet } from 'react-native'
import * as ImagePicker from 'expo-image-picker';


export async function openGallery(options) {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
        alert('권한이 없으면 사용이 불가능합니다. 권한 요청을 수락해주세요!');
        return;
    }

    try {
        return await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.All,
            quality: 1,
            ...options,
        });
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
        return await ImagePicker.launchCameraAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.All,
            ...options,
        });
    } catch (e) {
        console.error(e);
    }
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
        prev[name] = prev[name].replace(/\\054/g, ',').split(',');
        if (prev[name].length <= 1) prev[name] = prev[name][0]
        return prev;
    }, {});
}


export async function blob2base54(blob) {
    const fr = new FileReader();
    fr.readAsDataURL(blob);

    return new Promise((resolve, reject) => {
        fr.onload = () => resolve(fr.result);
        fr.onerror = () => reject;
    })
}