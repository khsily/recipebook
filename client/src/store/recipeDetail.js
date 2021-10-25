import { makeAutoObservable } from 'mobx';
import { Recipe } from '../api';

class RecommendRecipeStore {
    detail = null;
    isFetching = false;

    constructor() {
        makeAutoObservable(this)
    }

    _setDetail(detail) {
        this.detail = detail;
    }

    _setIsFetching(isFetching) {
        this.isFetching = isFetching;
    }

    reset() {
        this._setDetail(null);
    }

    async fetchDetail(id) {
        this._setIsFetching(true);

        const recipe = await Recipe.fetchDetail(id);
        this._setDetail(recipe.data);

        this._setIsFetching(false);
    }
}

const recommendRecipeStore = new RecommendRecipeStore();
export default recommendRecipeStore;

