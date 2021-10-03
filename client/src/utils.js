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
            fontFamily: 'AppleSDGothicNeoM',//Default font family
        }
    });

    const oldTextRender = Text.render
    Text.render = function (...args) {
        const origin = oldTextRender.call(this, ...args)
        return React.cloneElement(origin, {
            style: [styles.defaultText, origin.props.style],
        })
    }
}