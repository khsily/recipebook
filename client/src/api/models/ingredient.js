import Api from '../config';

export const fetchIngredientList = () => {
    return Api.get('ingredient');
}

export const detectIngredientFromImage = (image) => {
    return Api.post('ingredient/detection', {
        payload: { image },
        multipart: true,
    });
}