import React from 'react';
import FloatingButton from '../../Common/FloatingButton';

import { styles } from './styles';
import ic_camera_red from '../../../../assets/icon/ic_camera_red.png';
import { useActionSheet } from '@expo/react-native-action-sheet';

import { openCamera, openGallery } from '../../../utils';

function FloatingCameraButton({ onAction = (() => { }), ...props }) {
    const { showActionSheetWithOptions } = useActionSheet();

    async function onActionSheetSelect(buttonIndex) {
        let result;
        if (buttonIndex == 0) result = await openCamera();
        if (buttonIndex == 1) result = await openGallery();
        if (buttonIndex == 2) return;
        onAction(result);
    }

    return (
        <FloatingButton
            {...props}
            style={styles.button}
            icon={ic_camera_red}
            onPress={() => {
                showActionSheetWithOptions({
                    options: ['식재료 촬영', '갤러리에서 선택', '닫기'],
                    destructiveButtonIndex: 2,
                    cancelButtonIndex: 2,
                }, onActionSheetSelect)
            }} />
    );
}

export default FloatingCameraButton;