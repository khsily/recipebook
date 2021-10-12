import { makeAutoObservable } from 'mobx';
import { fakeLoading } from '../utils';
import * as dummy from './dummyData';

class Recipe {
    recommend = []
    sufficient = []
    insufficient = []
    isFetching = false;

    constructor() {
        makeAutoObservable(this)
    }

    async fetchRecoomend() {
        this.isFetching = true;

        await fakeLoading(2000);
        this.recommend = dummy.recommends.payload.data;

        this.isFetching = false;
    }

    async fetchList() {
        this.isFetching = true;

        await fakeLoading(2000);
        const { sufficient, insufficient } = dummy.recipes.payload.data
        this.sufficient = sufficient;
        this.insufficient = insufficient;

        this.isFetching = false;
    }
}

const recipeStore = new Recipe();
export default recipeStore;

