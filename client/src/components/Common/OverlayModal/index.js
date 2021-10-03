import React from 'react';
import { View, Modal } from 'react-native';
import { styles } from './styles';

function OverlayModal({ visible = false, ...props }) {
    return (
        <Modal animationType="fade" transparent visible={visible}>
            <View {...props} style={{ ...styles.contrainer, ...props.style }} />
        </Modal>
    );
}

export default OverlayModal;