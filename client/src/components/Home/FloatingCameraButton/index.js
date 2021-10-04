import React from 'react';
import FloatingButton from '../../Common/FloatingButton';

import { styles } from './styles';
import ic_camera_red from '../../../../assets/icon/ic_camera_red.png';

function FloatingCameraButton({ onAction = (() => { }), ...props }) {
    return (
        <FloatingButton
            {...props}
            style={styles.button}
            icon={ic_camera_red} />
    );
}

export default FloatingCameraButton;