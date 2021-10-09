import React, { useState } from 'react';
import { View, Text, SectionList } from 'react-native';

import { FavorSectionItem, FavorSectionLayout, FavorFooter } from '../../components';

import { styles } from './styles';

const DATA = [
    {
        cateogry: "한식",
        data: [
            { id: 1, name: '라면', image: 'http://res.heraldm.com/phpwas/restmb_idxmake.php?idx=507&simg=/content/image/2019/04/19/20190419000369_0.jpg' },
            { id: 2, name: '김치찌개', image: 'https://mblogthumb-phinf.pstatic.net/MjAyMDAxMDZfMjEz/MDAxNTc4MzE2NTc2ODEw.b6IujcsSNNPhBWMs5moOBwSkmkMxZ6EEXy0V8FfBryEg.WPC2CZCowQJSuFfiyipT1Vea8jVr6BGHCdcL6PXVpdQg.PNG.llzzinll/SE-3ffe00fc-a9fb-48a3-89a2-1d0f8a934cef.png?type=w800' },
            { id: 3, name: '제육볶음', image: 'https://recipe1.ezmember.co.kr/cache/recipe/2015/05/27/38013d1dfd8fa46a871b9cda074b26341.jpg' },
            { id: 4, name: '라면', image: 'http://res.heraldm.com/phpwas/restmb_idxmake.php?idx=507&simg=/content/image/2019/04/19/20190419000369_0.jpg' },
            { id: 5, name: '김치찌개', image: 'https://mblogthumb-phinf.pstatic.net/MjAyMDAxMDZfMjEz/MDAxNTc4MzE2NTc2ODEw.b6IujcsSNNPhBWMs5moOBwSkmkMxZ6EEXy0V8FfBryEg.WPC2CZCowQJSuFfiyipT1Vea8jVr6BGHCdcL6PXVpdQg.PNG.llzzinll/SE-3ffe00fc-a9fb-48a3-89a2-1d0f8a934cef.png?type=w800' },
            { id: 6, name: '제육볶음', image: 'https://recipe1.ezmember.co.kr/cache/recipe/2015/05/27/38013d1dfd8fa46a871b9cda074b26341.jpg' },
        ]
    },
    {
        cateogry: "중식",
        data: [
            { id: 7, name: '라면', image: 'http://res.heraldm.com/phpwas/restmb_idxmake.php?idx=507&simg=/content/image/2019/04/19/20190419000369_0.jpg' },
            { id: 8, name: '김치찌개', image: 'https://mblogthumb-phinf.pstatic.net/MjAyMDAxMDZfMjEz/MDAxNTc4MzE2NTc2ODEw.b6IujcsSNNPhBWMs5moOBwSkmkMxZ6EEXy0V8FfBryEg.WPC2CZCowQJSuFfiyipT1Vea8jVr6BGHCdcL6PXVpdQg.PNG.llzzinll/SE-3ffe00fc-a9fb-48a3-89a2-1d0f8a934cef.png?type=w800' },
            { id: 9, name: '제육볶음', image: 'https://recipe1.ezmember.co.kr/cache/recipe/2015/05/27/38013d1dfd8fa46a871b9cda074b26341.jpg' },
            { id: 10, name: '라면', image: 'http://res.heraldm.com/phpwas/restmb_idxmake.php?idx=507&simg=/content/image/2019/04/19/20190419000369_0.jpg' },
            { id: 11, name: '김치찌개', image: 'https://mblogthumb-phinf.pstatic.net/MjAyMDAxMDZfMjEz/MDAxNTc4MzE2NTc2ODEw.b6IujcsSNNPhBWMs5moOBwSkmkMxZ6EEXy0V8FfBryEg.WPC2CZCowQJSuFfiyipT1Vea8jVr6BGHCdcL6PXVpdQg.PNG.llzzinll/SE-3ffe00fc-a9fb-48a3-89a2-1d0f8a934cef.png?type=w800' },
            { id: 12, name: '제육볶음', image: 'https://recipe1.ezmember.co.kr/cache/recipe/2015/05/27/38013d1dfd8fa46a871b9cda074b26341.jpg' },
        ]
    },
    {
        cateogry: "양식",
        data: [
            { id: 13, name: '라면', image: 'http://res.heraldm.com/phpwas/restmb_idxmake.php?idx=507&simg=/content/image/2019/04/19/20190419000369_0.jpg' },
            { id: 14, name: '김치찌개', image: 'https://mblogthumb-phinf.pstatic.net/MjAyMDAxMDZfMjEz/MDAxNTc4MzE2NTc2ODEw.b6IujcsSNNPhBWMs5moOBwSkmkMxZ6EEXy0V8FfBryEg.WPC2CZCowQJSuFfiyipT1Vea8jVr6BGHCdcL6PXVpdQg.PNG.llzzinll/SE-3ffe00fc-a9fb-48a3-89a2-1d0f8a934cef.png?type=w800' },
            { id: 15, name: '제육볶음', image: 'https://recipe1.ezmember.co.kr/cache/recipe/2015/05/27/38013d1dfd8fa46a871b9cda074b26341.jpg' },
            { id: 16, name: '라면', image: 'http://res.heraldm.com/phpwas/restmb_idxmake.php?idx=507&simg=/content/image/2019/04/19/20190419000369_0.jpg' },
            { id: 17, name: '김치찌개', image: 'https://mblogthumb-phinf.pstatic.net/MjAyMDAxMDZfMjEz/MDAxNTc4MzE2NTc2ODEw.b6IujcsSNNPhBWMs5moOBwSkmkMxZ6EEXy0V8FfBryEg.WPC2CZCowQJSuFfiyipT1Vea8jVr6BGHCdcL6PXVpdQg.PNG.llzzinll/SE-3ffe00fc-a9fb-48a3-89a2-1d0f8a934cef.png?type=w800' },
            { id: 18, name: '제육볶음', image: 'https://recipe1.ezmember.co.kr/cache/recipe/2015/05/27/38013d1dfd8fa46a871b9cda074b26341.jpg' },
        ]
    },
];

