import { makeAutoObservable } from 'mobx';
import { Category } from '../api';

class CategoryStore {
    categories = []
    isFetching = false;

    constructor() {
        makeAutoObservable(this)
    }

    async fetchList() {
        this.isFetching = true;

        let categories = await Category.fetchCategoryList();
        this.categories = categories.data;

        this.isFetching = false;
    }
}

const categoryStore = new CategoryStore();
export default categoryStore;

