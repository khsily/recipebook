import { makeAutoObservable } from 'mobx';
import { fakeLoading } from '../utils';
import * as dummy from './dummyData';

class Category {
    categories = []
    isFetching = false;

    constructor() {
        makeAutoObservable(this)
    }

    async fetchList() {
        this.isFetching = true;

        await fakeLoading(500);
        this.categories = dummy.categories.payload.data;

        this.isFetching = false;
    }
}

const categoryStore = new Category();
export default categoryStore;

