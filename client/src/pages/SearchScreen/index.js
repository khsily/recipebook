import React, { useState } from 'react';
import { Text, View } from 'react-native';

import { HeaderButton, LoadingModal } from '../../components';
import { useCameraAction } from '../../customHook/useCameraAction';

import ic_camera from '../../../assets/icon/ic_camera.png';
import { fakeLoading } from '../../utils';

const SearchScreen = ({ navigation }) => {
    const [isDetectioning, setIsDetectioning] = useState(false);
    const showAction = useCameraAction();

    function handleDetection() {
        showAction(async (res) => {
            setIsDetectioning(true);
            // TODO: object detection 수행
            await fakeLoading(4000);

            // TODO: object detection 완료 결과 보여주기
            setIsDetectioning(false);
            console.log(res);
            navigation.navigate('Detection', {
                images: [res.uri],
                from: 'Search',
            });
        })
    }

    React.useLayoutEffect(() => {
        navigation.setOptions({
            headerRight: () => (
                <HeaderButton icon={ic_camera} onPress={handleDetection} />
            )
        });
    }, [navigation]);

    return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
            <Text>Search Screen</Text>
            <LoadingModal visible={isDetectioning} text='식재료를 확인하고 있어요...' />
        </View>
    );
}

export default SearchScreen;
