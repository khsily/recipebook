import React, { useState } from 'react';
import { View, Text, SectionList } from 'react-native';

import { FavorSectionItem, FavorSectionLayout, FavorFooter } from '../../components';
import { myFavorStore, favorStore } from '../../store';
import { styles } from './styles';


const FavorScreen = () => {
    const [selectedItems, setSelectedItems] = useState([]);

    function selectItem(item, maxSize = 4) {
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

    function handleSubmit() {
        if (selectedItems.length < 3) {
            alert('최소 3개 이상 선택해 주세요');
            return;
        }
        myFavorStore.saveFavors(selectedItems);
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
                sections={favorStore.formattedFavors}
                keyExtractor={(v) => `favor_${v.id}`}
                renderSectionHeader={({ section: { category } }) => (
                    <Text style={styles.sectionTitle}>{category}</Text>
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
            <FavorFooter
                selectedItems={selectedItems}
                onSubmit={handleSubmit} />
        </View>
    );
}

export default FavorScreen;
