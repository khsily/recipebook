import React from 'react';
import { Text, View } from 'react-native';

import { HeaderButton } from '../../components';
import { useCameraAction } from '../../customHook/useCameraAction';

import ic_camera from '../../../assets/icon/ic_camera.png';

const SearchScreen = ({ navigation }) => {
    const showAction = useCameraAction();

    React.useLayoutEffect(() => {
        navigation.setOptions({
            headerRight: () => (
                <HeaderButton icon={ic_camera} onPress={() => showAction((res) => console.log(res))} />
            )
        });
    }, [navigation]);

    return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
            <Text>Search Screen</Text>
        </View>
    );
}

export default SearchScreen;
