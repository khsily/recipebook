import Api from '../config';

export const fetchCategoryList = () => {
    return Api.get('category');
}