const FavorScreen = () => {
    const [selectedItems, setSelectedItems] = useState([]);

    function selectItem(item, maxSize = 5) {
        const index = getIndexOfSelectedItem(item.id);

        if (index > -1) {
            selectedItems.splice(index, 1);
            setSelectedItems([...selectedItems]);
            return;
        }

        if (selectedItems.length >= maxSize) {
            alert('최대 5개까지만 선택 가능해요');
            return;
        }

        setSelectedItems([...selectedItems, item]); 
    }

    function getIndexOfSelectedItem(id) {
        return selectedItems.findIndex((v) => v.id === id);
    }

    return (
        <View style={styles.contrainer}>
            <View style={styles.header}>
                <Text style={styles.title}>어떤 요리를 좋아하세요?</Text>
                <Text style={styles.description}>취향을 선택하고 나에게 맞는 레시피를 받아보세요</Text>
            </View>
            <SectionList
                style={styles.section}
                contentContainerStyle={styles.sectionContent}
                stickySectionHeadersEnabled={false}
                sections={DATA}
                keyExtractor={(v, i) => v + i}
                renderSectionHeader={({ section: { cateogry } }) => (
                    <Text style={styles.sectionTitle}>{cateogry}</Text>
                )}
                renderItem={({ section, index }) => (
                    <FavorSectionLayout
                        renderItem={({ item }) => (
                            <FavorSectionItem
                                selected={getIndexOfSelectedItem(item.id) > -1}
                                onPress={() => selectItem(item)}
                                {...item} />
                        )}
                        section={section}
                        index={index} />
                )} />
            <FavorFooter selectedItems={selectedItems} />
        </View>
    );
}

export default FavorScreen;
