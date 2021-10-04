import { useActionSheet } from '@expo/react-native-action-sheet';
import { openCamera, openGallery } from '../utils';

export function useCameraAction() {
    const { showActionSheetWithOptions } = useActionSheet();

    async function onActionSheetSelect(buttonIndex, callback) {
        let result;
        if (buttonIndex == 0) result = await openCamera();
        if (buttonIndex == 1) result = await openGallery();
        if (buttonIndex == 2) return;
        callback(result);
    }

    function show(callback) {
        showActionSheetWithOptions({
            options: ['식재료 촬영', '갤러리에서 선택', '닫기'],
            destructiveButtonIndex: 2,
            cancelButtonIndex: 2,
        }, (buttonIndex) => onActionSheetSelect(buttonIndex, callback))
    }

    return show;
}