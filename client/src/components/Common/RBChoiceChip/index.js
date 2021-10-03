import React from 'react';
import RBButton from '../RBButton'
import { styles } from './styles';

function RBChoiceChip({ active, ...props }) {
    const chipStyle = active ? {} : styles.inactive
    const color = active ? '#FFFFFF' : '#B3B3B3';

    return (
        <RBButton
            {...props}
            rounded
            color={color}
            style={{ ...chipStyle, ...props.style }} />
    );
}

export default RBChoiceChip;