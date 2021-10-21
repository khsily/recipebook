import Api from '../config';

export const fetchIngredientList = () => {
    return Api.get('ingredient');
}

export const detectIngredientFromImage = (uri) => {
    const name = uri.split('/').pop();

    // 이미지 타입
    const match = /\.(\w+)$/.exec(name);
    const type = match ? `image/${match[1]}` : `image`;

    return Api.post('ingredient/detection', {
        payload: { image: { name, uri, type } },
        multipart: true,
    });
}

export const detectIngredientFromImage2 = (image) => {
    return Api.post('ingredient/detection', {
        payload: { image },
        multipart: true,
    });
}