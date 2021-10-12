import { makeAutoObservable } from 'mobx';
import { fakeLoading } from '../utils';
import * as dummy from './dummyData';

class Ingredient {
    ingredients = []
    isFetching = false;

    constructor() {
        makeAutoObservable(this)
    }

    async fetchList() {
        this.isFetching = true;

        await fakeLoading(500);
        this.ingredients = dummy.ingredients.payload.data;

        this.isFetching = false;
    }
}

const ingredientStore = new Ingredient();
export default ingredientStore;

