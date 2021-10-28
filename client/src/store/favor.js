import { makeAutoObservable } from 'mobx';
import { Category, Recipe } from '../api';

class FavorStore {
    favors = [];
    isFetching = false;

    constructor() {
        makeAutoObservable(this)
    }

    // sectionList에서 사용하기 위해 추가 포맷팅 필요
    get formattedFavors() {
        return this.favors.map(v => ({
            ...v,
            data: v.data.slice(),
        })).slice();
    }

    _setFavors(favors) {
        this.favors = favors;
    }

    _setIsFetching(isFetching) {
        this.isFetching = isFetching;
    }

    async fetchList() {
        this._setIsFetching(true);

        let categories = await Category.fetchCategoryList();
        categories = categories.data.map((v) => v.name);

        let favors = await Recipe.fetchFavorList();
        favors = favors.data.reduce((prev, curr) => {
            if (!prev[curr.category]) prev[curr.category] = [];
            prev[curr.category].push(curr);
            return prev;
        }, {});
        favors = Object.entries(favors).map(([category, data]) => ({ category, data }));
        this._setFavors(favors);

        this._setIsFetching(false);
    }
}

const favorStore = new FavorStore();
export default favorStore;

