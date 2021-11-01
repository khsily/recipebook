import { makeAutoObservable } from 'mobx';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Recipe } from '../api';

class MyFavor {
    storageKey = '@my_favor';
    favors = [];
    combinationId = 0;
    isFetching = false;

    constructor() {
        makeAutoObservable(this);
    }

    _setFavors(favors) {
        this.favors = favors;
    }

    _setCombinationId(id) {
        this.combinationId = id;
    }

    _setIsFetching(isFetching) {
        this.isFetching = isFetching;
    }

    async saveFavors(favors) {
        const jsonValue = JSON.stringify(favors);
        await AsyncStorage.setItem(this.storageKey, jsonValue);
        await this.fetchList();
    }

    async fetchList() {
        this._setIsFetching(true);

        const jsonValue = await AsyncStorage.getItem(this.storageKey);
        const favors = jsonValue ? JSON.parse(jsonValue) : [];
        await this.fetchId(favors);
        this._setFavors(favors);

        this._setIsFetching(false);
    }

    async fetchId(favors) {
        if (favors.length === 0) return;

        const favorTitles = favors.map((v) => v.title);
        const combination = await Recipe.fetchCombinationId(favorTitles);
        const id = combination.data[0].id;
        this._setCombinationId(id);
    }

    async clear() {
        await this.saveFavors([]);
    }
}

const myFavorStore = new MyFavor();
export default myFavorStore;

