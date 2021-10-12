import { makeAutoObservable } from 'mobx';
import AsyncStorage from '@react-native-async-storage/async-storage';

class MyFavor {
    storageKey = '@my_favor';
    favors = [];
    isFetching = false;

    constructor() {
        makeAutoObservable(this);
    }

    _setFavors(favors) {
        this.favors = favors;
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
        this._setFavors(jsonValue ? JSON.parse(jsonValue) : []);

        this._setIsFetching(false);
    }

    async clear() {
        await this.saveFavors([]);
    }
}

const myFavorStore = new MyFavor();
export default myFavorStore;

